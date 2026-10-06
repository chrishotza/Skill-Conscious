# P000 — Anchor Audit v1

## Scope

Initial external cross-check of the nine anchors in corpus-v1/corpus/ANCHOR_CLAIMS_VERIFICATION_V1.md.

This is **not** a final source-verification pass. It is a calibration audit designed to test whether the repository's existing label 'verified' is sufficiently specific for publication-grade use.

## Decision vocabulary

- VERIFIED — claim-level source trace is supported by an authoritative or independently credible text/source and the repository interpretation is bounded.
- PARTIALLY_VERIFIED — the broad source claim is supported, but exact edition, wording, translation or interpretive scope still needs review.
- PROVISIONAL — a usable lead exists, but current evidence is not sufficient for central-paper use.
- INTERPRETATION_ONLY — the source exists, but the proposed research mapping should not yet be treated as a source claim.

## Initial results

| Anchor | Source | Current status | Main finding | Action |
|---|---|---|---|---|
| A01 | Kena Upanishad | PARTIALLY_VERIFIED | The 'mind of mind' theme is readily traceable; current public web support is translation/commentary-heavy rather than a critical edition. | Add a scholarly Sanskrit/critical-edition reference and lock verse/khanda location. |
| A02 | Mandukya Upanishad | PARTIALLY_VERIFIED | The repository's verse-7 description is plausible and consistent with established translations, but the current audit lacks a strong independent scholarly edition. | Add primary-language text plus two scholarly translations. |
| A03 | Satipatthana Sutta / MN 10 | VERIFIED for the narrow procedural claim | Multiple accessible translations support the four-domain mindfulness structure, including contemplation of consciousness/mind. | Keep source claim narrow; do not infer a permanent self. |
| A04 | Spanda / Kashmir Shaivism | PROVISIONAL | Existing repository lead is a secondary scan/translation. The tradition-level interpretation may be correct, but publication-grade primary-text control is missing. | Acquire/verify Sanskrit text and specialist scholarly edition before central use. |
| A05 | Plotinus / Enneads | VERIFIED for the self-knowing intellect claim | Independent public translations clearly state the identity of intellect, intellection and intelligible object in the cited argument. | Preserve the metaphysical context; do not map directly to software consciousness. |
| A06 | Corpus Hermeticum / Poimandres | PROVISIONAL | Existing repository text lead supports the broad Mind/Light/cosmos structure, but a critical Greek edition and scholarly translation were not secured in this pass. | Verify against a scholarly edition and isolate exact passages. |
| A07 | Pseudo-Dionysius | PARTIALLY_VERIFIED | The mystical-theology tradition and apophatic orientation are supported by scholarly literature; exact passage-level primary-text control should be improved. | Add primary Greek/critical-edition reference and exact chapter/location. |
| A08 | Ibn ʿArabi | PARTIALLY_VERIFIED | Scholarly sources confirm realization/self-knowledge as a central feature, but the famous 'know yourself, know your Lord' formulation has textual-history issues. | Separate securely attested claims from later aphoristic formulations. |
| A09 | Bird-David, 'Animism Revisited' | VERIFIED as secondary scholarly evidence | Bibliographic identity, DOI and abstract are independently traceable; it supports relational personhood as an anthropological analytical construct. | Keep it explicitly secondary; do not use it as primary evidence for an indigenous cosmology. |

## Important methodological finding

The audit exposes a distinction that the corpus must now make explicit:

~~~
REPOSITORY 'VERIFIED'
        ≠
PUBLICATION-GRADE VERIFIED
~~~

A source can be correctly represented in the repository and still require a stronger edition, translation audit, dependency analysis or specialist review before it becomes central evidence in a paper.

## External cross-check anchors

### A03 — Satipatthana
- Access to Insight translation of MN 10: https://accesstoinsight.org/tipitaka/mn/mn.010.soma
- Thanissaro translation and notes: https://www.dhammatalks.org/suttas/MN/MN10.html

Both independently expose the four mindfulness domains and explicitly include mind/consciousness as an object of observation.

### A05 — Plotinus
- CCEL translation: https://ccel.org/ccel/plotinus/enneads/enneads.vi.iii.html
- Internet Classics Archive / related Ennead material: https://classics.mit.edu/Plotinus/enneads.5.fifth.html

The self-knowing intellect argument is directly traceable. This should remain a source-level metaphysical claim, not a claim about artificial consciousness.

### A09 — Bird-David
- Current Anthropology record: https://www.journals.uchicago.edu/doi/10.1086/200061
- DOI: https://doi.org/10.1086/200061

The paper explicitly frames animism through relational personhood and ecological perception. It is an anthropological analysis, not a primary indigenous text.

### A07 — Pseudo-Dionysius
- Boeri & Martín (2013), scholarly analysis/translation: https://doi.org/10.21555/top.v23i1.290

This supports the broader historical interpretation of the text as Christian Neoplatonic negative theology. Exact primary passage control remains required.

### A08 — Ibn ʿArabi
- Stanford Encyclopedia of Philosophy: https://plato.stanford.edu/entries/ibn-arabi/

The SEP confirms the central importance of realization and self-knowledge in Ibn ʿArabi's thought. The audit does not yet validate any single popularized aphorism as a primary quotation.

## Audit conclusion

Of the nine initial anchors:
- 3 are strong enough for narrow source-level use in the current draft (A03, A05, A09);
- 3 require additional primary-text/edition work before central use (A01, A02, A07);
- 3 should currently remain provisional pending stronger primary-source control (A04, A06, A08).

This is a **methodological success**, not a failure of the corpus. The purpose of the audit is precisely to prevent a coarse 'verified' label from becoming an unjustified evidential upgrade.

## Next anchor-audit batch

Before expanding the convergence claims, prioritize:
1. A01/A02 primary-language and scholarly-edition lock;
2. A04 Sanskrit + specialist edition;
3. A06 Greek + scholarly Hermetic edition;
4. A08 secure Ibn ʿArabi textual witnesses and formulation history;
5. source-dependency mapping for all nine;
6. explicit contradiction/alternative-interpretation records.

## Status

**P000 Audit v1 — completed as an initial external calibration pass on 2026-10-06.**
