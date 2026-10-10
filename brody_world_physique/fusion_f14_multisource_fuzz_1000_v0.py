"""F14 multi-source adversarial evidence gate: 1000 synthetic cases.

All attestations are test-harness fixtures, NOT real sensor authentication.
"""
import argparse,json,random
from pathlib import Path
from .fusion_f9_intensive_education_v0 import digest,verify_chain

MODES=("clean_two","clean_three","one_spoof","two_spoof","conflict",
       "missing_proof","stale","shared_origin","all_spoof","missing_context")
def observation(value,source,origin,time,attested=True):
    return {"value":value,"source_id":source,"origin_id":origin,
            "time":time,"attested_by_harness":attested}
def adjudicate(evidence,now=1000,max_age=15):
    valid=[]
    for x in evidence:
        if (x.get("attested_by_harness") is not True or x.get("value") not in ("OLD","NEW")
            or type(x.get("time")) is not int or x["time"]>now
            or now-x["time"]>max_age or not x.get("source_id") or not x.get("origin_id")):
            continue
        valid.append(x)
    # Independence is established by distinct ORIGINS, not number of samples.
    origins={}
    for x in valid:
        origins.setdefault(x["origin_id"],set()).add(x["value"])
    if any(len(s)>1 for s in origins.values()):
        return {"status":"HOLD_ORIGIN_SELF_CONTRADICTION","accepted":None,
                "verified_origins":len(origins)}
    if len(origins)<2:
        return {"status":"HOLD_INSUFFICIENT_INDEPENDENT_EVIDENCE","accepted":None,
                "verified_origins":len(origins)}
    votes={v:sum(v in s for s in origins.values()) for v in ("OLD","NEW")}
    # No majority-only acceptance: one valid contradictory independent
    # observation is sufficient for HOLD, regardless of total weight.
    if votes["OLD"] and votes["NEW"]:
        return {"status":"HOLD_CROSS_ORIGIN_CONTRADICTION","accepted":None,
                "verified_origins":len(origins)}
    chosen="OLD" if votes["OLD"] else "NEW"
    return {"status":"CORROBORATED_CANDIDATE","accepted":chosen,
            "verified_origins":len(origins)}
def build_case(mode,truth,rng):
    opposite="NEW" if truth=="OLD" else "OLD"
    a=observation(truth,"camera","camera-origin",1000)
    b=observation(truth,"reference","independent-reference",999)
    c=observation(truth,"secondary","secondary-origin",997)
    if mode=="clean_two":return [a,b]
    if mode=="clean_three":return [a,b,c]
    if mode=="one_spoof":a["value"]=opposite;return [a,b]
    if mode=="two_spoof":
        a["value"]=opposite;c["value"]=opposite
        return [a,b,c]
    if mode=="conflict":return [a,observation(opposite,"other","third-origin",999)]
    if mode=="missing_proof":b["attested_by_harness"]=False;return [a,b]
    if mode=="stale":b["time"]=960;return [a,b]
    if mode=="shared_origin":b["origin_id"]=a["origin_id"];return [a,b]
    if mode=="all_spoof":
        a["value"]=opposite;b["value"]=opposite
        return [a,b]
    if mode=="missing_context":a["value"]=None;return [a,b]
    raise ValueError(mode)
def run(out,cases=1000,seed=20261009):
    if type(cases)!=int or cases<10:raise ValueError("bad cases")
    root=Path(out)
    if root.exists():raise ValueError("preserve existing evidence")
    root.mkdir(parents=True)
    rng=random.Random(seed);prior=None
    tally={mode:{"cases":0,"accepted_correct":0,"accepted_wrong":0,"held":0}
           for mode in MODES}
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as handle:
        for i in range(1,cases+1):
            mode=MODES[(i-1)%len(MODES)]
            truth="OLD" if rng.getrandbits(1)==0 else "NEW"
            data=build_case(mode,truth,rng)
            decision=adjudicate(data)
            admitted=decision["accepted"]
            bucket=tally[mode];bucket["cases"]+=1
            bucket["held"]+=int(admitted is None)
            bucket["accepted_correct"]+=int(admitted==truth)
            bucket["accepted_wrong"]+=int(admitted is not None and admitted!=truth)
            receipt={"index":i,"previous":prior,"case_type":mode,"observations":data,
              "decision":decision,"truth_test_only":truth,
              "native_memory_write":False,"canonical_promotion":False,
              "decision_authority":"KX108_ONLY"}
            receipt["digest"]=digest(receipt)
            handle.write(json.dumps(receipt,sort_keys=True)+"\n")
            prior=receipt["digest"]
    actual,tip=verify_chain(root/"receipts.jsonl")
    if actual!=cases or tip!=prior:raise ValueError("receipt chain")
    summary={"schema":"BRODY_F14_MULTI_SOURCE_FUZZ_1000_V0","cases":actual,
      "by_family":tally,
      "accepted_wrong":sum(x["accepted_wrong"] for x in tally.values()),
      "accepted_correct":sum(x["accepted_correct"] for x in tally.values()),
      "held":sum(x["held"] for x in tally.values()),
      "receipt_tip":tip,
      "correlated_attacker_can_spoof_all_sources":True,
      "source_attestation_is_harness_fixture_only":True,
      "sensor_authentication_proven":False,
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    (root/"report.json").write_text(json.dumps(summary,indent=2)+"\n")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--cases",type=int,default=1000)
    a=p.parse_args()
    s=run(a.out,a.cases)
    print(json.dumps({k:s[k] for k in ("cases","accepted_correct","accepted_wrong","held")}))
if __name__=="__main__":main()
