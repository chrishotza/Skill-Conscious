"""Consciousness-specific causal attack for the runtime SubjectiveField."""
from __future__ import annotations
import json
import tempfile
from pathlib import Path
from typing import Any, Mapping
from skill_conscious import ConsciousRuntime
from skill_conscious.subjective_field import SubjectiveField
from skill_conscious.subjective_field_runtime import ConsciousFieldRuntime

PRESENT={"signal":1.0,"reward":0.7,"threat":0.1,"self_impact":0.9}

def _objective(frame: Mapping[str, Any]) -> float:
    return max(float(item["signals"].get("goal_fit", 0.0)) for item in frame["candidate_futures"])

def run() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        runtime=ConsciousRuntime(
            "subjective-field-agent", root/"state.json",
            report_enabled=False, metacognition_enabled=False,
            self_observation_enabled=False,
        )
        runtime.state.self_state={"energy":0.8,"safety":0.8,"goal":0.6}
        runtime.state.salience={"present":1.0}
        runtime.state.valence=0.4
        bridge=ConsciousFieldRuntime(runtime)

        candidates=[
            {"id":"self_preserving","signals":{"goal_fit":0.6,"self_alignment":0.9}},
            {"id":"world_only","signals":{"goal_fit":0.6,"self_alignment":0.2}},
        ]
        frame={"response":"","internal_state":dict(runtime.state.self_state),"candidate_futures":candidates}
        baseline=bridge.project(PRESENT)
        objective_baseline=_objective(frame)

        no_integration=SubjectiveField().compute(
            PRESENT,runtime.state.self_state,attention=1.0,
            self_relevance=0.9,valence=0.4,integration=False)
        no_relevance=SubjectiveField().compute(
            PRESENT,runtime.state.self_state,attention=1.0,
            self_relevance=0.0,valence=0.4)

        c1=SubjectiveField()
        c1.compute(PRESENT,runtime.state.self_state,attention=1.0,self_relevance=0.9,valence=0.4)
        continuity_on=c1.compute(
            {**PRESENT,"reward":0.65},runtime.state.self_state,
            attention=1.0,self_relevance=0.9,valence=0.35,
            temporal_continuity=True,reentry=False)
        c2=SubjectiveField()
        c2.compute(PRESENT,runtime.state.self_state,attention=1.0,self_relevance=0.9,valence=0.4)
        continuity_off=c2.compute(
            {**PRESENT,"reward":0.65},runtime.state.self_state,
            attention=1.0,self_relevance=0.9,valence=0.35,
            temporal_continuity=False,reentry=False)

        r1=SubjectiveField()
        r1.compute(PRESENT,runtime.state.self_state,attention=1.0,self_relevance=0.9,valence=0.4)
        reentry_on=r1.compute(
            {**PRESENT,"reward":0.1},runtime.state.self_state,
            attention=1.0,self_relevance=0.1,valence=0.0,reentry=True)
        r2=SubjectiveField()
        r2.compute(PRESENT,runtime.state.self_state,attention=1.0,self_relevance=0.9,valence=0.4)
        reentry_off=r2.compute(
            {**PRESENT,"reward":0.1},runtime.state.self_state,
            attention=1.0,self_relevance=0.1,valence=0.0,reentry=False)

        cycle=bridge.integrate(frame,PRESENT,persist=True)
        restarted=ConsciousRuntime(
            "subjective-field-agent", root/"state.json",
            report_enabled=False, metacognition_enabled=False,
            self_observation_enabled=False,
        )
        restored=ConsciousFieldRuntime(restarted).snapshot()

        metrics={
            "objective_processing_unchanged": _objective(frame)==objective_baseline,
            "baseline_field_nonzero": baseline["unity"]>0.0 and baseline["strength"]>0.0,
            "integration_destroyed_binding": no_integration["binding"]==0.0 and no_integration["strength"]<baseline["strength"],
            "self_relevance_changes_subjective_strength": no_relevance["strength"]<baseline["strength"],
            "continuity_destroyed_temporal_contribution": continuity_on["continuity"]>continuity_off["continuity"],
            "reentry_changes_next_cycle": reentry_on["reentry"]>reentry_off["reentry"],
            "persistent_field_survives_restart": bool(restored) and restored.get("revision")==cycle["after"].get("revision"),
            "reentry_is_measured_without_report": cycle["after"]["reentry"]>=0.0,
        }
        result={
            "protocol":{
                "what_aspect":"unified present as world/self binding, relevance, valence, continuity and reentry",
                "causal_relation":"persistent runtime-owned field with next-cycle reentry",
                "destructive_test":"selective ablation with objective control invariant",
                "no_report":True,
                "phenomenal_consciousness_claim":False,
            },
            "baseline":baseline,
            "cycle":cycle,
            "restarted":restored,
            "ablations":{
                "integration":no_integration,"self_relevance":no_relevance,
                "continuity_enabled":continuity_on,"continuity_ablated":continuity_off,
                "reentry_enabled":reentry_on,"reentry_ablated":reentry_off,
            },
            "metrics":metrics,
            "interpretation":{
                "pass":all(metrics.values()),
                "meaning":"The SubjectiveField is persistent across the runtime boundary and retains a measurable reentry relation while objective candidate control remains invariant.",
            },
        }
        print(json.dumps(result,indent=2,sort_keys=True))
        if not all(metrics.values()):
            raise AssertionError(metrics)
        print("CONSCIOUS FIELD RUNTIME CAUSAL ATTACK v1: PASS")
        return result

if __name__=="__main__":
    run()
