"""Restartable, bounded visual learning loop with local candidate skills.

Learns per-image *perceptual preprocessing* by supervised comparisons, not
semantic world concepts. Saves a verified local skill state, reuses it next
run, diagnoses failures and schedules more challenging lessons. Never touches
Obsidia native memory or kernel.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from pathlib import Path
from statistics import mean
from PIL import Image,ImageOps,ImageEnhance,ImageFilter
from .image_external_source_school_v0 import load_sources,reference
from .image_multidirection_stress_10k_v0 import AXES,perturb
from .drawing_school_v1 import suggest_gestures_from_reference
from .instrument_school_v2 import render_instrument,_gray_pixel_loss
from .fusion_f9_intensive_education_v0 import digest,verify_chain

STRATEGIES=("raw","invert","autocontrast","threshold","sharpen")
def vision(img,strategy):
    x=img.convert("L")
    if strategy=="invert":return ImageOps.invert(x)
    if strategy=="autocontrast":return ImageOps.autocontrast(x)
    if strategy=="threshold":return x.point(lambda v:0 if v<175 else 255)
    if strategy=="sharpen":return x.filter(ImageFilter.UnsharpMask(radius=1.5,percent=180,threshold=2))
    return x
def reconstruct(img,strategy):
    observed=vision(img,strategy)
    strokes=suggest_gestures_from_reference(observed)
    return (render_instrument(strokes,"PEN") if strokes else Image.new("L",(64,64),255)),len(strokes)
def decision(skills,source_key):
    means=skills.get(source_key,{})
    # Only successful previously trained configurations are reused;
    # unseen input uses raw; no access to current reference for selection.
    scored=[(v["sum"]/v["n"],s) for s,v in means.items() if v["n"]>0]
    return min(scored)[1] if scored else "raw"
def checksum_files(paths):
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
def load_state(path,manifest):
    if not path:return {"skills":{},"cycles":0,"manifest":manifest}
    s=json.loads(Path(path).read_text(encoding="utf-8"))
    sig=s.pop("digest",None)
    if sig!=digest(s) or s.get("schema")!="BRODY_LOCAL_CONTINUOUS_VISION_SKILLS_V0":
        raise ValueError("CANDIDATE_MEMORY_TAMPER")
    if s["manifest"]!=manifest:raise ValueError("SOURCE_MANIFEST_DRIFT")
    if s.get("native_memory_write") is not False or s.get("canonical_promotion") is not False:
        raise ValueError("FORBIDDEN_MEMORY_AUTHORITY")
    return s
def run(images,out,previous=None,episodes=1400,seed=20261010):
    if episodes<14 or episodes%14:raise ValueError("EPISODES_MULTIPLE_14")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EXISTING_EVIDENCE")
    files=load_sources(images)
    originals={p.name:reference(p) for p in files}
    manifest=checksum_files(files)
    state=load_state(previous,manifest)
    skills=state["skills"]
    rng=random.Random(seed+state["cycles"]*7919)
    # Fresh seeded cases, axes never given as input to choose(); each lesson
    # explores alternatives only after an initial candidate is committed.
    cases=list(AXES)*(episodes//14);rng.shuffle(cases)
    dest.mkdir(parents=True)
    items=[];prev_hash=None;failures={}
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i,axis in enumerate(cases,1):
            name=rng.choice(list(originals))
            target=perturb(originals[name],axis,random.Random(rng.getrandbits(63)))
            # Learned skill is source-specific, not hidden family-specific.
            learned=decision(skills,name)
            first,ntrace=reconstruct(target,learned)
            initial_sha=hashlib.sha256(first.tobytes()).hexdigest()
            initial_loss=_gray_pixel_loss(first,target)
            # Teacher reference is used for feedback AFTER sealed initial.
            alternatives={}
            for s in STRATEGIES:
                art,n=reconstruct(target,s)
                alternatives[s]=_gray_pixel_loss(art,target)
            best=min(STRATEGIES,key=lambda s:(alternatives[s],STRATEGIES.index(s)))
            new_loss=alternatives[best]
            # Track experience across episodes. No raw image storage/auto promotion.
            entry=skills.setdefault(name,{})
            for strategy,loss in alternatives.items():
                stat=entry.setdefault(strategy,{"sum":0.0,"n":0})
                stat["sum"]+=loss;stat["n"]+=1
            if initial_loss>20 or ntrace==0:
                failures[axis]=failures.get(axis,0)+1
            event={"index":i,"previous":prev_hash,"source_file":name,
                "source_sha256":manifest[name],"axis_evaluator_only":axis,
                "strategy_before_feedback":learned,"candidate_sha256":initial_sha,
                "before_loss":initial_loss,"best_supervised_strategy":best,
                "after_feedback_loss":new_loss,"candidate_improved":new_loss<initial_loss-1e-9,
                "feedback_cross_episode_update":True,"native_memory_write":False,
                "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
            event["digest"]=digest(event);prev_hash=event["digest"]
            f.write(json.dumps(event,sort_keys=True)+"\n");items.append(event)
    count,tip=verify_chain(dest/"receipts.jsonl")
    state={"schema":"BRODY_LOCAL_CONTINUOUS_VISION_SKILLS_V0",
           "skills":skills,"cycles":state["cycles"]+1,"manifest":manifest,
           "source_kind":"ARCHIVED_IMAGES_UNVERIFIED",
           "native_memory_write":False,"canonical_promotion":False,
           "decision_authority":"KX108_ONLY"}
    state["digest"]=digest(state)
    (dest/"candidate_skills.json").write_text(json.dumps(state,indent=2)+"\n")
    report={"schema":"BRODY_CONTINUOUS_VISUAL_LEARNING_CYCLE_V0",
       "episodes":count,"cycles_completed":state["cycles"],
       "source_images":len(files),"receipt_tip":tip,
       "initial_loss_mean":mean(x["before_loss"] for x in items),
       "supervised_best_loss_mean":mean(x["after_feedback_loss"] for x in items),
       "episodes_with_supervised_improvement":sum(x["candidate_improved"] for x in items),
       "difficulty_queue_failures":failures,
       "next_candidate_state":"candidate_skills.json",
       "cross_restart_state_supported":True,
       "next_cycle_adaptive_scheduler_implemented":False,
       "independent_heldout_transfer_proven":False,
       "source_discovery_external_implemented":False,
       "real_physics_proven":False,
       "native_memory_write":False,"canonical_promotion":False,
       "kernel_mutation":False,"decision_authority":"KX108_ONLY",
       "status":"LOCAL_RESTARTABLE_CONTINUOUS_CANDIDATE_LEARNING_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--images",required=True);p.add_argument("--out",required=True)
    p.add_argument("--previous");p.add_argument("--episodes",type=int,default=1400)
    a=p.parse_args()
    print(json.dumps(run(a.images,a.out,a.previous,a.episodes),indent=2))
if __name__=="__main__":main()
