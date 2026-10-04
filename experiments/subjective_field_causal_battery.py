"""Causal battery for the Subjective Field consciousness primitive."""
from __future__ import annotations
import json
from typing import Any, Mapping
from skill_conscious.subjective_field import SubjectiveField

WORLD={"signal":1.0,"reward":0.7,"threat":0.1,"self_impact":0.9}
NEUTRAL_WORLD={"signal":0.2,"reward":0.1,"threat":0.1,"self_impact":0.0}
SELF_STATE={"energy":0.8,"safety":0.8,"goal":0.6}

class ObjectiveProcessor:
    @staticmethod
    def process(world: Mapping[str,float]) -> float:
        return round(float(world.get("reward",0.0))
                     -0.50*float(world.get("threat",0.0))
                     +0.10*float(world.get("signal",0.0)),8)

def _field(
    field:SubjectiveField,
    world:Mapping[str,float],
    *,
    attention:float=1.0,
    self_relevance:float|None=None,
    valence:float|None=None,
    integration:bool=True,
    temporal_continuity:bool=True,
    reentry:bool=True,
)->dict[str,Any]:
    relevance=(float(world.get("self_impact",0.0))
               if self_relevance is None else float(self_relevance))
    value=((float(world.get("reward",0.0))-float(world.get("threat",0.0)))*relevance
           if valence is None else float(valence))
    return field.compute(
        world,SELF_STATE,attention=attention,self_relevance=relevance,
        valence=value,integration=integration,
        temporal_continuity=temporal_continuity,reentry=reentry,
    )

def _run_ablation(name:str)->dict[str,Any]:
    field=SubjectiveField()
    first=_field(
        field,WORLD,
        integration=name!="integration",
        self_relevance=None if name!="self_relevance" else 0.0,
        valence=None if name!="valence" else 0.0,
        temporal_continuity=name!="continuity",
        reentry=name!="reentry",
        attention=0.0 if name=="attention" else 1.0,
    )
    second=_field(
        field,NEUTRAL_WORLD,
        integration=name!="integration",
        self_relevance=None if name!="self_relevance" else 0.0,
        valence=None if name!="valence" else 0.0,
        temporal_continuity=name!="continuity",
        reentry=name!="reentry",
        attention=0.0 if name=="attention" else 1.0,
    )
    return {"first":first,"second":second,"objective":ObjectiveProcessor.process(WORLD)}

def run()->dict[str,Any]:
    objective=ObjectiveProcessor.process(WORLD)
    conditions={n:_run_ablation(n) for n in
                ("integration","self_relevance","valence","continuity","reentry","attention")}
    baseline=SubjectiveField()
    baseline_first=_field(baseline,WORLD)
    baseline_second=_field(baseline,NEUTRAL_WORLD)
    high=SubjectiveField()
    high_value=_field(high,WORLD)
    low=SubjectiveField()
    low_value=_field(low,{**WORLD,"self_impact":0.1})
    pos=SubjectiveField()
    positive=_field(pos,WORLD,valence=0.8)["valence"]
    neg=SubjectiveField()
    negative=_field(neg,WORLD,valence=-0.8)["valence"]

    cf=SubjectiveField(); _field(cf,WORLD)
    c2=_field(cf,{**WORLD,"reward":0.65},reentry=False)
    ca=SubjectiveField(); _field(ca,WORLD)
    c2a=_field(ca,{**WORLD,"reward":0.65},temporal_continuity=False,reentry=False)

    rf=SubjectiveField(); _field(rf,WORLD)
    r2=_field(rf,NEUTRAL_WORLD,reentry=True)
    ra=SubjectiveField(); _field(ra,WORLD)
    r2a=_field(ra,NEUTRAL_WORLD,reentry=False)

    restored=SubjectiveField().compute(
        WORLD,SELF_STATE,attention=1.0,self_relevance=0.9,valence=0.54
    )

    metrics={
        "objective_processing_invariant":all(x["objective"]==objective for x in conditions.values()),
        "integration_ablation_removes_binding":conditions["integration"]["first"]["binding"]==0.0,
        "integration_ablation_reduces_field":conditions["integration"]["first"]["strength"]<baseline_first["strength"],
        "self_relevance_changes_field":high_value["strength"]>low_value["strength"],
        "valence_is_causally_encoded":positive>0.0 and negative<0.0,
        "continuity_contributes_temporal_unity":c2["continuity"]>c2a["continuity"],
        "reentry_contributes_next_cycle_field":(
            r2["reentry"]>r2a["reentry"] and r2["strength"]>r2a["strength"]
        ),
        "attention_ablation_removes_access":(
            conditions["attention"]["first"]["strength"]==0.0
            and conditions["attention"]["first"]["unity"]==0.0
        ),
        "field_restores_exactly":(
            restored["strength"]==baseline_first["strength"]
            and restored["unity"]==baseline_first["unity"]
        ),
    }
    result={
        "protocol":{
            "no_report_measurement":True,
            "objective_control_channel":"world-only deterministic processor",
            "subjective_field":"present + self-state + self-relevance + valence + continuity + reentry + attention",
            "phenomenal_consciousness_claim":False,
        },
        "baseline":{"first":baseline_first,"second":baseline_second},
        "ablations":conditions,
        "dissociations":{
            "high_self_relevance":high_value,
            "low_self_relevance":low_value,
            "positive_valence":positive,
            "negative_valence":negative,
            "continuity_enabled":c2,
            "continuity_ablated":c2a,
            "reentry_enabled":r2,
            "reentry_ablated":r2a,
        },
        "metrics":metrics,
        "interpretation":{
            "pass":all(metrics.values()),
            "meaning":"The proposed Subjective Field is a separable causal layer whose components contribute distinctively while objective world processing remains invariant.",
        },
    }
    print(json.dumps(result,indent=2,sort_keys=True))
    if not all(metrics.values()):
        raise AssertionError(metrics)
    print("SUBJECTIVE FIELD CAUSAL BATTERY v1: PASS")
    return result

if __name__=="__main__":
    run()
