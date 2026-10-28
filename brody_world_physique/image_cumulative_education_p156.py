"""P156 sequential education: gated vs ungated cumulative corrections.

Replay of previously mastered skills is required before every ACCEPT. Three
distinct RNG streams for feedback, validation and sealed final evaluation.
Curriculum remains synthetic and predefined; no native memory mutations.
"""
from __future__ import annotations
import argparse,json,random,time
from pathlib import Path
from .image_full_education_p154 import LAWS,WORLD
from .image_education_retention_gate_p155 import train,sample_error,mae

def curriculum():
    return [(law,world) for law in LAWS for world in WORLD]

def check(candidate, target_validation, replay, margin=.005, retention_tolerance=.035):
    old=mae(target_validation,0.0);new=mae(target_validation,candidate)
    if old is None or new is None:return False,"HOLD_MISSING_VALIDATION"
    if new>=old-margin:return False,"HOLD_NO_GAIN"
    for key,pairs,existing in replay:
        before=mae(pairs,existing);after=mae(pairs,existing+candidate)
        if before is None or after is None:return False,"HOLD_MISSING_REPLAY"
        if after>before+retention_tolerance:return False,"HOLD_FORGETTING"
    return True,"ACCEPT_GAIN_RETAINED"

def run(out,minutes=20,seed=156,lessons_each=24,feedback_each=24,validation_each=24,exam_each=50,
        retention_tolerance=.035):
    if not (3<=minutes<=90 and 8<=lessons_each<=200 and 8<=feedback_each<=200
            and 8<=validation_each<=200 and 20<=exam_each<=400 and 0<=retention_tolerance<=5):
        raise ValueError("INVALID_BOUNDS")
    dst=Path(out)
    if dst.exists():raise ValueError("PRESERVE_EVIDENCE")
    dst.mkdir(parents=True)
    start=time.monotonic();deadline=start+minutes*60
    train_rng=random.Random(seed+11);feedback_rng=random.Random(seed+22)
    val_rng=random.Random(seed+33);exam_rng=random.Random(seed+44)
    rules={law:train(law,train_rng,lessons_each) for law in LAWS}
    (dst/"FROZEN_BASE.json").write_text(json.dumps(rules,indent=2),encoding="utf8")
    # Persistent per-family correction: a new proposal is *cumulative*, so it
    # must not shift all earlier tasks harmfully. Ungated always accepts.
    gated={law:0. for law in LAWS};ungated={law:0. for law in LAWS}
    history=[];replay_bank={};stopped=False
    with (dst/"CYCLES.jsonl").open("w",encoding="utf8") as journal:
        for cycle,(law,world) in enumerate(curriculum(),1):
            if time.monotonic()>=deadline:stopped=True;break
            key=law+"/"+world
            feedback=sample_error(feedback_rng,law,world,rules[law],feedback_each)
            # For learned cumulative adjustment, propose residual on top of
            # current gated model, from distinct teaching examples.
            proposal=(sum(t-p-gated[law] for p,t in feedback)/len(feedback)) if feedback else 0.
            val=sample_error(val_rng,law,world,rules[law],validation_each)
            baseline_shift=gated[law]
            val_relative=[(p+baseline_shift,t) for p,t in val]
            replay=[(k,[(p+baseline_shift,t) for p,t in rows],0.)
                    for k,rows in replay_bank.items() if k.startswith(law+"/")]
            allow,reason=check(proposal,val_relative,replay,retention_tolerance=retention_tolerance)
            before_gated=gated[law];before_ungated=ungated[law]
            if allow:gated[law]+=proposal
            ungated[law]+=proposal
            # The replay bank is validation-only and accumulates earlier tasks.
            replay_bank[key]=sample_error(val_rng,law,world,rules[law],validation_each)
            h={"cycle":cycle,"task":key,"proposal":proposal,"accepted":allow,"reason":reason,
               "gated_before":before_gated,"gated_after":gated[law],
               "ungated_before":before_ungated,"ungated_after":ungated[law],
               "replayed_prior_skills":len(replay)}
            history.append(h);journal.write(json.dumps(h)+"\n")
    # New held-out set created after all choices. Test old and new on identical
    # unseen sequences; NO exam feedback drives any training decisions.
    scores={};n=0;total={"frozen":0.,"ungated":0.,"gated":0.}
    with (dst/"FINAL_EXAM.jsonl").open("w",encoding="utf8") as journal:
        for law,world in curriculum():
            key=law+"/"+world
            test=sample_error(exam_rng,law,world,rules[law],exam_each)
            if not test:continue
            b=mae(test);u=mae(test,ungated[law]);g=mae(test,gated[law])
            scores[key]={"n":len(test),"baseline_mae":b,"ungated_mae":u,"gated_mae":g,
                         "gated_vs_baseline_delta":g-b,"gated_vs_ungated_delta":g-u}
            for label,value in (("frozen",b),("ungated",u),("gated",g)):
                total[label]+=value*len(test)
            n+=len(test);journal.write(json.dumps({"task":key,**scores[key]})+"\n")
    report={"schema":"BRODY_P156_CUMULATIVE_EDUCATION",
      "cycles_completed":len(history),"cycles_expected":len(LAWS)*len(WORLD),
      "exam_cases":n,"exam_cells":len(scores),
      "duration_seconds":round(time.monotonic()-start,3),
      "stopped_by":"TIME_BUDGET" if stopped else "CURRICULUM_CAP",
      "decisions_accepted":sum(int(h["accepted"]) for h in history),
      "decisions_held":sum(int(not h["accepted"]) for h in history),
      "final_mean_error":{k:(v/n if n else None) for k,v in total.items()},
      "gated_memory":gated,"ungated_memory":ungated,"history":history,"per_task":scores,
      "read_only_from_native_memory":True,"learning_is_synthetic":True,
      "exam_selection_leakage":False,"full_curriculum_completed":not stopped,
      "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dst/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=20);p.add_argument("--seed",type=int,default=156)
    p.add_argument("--lessons-each",type=int,default=24)
    p.add_argument("--feedback-each",type=int,default=24)
    p.add_argument("--validation-each",type=int,default=24)
    p.add_argument("--exam-each",type=int,default=50)
    a=p.parse_args();r=run(a.out,a.minutes,a.seed,a.lessons_each,a.feedback_each,a.validation_each,a.exam_each)
    print(json.dumps({k:v for k,v in r.items() if k not in ("history","per_task")},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
