"""F5: multi-skill cumulative candidate education and explicit readonly routing.

Routing uses an EXPLICIT IN skill goal only; absent/unknown is HOLD.
No TEST pixels, test score, or prompt-derived semantic guess chooses a skill.
"""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE
from .fusion_f3b_multilesson_school_v0 import draw_shape
from .fusion_f3c_cumulative_skill_archive_v0 import load_registry
from .fusion_f4_education_journal_v0 import teach_recorded,test_recorded,readonly_context,append_event,verify_journal

def route(root,version,goal):
    snap=readonly_context(root,version)
    matches=[name for name in snap["skill_ids"] if name==goal]
    if len(matches)!=1:
        return {"authority":"HOLD","reason":"UNKNOWN_OR_AMBIGUOUS_SKILL",
                "selected":None,"registry_digest":snap["registry_digest"],
                "test_pixels_seen":False,"decision_authority":"KX108_ONLY"}
    return {"authority":"CANDIDATE_PROPOSAL_ONLY","selected":matches[0],
            "registry_digest":snap["registry_digest"],"test_pixels_seen":False,
            "decision_authority":"KX108_ONLY"}

def course(out):
    root=Path(out)
    if root.exists():raise ValueError("output already exists")
    root.mkdir(parents=True)
    specs=(("rectangle","rectangle",[12,10,33,31]),
           ("triangle","triangle",[12,10,33,31]),
           ("ellipse","ellipse",[12,10,33,31]))
    version=0
    for name,shape,box in specs:
        train=root/("train-"+name+".png")
        image=Image.new("L",(SIDE,SIDE),255)
        draw_shape(ImageDraw.Draw(image),shape,box)
        image.save(train)
        version=teach_recorded(root,version,name,train)["version"]
    rows=[]
    exams=(("rectangle",[[5,5,25,25],[36,34,57,56]]),
           ("triangle",[[6,6,26,27],[33,33,57,57]]),
           ("ellipse",[[5,5,28,28],[34,31,58,56]]))
    for i,(goal,boxes) in enumerate(exams,1):
        choice=route(root,version,goal)
        if choice["selected"]!=goal:raise ValueError("valid selection unavailable")
        folder=root/("exam-%02d"%i+"-"+goal)
        teacher_dir=root/("teacher-%02d"%i);teacher_dir.mkdir()
        layout=teacher_dir/"layout.json"
        layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":boxes}))
        target=Image.new("L",(SIDE,SIDE),255)
        draw=ImageDraw.Draw(target)
        for box in boxes:draw_shape(draw,goal,box)
        gold=teacher_dir/"target.png";target.save(gold)
        report=test_recorded(root,version,goal,layout,gold,folder)
        rows.append({"goal":goal,"choice":choice,"candidate_error":report["candidate_error"],
                    "blank_error":report["blank_error"],"gain":report["gain"],
                    "verdict":report["verdict"],"exam_dir":str(folder)})
    unknown=route(root,version,"unseen_unknown")
    if unknown["authority"]!="HOLD":raise ValueError("unknown did not hold")
    result={"schema":"BRODY_F5_MULTI_SKILL_EDUCATION_V0",
            "training_skill_count":len(specs),"snapshot_version":version,
            "exams":rows,"unknown_route":unknown,
            "history_count":len(verify_journal(root)),
            "selects_by_explicit_goal_not_semantics":True,
            "cross_lesson_memory_reuse":True,
            "correction_after_failure_implemented":False,
            "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (root/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args();r=course(args.out)
    print(json.dumps({"skills":r["training_skill_count"],"exams":[[x["goal"],x["gain"],x["verdict"]] for x in r["exams"]],"unknown":r["unknown_route"]["authority"]}))
if __name__=="__main__":main()
