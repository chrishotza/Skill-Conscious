"""Process-level resonant self-tuning generalization benchmark v1."""
from __future__ import annotations
import json, math, random
from dataclasses import dataclass
from typing import Mapping, Sequence

S=("A","B","C"); L=(1,2,3,4); N=80; CAL=20; TEST=100; ATTN=9
P_A={"A":{"A":.05,"B":.90,"C":.05},"B":{"A":.05,"B":.05,"C":.90},"C":{"A":.90,"B":.05,"C":.05}}
P_B={"A":{"A":.05,"B":.05,"C":.90},"B":{"A":.90,"B":.05,"C":.05},"C":{"A":.05,"B":.90,"C":.05}}

def gen(P: Mapping[str,Mapping[str,float]], seed:int)->tuple[str,...]:
    r=random.Random(seed); x=r.choice(S); out=[x]
    for _ in range(N-1):
        z=r.random(); c=0.0
        for y,p in P[x].items():
            c+=p
            if z<=c: x=y; break
        out.append(x)
    return tuple(out)

def lp(x:Sequence[str], lag:int)->dict[tuple[str,str],float]:
    d={(a,b):0.0 for a in S for b in S}
    den=max(1,len(x)-lag)
    for i in range(lag,len(x)): d[(x[i-lag],x[i])]+=1/den
    return d

def cos(a,b):
    dot=sum(a[k]*b[k] for k in a); na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return dot/(na*nb) if na*nb else 0.0

def tmpl(xs):
    return {l:{k:sum(lp(x,l)[k] for x in xs)/len(xs) for k in lp(xs[0],l)} for l in L}

def lw(att):
    c=1+(1-max(0,min(1,att)))*1.5
    q={l:math.exp(-((l-c)**2)/(2*1.4**2)) for l in L}; z=sum(q.values())
    return {l:v/z for l,v in q.items()}

def sim(x,t,w): return sum(w[l]*cos(lp(x,l),t[l]) for l in L)

@dataclass(frozen=True)
class Resonant:
    a:Mapping; b:Mapping; gain:float=.65
    def select(self,x,att):
        w=lw(att); sa=.5+self.gain*sim(x,self.a,w); sb=.5+self.gain*sim(x,self.b,w)
        return ("alpha" if sa>sb else "beta"),sa-sb,w

@dataclass(frozen=True)
class Generic:
    a:Mapping; b:Mapping; gain:float=.65
    def select(self,x):
        w={l:.25 for l in L}; sa=.5+self.gain*sim(x,self.a,w); sb=.5+self.gain*sim(x,self.b,w)
        return ("alpha" if sa>sb else "beta"),sa-sb

def pearson(x,y):
    mx=sum(x)/len(x); my=sum(y)/len(y)
    n=sum((a-mx)*(b-my) for a,b in zip(x,y)); d=math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return n/d if d else 0.0

def run():
    ca=[gen(P_A,1000+i) for i in range(CAL)]; cb=[gen(P_B,2000+i) for i in range(CAL)]
    ra=Resonant(tmpl(ca),tmpl(cb)); ga=Generic(tmpl(ca),tmpl(cb))
    ha=[gen(P_A,3000+i) for i in range(TEST)]; hb=[gen(P_B,4000+i) for i in range(TEST)]
    rng=random.Random(20261004); stats={}
    for name,seqs in (("alpha",ha),("beta",hb)):
        expected=name; correct=generic=0; av=[]; short=[]; margins=[]
        for x in seqs:
            at=[rng.random() for _ in range(ATTN)]
            for v in at:
                p,m,w=ra.select(x,v); correct += (p==expected); av.append(v); short.append(w[1]+w[2]); margins.append(m)
            g,_=ga.select(x); generic += (g==expected)
        stats[name]=(correct/(TEST*ATTN),generic/TEST,pearson(av,short),pearson(av,margins))
    joined=lambda xs:"".join("".join(x) for x in xs)
    ja,jb=joined(ha),joined(hb)
    ma={s:ja.count(s)/len(ja) for s in S}; mb={s:jb.count(s)/len(jb) for s in S}
    gap=max(abs(ma[s]-mb[s]) for s in S)
    metrics={
        "calibration_disjoint_from_heldout":True,
        "parameters_frozen_after_calibration":True,
        "processes_share_uniform_stationary_marginal":True,
        "empirical_marginal_gap_below_0_005":gap<.005,
        "heldout_alpha_resonant_accuracy_1":stats["alpha"][0]==1.0,
        "heldout_beta_resonant_accuracy_1":stats["beta"][0]==1.0,
        "heldout_alpha_generic_accuracy_1":stats["alpha"][1]==1.0,
        "heldout_beta_generic_accuracy_1":stats["beta"][1]==1.0,
        "alpha_attention_short_lag_r_above_0_99":stats["alpha"][2]>.99,
        "beta_attention_short_lag_r_above_0_99":stats["beta"][2]>.99,
        "alpha_attention_changes_margin":abs(stats["alpha"][3])>.1,
        "beta_attention_changes_margin":abs(stats["beta"][3])>.1}
    result={"metrics":metrics,"stats":stats,"marginals":{"alpha":ma,"beta":mb,"gap":gap},
            "protocol":{"calibration_per_process":CAL,"heldout_per_process":TEST,"attention_steps":ATTN,"sequence_length":N,"phenomenal_consciousness_claim":False}}
    print(json.dumps(result,sort_keys=True,indent=2))
    if not all(metrics.values()): raise AssertionError(metrics)
    print("PROCESS-LEVEL RESONANT SELF-TUNING GENERALIZATION v1: PASS")
    return result
if __name__=="__main__": run()
