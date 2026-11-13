from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite, log2
from statistics import mean, pstdev
from typing import Iterable, Sequence


@dataclass(frozen=True)
class DynamicProfile:
    """Dependency-free operational profile inspired by empirical consciousness work.

    The metrics are engineering measurements, not a consciousness detector.
    """

    channels: int
    samples: int
    activity_mean: float
    activity_std: float
    lag1_autocorrelation: float
    pairwise_correlation: float
    metastability: float
    lz_complexity: float
    avalanche_count: int
    avalanche_mean_size: float
    avalanche_largest_size: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def _clean_channels(channels: Iterable[Sequence[float]]) -> list[list[float]]:
    cleaned: list[list[float]] = []
    for channel in channels:
        # Reject invalid samples rather than deleting them independently:
        # removing one NaN at position t shifts that channel's time axis and
        # manufactures inter-channel correlations at the wrong timestamps.
        try:
            values = [float(value) for value in channel]
        except (ValueError, TypeError, OverflowError) as exc:
            raise ValueError("channel samples must be numeric and finite") from exc
        if not values:
            raise ValueError("channels must be non-empty")
        if any(not isfinite(value) for value in values):
            raise ValueError("channel samples must be numeric and finite")
        cleaned.append(values)
    if not cleaned:
        raise ValueError("at least one non-empty numeric channel is required")
    length = min(len(channel) for channel in cleaned)
    if length < 3:
        raise ValueError("channels require at least 3 samples")
    return [channel[:length] for channel in cleaned]


def _zscore(values: Sequence[float]) -> list[float]:
    mu = mean(values)
    sigma = pstdev(values)
    if sigma <= 1e-12:
        return [0.0 for _ in values]
    return [(value - mu) / sigma for value in values]


def _correlation(left: Sequence[float], right: Sequence[float]) -> float:
    z_left = _zscore(left)
    z_right = _zscore(right)
    denom = len(z_left)
    if denom == 0:
        return 0.0
    return sum(a * b for a, b in zip(z_left, z_right)) / denom


def _lag1_autocorrelation(values: Sequence[float]) -> float:
    return max(-1.0, min(1.0, _correlation(values[:-1], values[1:])))


def _binary_lz_complexity(bits: Sequence[int]) -> float:
    """Normalized Lempel-Ziv complexity for a binary sequence."""
    n = len(bits)
    if n < 2:
        return 0.0
    sequence = "".join("1" if bit else "0" for bit in bits)
    dictionary: set[str] = set()
    i = 0
    phrases = 0
    while i < n:
        length = 1
        while i + length <= n and sequence[i : i + length] in dictionary:
            length += 1
        phrase = sequence[i : min(n, i + length)]
        dictionary.add(phrase)
        phrases += 1
        i += len(phrase)

    normalizer = max(1.0, n / max(1.0, log2(n)))
    return max(0.0, min(1.0, phrases / normalizer))


def _timewise_synchrony(channels: Sequence[Sequence[float]]) -> list[float]:
    """A dependency-free synchrony proxy."""
    n = len(channels)
    if n == 1:
        return [1.0]
    window = max(8, min(32, len(channels[0]) // 8))
    values: list[float] = []
    for start in range(0, len(channels[0]) - window + 1, max(1, window // 2)):
        stop = start + window
        pair_values: list[float] = []
        for i in range(n):
            for j in range(i + 1, n):
                pair_values.append(abs(_correlation(channels[i][start:stop], channels[j][start:stop])))
        values.append(mean(pair_values) if pair_values else 0.0)
    return values or [0.0]


def _avalanche_sizes(channels: Sequence[Sequence[float]], threshold_sigma: float) -> list[float]:
    """Extract simple event cascades from thresholded multichannel activity."""
    zchannels = [_zscore(channel) for channel in channels]
    active = [
        sum(1 for channel in zchannels if abs(channel[index]) >= threshold_sigma)
        for index in range(len(zchannels[0]))
    ]
    sizes: list[float] = []
    running = 0.0
    for count in active:
        if count > 0:
            running += float(count)
        elif running > 0:
            sizes.append(running)
            running = 0.0
    if running > 0:
        sizes.append(running)
    return sizes


def measure_dynamics(
    channels: Iterable[Sequence[float]],
    *,
    avalanche_threshold_sigma: float = 2.0,
) -> DynamicProfile:
    """Compute the first dependency-free Dynamic Core profile."""
    if isinstance(avalanche_threshold_sigma, bool):
        raise ValueError("avalanche_threshold_sigma must be finite and positive")
    try:
        threshold = float(avalanche_threshold_sigma)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError("avalanche_threshold_sigma must be finite and positive") from exc
    if not isfinite(threshold) or threshold <= 0.0:
        raise ValueError("avalanche_threshold_sigma must be finite and positive")
    cleaned = _clean_channels(channels)
    flattened = [value for channel in cleaned for value in channel]
    synchrony = _timewise_synchrony(cleaned)
    avalanche_sizes = _avalanche_sizes(cleaned, threshold)

    reference = cleaned[0]
    median = sorted(reference)[len(reference) // 2]
    bits = [1 if value >= median else 0 for value in reference]

    return DynamicProfile(
        channels=len(cleaned),
        samples=len(reference),
        activity_mean=round(mean(flattened), 6),
        activity_std=round(pstdev(flattened), 6),
        lag1_autocorrelation=round(mean(_lag1_autocorrelation(channel) for channel in cleaned), 6),
        pairwise_correlation=round(mean(synchrony), 6),
        metastability=round(pstdev(synchrony) if len(synchrony) > 1 else 0.0, 6),
        lz_complexity=round(_binary_lz_complexity(bits), 6),
        avalanche_count=len(avalanche_sizes),
        avalanche_mean_size=round(mean(avalanche_sizes), 6) if avalanche_sizes else 0.0,
        avalanche_largest_size=round(max(avalanche_sizes), 6) if avalanche_sizes else 0.0,
    )


def compare_dynamics(
    baseline: DynamicProfile,
    current: DynamicProfile,
) -> dict[str, float]:
    fields = (
        "lag1_autocorrelation",
        "pairwise_correlation",
        "metastability",
        "lz_complexity",
        "avalanche_mean_size",
        "avalanche_largest_size",
    )
    delta: dict[str, float] = {}
    for field in fields:
        before = float(getattr(baseline, field))
        after = float(getattr(current, field))
        scale = max(1.0, abs(before))
        delta[field] = round((after - before) / scale, 6)
    return delta
