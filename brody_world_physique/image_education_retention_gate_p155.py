"""P155: gate every proposed educational correction on untouched validation.

A teacher may propose a per-world residual. The student must choose ACCEPT or
HOLD from separate validation sequences, while enforcing a clean-world
retention guard. The final exam is never used for selection.

Synthetic one-dimensional pixel trajectories; educational-method prototype,
NOT autonomous discovery of physical laws.
"""
from __future__ import annotations
import argparse,json,random,time
from pathlib import Path
from .image_full_education_p154 import LAWS,WORLD,simulate,observations,infer_rule,forecast

def sample_error(rng,law,world,rule,n):
    data=[]
    for _ in range(n):
        frames,truth=simulate(rng,law,world)
        xs=observations(frames[:6],world)
        guess=forecast(xs,rule)
        if guess is not None:
            data.append((guess,truth[6]))
        for im in frames:im.close()
    return data

def mae(pairs,shift=0.0):
    return sum(abs(p+shift-t) for p,t in pairs)/len(pairs) if pairs else None

def train(law,rng,count):
    lessons=[]
    for _ in range(count):
        frames,_=simulate(rng,law,"clean")
        lessons.append(observations(frames[:5],"clean"))
        for im in frames:im.close()
    return infer_rule(lessons)

def choose(candidate,validation,clean_validation,tolerance=0.03):
    old=mae(validation);new=mae(validation,candidate)
    clean_old=mae(clean_validation);clean_new=mae(clean_validation,candidate)
    if old is None or new is None or clean_old is None or clean_new is None:
        return False,"HOLD_INSUFFICIENT_VISIBILITY"
    if new>=old-0.005:return False,"HOLD_NO_VALIDATED_GAIN"
    if clean_new>clean_old+tolerance:return False,"HOLD_RETENTION_REGRESSION"
    return True,"ACCEPT_VALIDATED_CORRECTION"

def run(out,minutes=20,seed=155,lessons_each=32,feedback_each=24,
        validation_each=32,exam_each=80,tolerance=0.03):
    if not (3<=minutes<=90 and 8<=lessons_each<=200 and 8<=feedback_each<=200
            and 8<=validation_each<=400 and 20<=exam_each<=1000 and 0<=tolerance<=3):
        raise ValueError("INVALID_BOUNDS")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    st=time.monotonic();deadline=st+60*minutes
    lesson_rng=random.Random(seed+1);feedback_rng=random.Random(seed+2)
    validation_rng=random.Random(seed+3);exam_rng=random.Random(seed+4)
    rules={law:train(law,lesson_rng,lessons_each) for law in LAWS}
    (root/"FROZEN_RULES.json").write_text(json.dumps(rules,indent=2),encoding="utf8")
    decisions={};final={};stop=False
    # Explicit independent clean retention batch for each law, shared by
    # all condition-specific candidate interventions within that law.
    with (root/"EXAM.jsonl").open("w",encoding="utf8") as log:
        for law in LAWS:
            clean_holdout=sample_error(validation_rng,law,"clean",rules[law],validation_each)
            for world in WORLD:
                if time.monotonic()>=deadline:stop=True;break
                feedback=sample_error(feedback_rng,law,world,rules[law],feedback_each)
                residual=sum(t-p for p,t in feedback)/len(feedback) if feedback else 0.
                val=sample_error(validation_rng,law,world,rules[law],validation_each)
                ok,reason=choose(residual,val,clean_holdout,tolerance)
                shift=residual if ok else 0.
                key=law+"/"+world
                decisions[key]={"proposed_shift":round(residual,6),"accepted":ok,"reason":reason,
                    "validation_before":mae(val),"validation_candidate":mae(val,residual),
                    "retention_before":mae(clean_holdout),"retention_candidate":mae(clean_holdout,residual),
                    "applied_shift":round(shift,6)}
                # Independent blind examination, after decision locked.
                exams=sample_error(exam_rng,law,world,rules[law],exam_each)
                before=mae(exams);after=mae(exams,shift);ungated=mae(exams,residual)
                final[key]={"n":len(exams),"exam_baseline_mae":before,
                    "exam_proposal_ungated_mae":ungated,"exam_gated_mae":after,
                    "regression_prevented":bool(not ok and ungated is not None and before is not None and ungated>before),
                    "accepted":ok}
                log.write(json.dumps({"case":key,**decisions[key],**final[key]})+"\n")
            if stop:break
    (root/"DECISIONS.json").write_text(json.dumps(decisions,indent=2),encoding="utf8")
    aggregate={"total_exam":sum(x["n"] for x in final.values()),
      "decisions_accepted":sum(int(v["accepted"]) for v in decisions.values()),
      "decisions_rejected":sum(int(not v["accepted"]) for v in decisions.values()),
      "prevented_regressions":sum(int(x["regression_prevented"]) for x in final.values()),
      "baseline_mae":sum(v["exam_baseline_mae"]*v["n"] for v in final.values() if v["exam_baseline_mae"] is not None)/max(1,sum(v["n"] for v in final.values())),
      "gated_mae":sum(v["exam_gated_mae"]*v["n"] for v in final.values() if v["exam_gated_mae"] is not None)/max(1,sum(v["n"] for v in final.values())),
      "ungated_mae":sum(v["exam_proposal_ungated_mae"]*v["n"] for v in final.values() if v["exam_proposal_ungated_mae"] is not None)/max(1,sum(v["n"] for v in final.values()))}
    report={"schema":"BRODY_P155_EDUCATION_RETENTION_GATE",
      "exam_cells_completed":len(final),"exam_cells_expected":len(LAWS)*len(WORLD),
      "duration_seconds":round(time.monotonic()-st,3),
      "stopped_by":"TIME_BUDGET" if stop else "EXAM_CAP",
      "aggregate":aggregate,"decisions":decisions,"exam":final,
      "independent_training_feedback_validation_exam_rng":True,
      "exam_used_for_selection":False,"acceptance_guard_uses_validation_only":True,
      "no_physics_autonomy_claim":True,"real_world_transfer_proven":False,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20)
    p.add_argument("--seed",type=int,default=155)
    p.add_argument("--lessons-each",type=int,default=32)
    p.add_argument("--feedback-each",type=int,default=24)
    p.add_argument("--validation-each",type=int,default=32)
    p.add_argument("--exam-each",type=int,default=80)
    p.add_argument("--tolerance",type=float,default=.03)
    args=p.parse_args()
    report=run(args.out,args.minutes,args.seed,args.lessons_each,
               args.feedback_each,args.validation_each,args.exam_each,args.tolerance)
    print(json.dumps({k:v for k,v in report.items() if k not in ("decisions","exam")},indent=2))
    print("Report:",str(Path(args.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
