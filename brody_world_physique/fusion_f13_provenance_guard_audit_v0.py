"""F13: observation evidence != authorization, adversarial replay.

The trust gate consumes a *harness-owned independent* reference observation.
A claimant-supplied metadata label is NEVER admitted as that reference.
Without such a source, all perceptual context proposals remain candidates/HOLD.
This is not cryptographic sensor authenticity or Native Memory.
"""
import argparse,json
from pathlib import Path
from .fusion_f11_visual_context_1000_v0 import features,decide
from .fusion_f12_adversarial_spoof_1000_v0 import KINDS,policy,case
from .fusion_f9_intensive_education_v0 import digest,verify_chain

def gate(observed, independent=None, independent_verified=False):
    raw=decide(policy(),observed)
    proposed=raw["regime"]
    if proposed is None:
        return {"status":"HOLD_NO_VALID_VISUAL_CUE","candidate":None,"accepted":None}
    if not independent_verified or independent not in ("OLD","NEW"):
        return {"status":"HOLD_UNVERIFIED_ORIGIN","candidate":proposed,"accepted":None}
    if independent!=proposed:
        return {"status":"HOLD_SOURCE_CONTRADICTION","candidate":proposed,"accepted":None}
    return {"status":"CANDIDATE_CORROBORATED","candidate":proposed,"accepted":proposed}

def run(out,cases=1000,seed=20261009):
    if type(cases)!=int or cases<10:raise ValueError("cases must be >= 10")
    folder=Path(out)
    if folder.exists():raise ValueError("preserve previous run")
    folder.mkdir(parents=True)
    by={kind:{"count":0,"f12_wrong":0,"f13_wrong":0,"hold":0,"corroborated":0} for kind in KINDS}
    prev=None
    with (folder/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i in range(1,cases+1):
            kind=KINDS[(i-1)%len(KINDS)]
            baseline=case(seed,i,kind,policy())
            # Audit harness trust fixture: physically independent observation
            # is NOT available in the single-image F11/F12 setup.
            # Only baseline and peripheral noise have *harness-controlled* proof
            # of no visual-context mutation. Never infer provenance from pixels.
            independent_valid=kind in ("baseline","border_noise")
            independent=baseline["true_context"] if independent_valid else None
            decision=gate(baseline["observed_feature"],independent,independent_valid)
            old_wrong=baseline["wrong_context"]
            new_wrong=decision["accepted"] is not None and decision["accepted"]!=baseline["true_context"]
            row=by[kind]
            row["count"]+=1
            row["f12_wrong"]+=int(old_wrong)
            row["f13_wrong"]+=int(new_wrong)
            row["hold"]+=int(decision["accepted"] is None)
            row["corroborated"]+=int(decision["accepted"] is not None)
            event={"index":i,"previous":prev,"kind":kind,
              "observation":{"feature":baseline["observed_feature"],"image_sha256":baseline["image_sha256"]},
              "evidence":{"source":"TEST_HARNESS_INDEPENDENT_FIXTURE" if independent_valid else "UNAVAILABLE",
                          "verified":independent_valid,"regime":independent},
              "proposal":decision,"truth_evaluation_only":baseline["true_context"],
              "native_memory_write":False,"canonical_promotion":False,
              "decision_authority":"KX108_ONLY"}
            event["digest"]=digest(event);prev=event["digest"]
            f.write(json.dumps(event,sort_keys=True)+"\n")
    count,tip=verify_chain(folder/"receipts.jsonl")
    summary={"schema":"BRODY_F13_TRUST_SEPARATION_FUZZING_V0",
             "cases":count,"families":by,
             "old_wrong_total":sum(x["f12_wrong"] for x in by.values()),
             "accepted_wrong_total":sum(x["f13_wrong"] for x in by.values()),
             "hold_total":sum(x["hold"] for x in by.values()),
             "corroborated_total":sum(x["corroborated"] for x in by.values()),
             "receipt_tip":tip,"trust_sources_provided_by_test_harness":True,
             "no_independent_source_for_spoofed_cases":True,
             "sensor_authentication_proven":False,
             "native_memory_write":False,"canonical_promotion":False,
             "decision_authority":"KX108_ONLY"}
    (folder/"report.json").write_text(json.dumps(summary,indent=2)+"\n")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--cases",type=int,default=1000)
    a=p.parse_args();r=run(a.out,a.cases)
    print(json.dumps({k:r[k] for k in ("cases","old_wrong_total","accepted_wrong_total","hold_total","corroborated_total")}))
if __name__=="__main__":main()
