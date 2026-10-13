"""P2.8c: guarded change detection on the SAME rendered pixel scenes as P2.8b.

Ablation isolates epistemic gate. No simulator truth is visible before inference.
Delayed supervised verification is disclosed. NO B8 promotion or memory writes.
"""
from __future__ import annotations
import argparse
import json
from hashlib import sha256
from pathlib import Path
from statistics import median, mean
from collections import deque

from . import p28b_pixel_reversal_v0 as prior

ARMS = ("fixed_history", "observed_majority", "p28b_revisable", "p28c_guarded")
SCHEMA = "BRODY_P28C_GUARDED_PIXEL_REVERSAL_V0"


class GuardedBelief:
    def __init__(self, window=8, tolerance=2):
        if window < 3:
            raise ValueError("window")
        self.window = window
        self.tolerance = tolerance
        self.samples = deque(maxlen=window)
        self.groups = set()

    def feedback(self, group, shifts, camera):
        if group in self.groups:
            return False
        self.groups.add(group)
        self.samples.append(tuple(abs(x-camera) for x in shifts))
        return True

    def ranking(self):
        if len(self.samples) < 2:
            return []
        return sorted((median(row[i] for row in self.samples), i) for i in range(5))

    def predict(self, observed):
        if observed is None:
            return None, "HOLD_PIXELS"
        ranks = self.ranking()
        if not ranks:
            return None, "HOLD_NO_VERIFIED_FEEDBACK"
        best_error, best_id = ranks[0]
        # Unreliable candidate in current evidence: do not just prefer
        # a historical source if its recent error is high.
        if best_error > self.tolerance:
            return None, "HOLD_UNRELIABLE_HISTORY"
        candidates = [i for err,i in ranks if err <= best_error+0.5
                      and err <= self.tolerance]
        vals = [observed["shifts"][i] for i in candidates]
        if max(vals)-min(vals) > 2:
            return None, "HOLD_DIVERGENT_HISTORIES"
        return observed["apparent"]-median(vals), "PREDICT_RECENT_VERIFIED_REPERE"


def execute(count=180, delay=2, window=8):
    if not 100 <= count <= 2000 or not 1 <= delay <= 10:
        raise ValueError("count/delay")
    old = prior.WorkingKnowledge()
    guard = GuardedBelief(window)
    pending = deque()
    receipts = []
    rows = []
    for i in range(count):
        s = prior.fixture(i)
        obs, observation_state = prior.observe(s)
        if obs is None:
            prior_pred = {x: None for x in ("fixed_history","observed_majority","scoped_revisable")}
            result, reason = None, observation_state
        else:
            prior_pred = prior.decide(obs, old)["predictions"]
            result, reason = guard.predict(obs)
        predictions = {"fixed_history":prior_pred["fixed_history"],
                       "observed_majority":prior_pred["observed_majority"],
                       "p28b_revisable":prior_pred["scoped_revisable"],
                       "p28c_guarded":result}
        receipts.append({"id":i, "observation":obs, "prediction":predictions,
                         "p28c_reason":reason, "observed_state":observation_state,
                         "seen_verified_groups":len(guard.groups),
                         "latest_verified_anchor":guard.ranking()[0][1] if guard.ranking() else None,
                         "memory_write":False, "decision_authority":"KX108_ONLY"})
        # This scoring uses truth only after predictions were committed to
        # a Python list. The saved receipt is sealed at end, not online.
        rows.append({"id":i,"regime":s["regime"],"observation_state":observation_state,
                     "errors":{arm:abs(v-s["world"]) if v is not None else None
                               for arm,v in predictions.items()}})
        pending.append((s,obs))
        if len(pending)>=delay:
            past, measured = pending.popleft()
            if past["feedback_available"] and measured is not None:
                group="pair-"+str(past["id"])
                guard.feedback(group,measured["shifts"],past["camera"])
                old.apply_feedback(episode_id=past["id"],group_id=group,
                                   observed_shifts=measured["shifts"],
                                   verified_camera=past["camera"])
    summary={}
    for arm in ARMS:
        good=[r["errors"][arm] for r in rows if r["errors"][arm] is not None]
        summary[arm]={"evaluated":len(good),"coverage":len(good)/count,
                      "mae_accepted_px":mean(good) if good else None,
                      "catastrophic_over_10px":sum(x>10 for x in good)}
    matched=[r for r in rows if r["errors"]["p28b_revisable"] is not None
             and r["errors"]["p28c_guarded"] is not None]
    return {"schema":SCHEMA,"count":count,"delay":delay,"window":window,
            "source_kind":"SYNTHETIC_RENDERED_PIXELS_SUPERVISED",
            "summary":summary, "matched_b_c_n":len(matched),
            "matched_b_mae":mean(r["errors"]["p28b_revisable"] for r in matched) if matched else None,
            "matched_c_mae":mean(r["errors"]["p28c_guarded"] for r in matched) if matched else None,
            "unseen_regime":False,"autonomous_learning":False,
            "pixels_detected_using_engineered_colors":True,
            "native_memory_write":False,"b8_promotion":False,
            "decision_authority":"KX108_ONLY",
            "predictions_pre_feedback":receipts,"rows":rows,
            "verdict":"DIAGNOSTIC_ONLY"}


def canonical(item):
    return (json.dumps(item,sort_keys=True,separators=(",",":"))+"\n").encode()


def run(out,count=180,delay=2,window=8):
    out=Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("output path nonempty")
    r=execute(count,delay,window)
    out.mkdir(parents=True,exist_ok=True)
    receipts=canonical(r["predictions_pre_feedback"])
    (out/"predictions_pre_feedback.json").write_bytes(receipts)
    r["precommit_sha256"]=sha256(receipts).hexdigest()
    (out/"evaluation.json").write_bytes(canonical(r))
    return r


def verify(out):
    out=Path(out)
    saved=json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    pre=(out/"predictions_pre_feedback.json").read_bytes()
    if sha256(pre).hexdigest()!=saved["precommit_sha256"]:
        raise ValueError("altered receipt")
    replay=execute(saved["count"],saved["delay"],saved["window"])
    replay["precommit_sha256"]=saved["precommit_sha256"]
    if canonical(replay)!=canonical(saved) or canonical(replay["predictions_pre_feedback"])!=pre:
        raise ValueError("deterministic replay mismatch")
    return True


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",required=True)
    a.add_argument("--count",type=int,default=180)
    a.add_argument("--delay",type=int,default=2)
    a.add_argument("--window",type=int,default=8)
    a.add_argument("--verify",action="store_true")
    args=a.parse_args()
    if args.verify:
        print(json.dumps({"verified":verify(args.out)}))
    else:
        r=run(args.out,args.count,args.delay,args.window)
        print(json.dumps({k:r[k] for k in
            ("summary","matched_b_c_n","matched_b_mae","matched_c_mae")}))
if __name__=="__main__":
    main()
