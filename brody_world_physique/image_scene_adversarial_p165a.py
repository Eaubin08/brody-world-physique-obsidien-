"""P165-A: adversarial scene fixtures and observation/identity impossibility gates.
An EXAM harness, not a repaired learner. No canonical Obsidia writes.
"""
import argparse,hashlib,json,random,time
from pathlib import Path
from PIL import Image,ImageDraw
from .image_hard_visual_ood_p161 import STYLES,TEST_LAWS,positions,draw_frames
from .image_identity_occlusion_p164 import track,decision
from .image_camera_occlusion_gate_p163 import annotate_fiducials,camera_evidence

W,H=168,96
CASES=("color_swap","crossing_indistinguishable","occluded_jump",
       "camera_without_landmarks","multiple_depth_planes","substitution")
def make_case(kind,seed):
    rng=random.Random(seed);imlist=[]
    # Two entities are initially separate. Their simulator IDs are hidden
    # from inference and used solely by the evaluation oracle.
    a=[32+4*t for t in range(7)];b=[91-4*t for t in range(7)]
    unknown_identity=kind in ("crossing_indistinguishable","substitution")
    world={"A":a[:],"B":b[:],"case":kind,
           "identity_identifiable":not unknown_identity,
           "camera_identifiable":kind!="camera_without_landmarks"}
    for t in range(7):
        im=Image.new("RGB",(W,H),(237,232,221));d=ImageDraw.Draw(im)
        if kind=="multiple_depth_planes":
            d.rectangle((0,58,W,95),fill=(178,190,171))
            d.rectangle((0,27,W,38),fill=(122,146,160))
        shift=2*t if kind in ("camera_without_landmarks","multiple_depth_planes") else 0
        xa=a[t]+shift;xb=b[t]+shift
        if kind=="occluded_jump" and t>=5:xa+=14
        if kind=="substitution" and t>=4:xa,xb=xb,xa
        if kind=="camera_without_landmarks":
            # No visual cues of camera state, so camera/object movement
            # cannot be uniquely distinguished.
            pass
        elif kind=="multiple_depth_planes":
            for cx in (14,92,144):
                d.rectangle((cx+shift-1,11,cx+shift+1,15),fill=(54,190,65))
        fill_a=(220,45,55)
        if kind=="color_swap" and t>=3:fill_a=(35,139,208)
        for x,fill in ((xa,fill_a),(xb,(220,45,55))):
            d.ellipse((int(x)-5,43,int(x)+5,53),fill=fill)
        if kind in ("occluded_jump","substitution") and t in (3,4):
            d.rectangle((40,39,88,60),fill=(115,115,116))
        imlist.append(im)
    return imlist,world

def observe_and_test(kind,seed):
    imgs,oracle=make_case(kind,seed)
    try:
        offsets=camera_evidence(imgs)
        paths=track(imgs,offsets)
        answer=decision(paths)
        best=paths[0]["xs"] if paths else []
        # Do not score arbitrary A/B identity against a single guessed ID
        # when images are observationally symmetric.
        identity_claimed=(kind in ("crossing_indistinguishable","substitution")
                          and answer["status"]=="SELECT")
        camera_claimed=(kind=="camera_without_landmarks"
                        and answer["status"]=="SELECT")
        return {"case":kind,"seed":seed,
          "oracle_identity_identifiable":oracle["identity_identifiable"],
          "oracle_camera_identifiable":oracle["camera_identifiable"],
          "camera_from_pixels":offsets,"paths":paths,
          "answer":answer,"candidate_x":best,
          "unsafe_identity_claim":identity_claimed,
          "unsafe_camera_claim":camera_claimed}
    finally:
        for im in imgs:im.close()

def run(out,seed=165,n_each=25,minutes=20):
    if not(5<=n_each<=300 and 2<=minutes<=90):raise ValueError("INVALID_BOUNDS")
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    start=time.monotonic();deadline=start+minutes*60
    stats={name:{"n":0,"unsafe_identity_claims":0,
                "unsafe_camera_claims":0,"holds":0,"multis":0,
                "novelty_candidates":0} for name in CASES}
    with (p/"ADVERSARIAL_EXAMS.jsonl").open("w",encoding="utf8") as log:
        for case in CASES:
            for i in range(n_each):
                if time.monotonic()>=deadline:break
                row=observe_and_test(case,seed+CASES.index(case)*100003+i*199)
                entry=stats[case];entry["n"]+=1
                entry["unsafe_identity_claims"]+=int(row["unsafe_identity_claim"])
                entry["unsafe_camera_claims"]+=int(row["unsafe_camera_claim"])
                entry["holds"]+=int(row["answer"]["status"]=="HOLD")
                entry["multis"]+=int(row["answer"]["status"]=="MULTI")
                entry["novelty_candidates"]+=int(row["answer"]["status"]=="NOVELTY_CANDIDATE")
                log.write(json.dumps(row)+"\n")
    report={"schema":"BRODY_P165A_ADVERSARIAL_FIXTURES",
      "test_scope":"SIX_NEW_FAMILIES_ONLY",
      "full_hard_plus_plus_16_family_suite_implemented":False,
      "legacy_77_cells_untouched_and_not_run_here":True,
      "episodes":sum(v["n"] for v in stats.values()),
      "duration_seconds":round(time.monotonic()-start,3),
      "cases":stats,
      "identity_and_camera_unsafe_claims":sum(v["unsafe_identity_claims"]+v["unsafe_camera_claims"] for v in stats.values()),
      "run_complete":all(v["n"]==n_each for v in stats.values()),
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report

def main():
    q=argparse.ArgumentParser()
    q.add_argument("--out",required=True);q.add_argument("--seed",type=int,default=165)
    q.add_argument("--n-each",type=int,default=25);q.add_argument("--minutes",type=int,default=20)
    a=q.parse_args();r=run(a.out,a.seed,a.n_each,a.minutes)
    print(json.dumps(r,indent=2))
if __name__=="__main__":main()
