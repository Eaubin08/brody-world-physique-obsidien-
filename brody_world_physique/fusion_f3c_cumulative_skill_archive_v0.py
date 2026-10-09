"""F3c: persistent immutable candidate-skill archive across visual lessons.

Trainer appends NEW immutable manifest versions; consumer reads validated
snapshots only. Never writes Obsidia Native Memory or promotes skill to B8.
TEST feedback is audit-only, not consumed as training or selection authority.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE
from .p211b_frozen_gesture_transfer_v0 import learn,read
from .p211c_gesture_recomposition_v0 import compose
from .p210a_visual_loop_contract_v0 import digest,open_rgba,pixel_error
from .fusion_f3b_multilesson_school_v0 import draw_shape

SCHEMA="BRODY_F3C_FROZEN_SKILL_ARCHIVE_V0"
def _hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load_registry(root,version):
    root=Path(root)
    if version==0:return {"schema":SCHEMA,"version":0,"previous":None,"skills":[],
                          "native_memory_write":False,"auto_promotion":False,
                          "decision_authority":"KX108_ONLY"}
    path=root/"versions"/f"v{version:03}.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    signature=data.pop("digest")
    if signature!=_hash(data) or data["schema"]!=SCHEMA or data["version"]!=version:
        raise ValueError("registry corrupted")
    if data["native_memory_write"] is not False or data["auto_promotion"] is not False or data["decision_authority"]!="KX108_ONLY":
        raise ValueError("authority mismatch")
    ids=set()
    for s in data["skills"]:
        if s["id"] in ids:raise ValueError("duplicated skill")
        ids.add(s["id"])
        memory=root/s["memory_path"]
        if not memory.is_file() or digest(memory)!=s["memory_sha256"]:raise ValueError("candidate memory changed")
        read(memory) # verify motor fingerprint and receipt against actual code
    if version>1:
        parent=load_registry(root,version-1)
        if data["previous"]!=parent["digest"] or data["skills"][:len(parent["skills"])]!=parent["skills"]:
            raise ValueError("non append-only memory history")
    elif data["previous"] is not None:raise ValueError("first registry has parent")
    data["digest"]=signature
    return data

def teach(root,previous_version,skill_id,training_image):
    root=Path(root)
    previous=load_registry(root,previous_version)
    if skill_id in {x["id"] for x in previous["skills"]}:raise ValueError("skill already taught")
    next_version=previous_version+1
    path=root/"versions"/f"v{next_version:03}.json"
    memory=root/"skills"/f"{skill_id}.json"
    if path.exists() or memory.exists():raise ValueError("immutable artifact exists")
    if not skill_id.isascii() or not skill_id.replace("_","").isalnum() or len(skill_id)>40:
        raise ValueError("unsafe skill id")
    learn(training_image,memory)
    entry={"id":skill_id,"memory_path":memory.relative_to(root).as_posix(),
           "memory_sha256":digest(memory),"training_sha256":digest(training_image),
           "authority":"FROZEN_TRAIN_CANDIDATE"}
    updated={"schema":SCHEMA,"version":next_version,
             "previous":previous.get("digest"),"skills":previous["skills"]+[entry],
             "native_memory_write":False,"auto_promotion":False,
             "decision_authority":"KX108_ONLY"}
    updated["digest"]=_hash(updated)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(updated,indent=2)+"\n",encoding="utf-8")
    return load_registry(root,next_version)

def exam(root,version,skill_id,layout_path,teacher_path,output):
    """Generate using only frozen TRAIN gestures and layout; score afterwards."""
    root=Path(root);registry=load_registry(root,version)
    entries=[s for s in registry["skills"] if s["id"]==skill_id]
    if len(entries)!=1:raise ValueError("unknown learned skill")
    entry=entries[0];out=Path(output)
    if out.exists():raise ValueError("exam exists")
    # Defend from accidental TRAIN-as-TEST reuse without opening target pixels.
    if digest(teacher_path)==entry["training_sha256"]:raise ValueError("target equals train")
    out.mkdir(parents=True)
    candidate=out/"candidate.png"
    report=compose(root/entry["memory_path"],layout_path,candidate)
    result={"schema":"BRODY_F3C_RECALL_EXAM_V0","registry_version":version,
            "registry_sha256":registry["digest"],"skill_id":skill_id,
            "candidate_sha256":digest(candidate),"sealed_before_teacher":True,
            "target_used_to_select_memory":False,"memory_reused_from_previous_lesson":True,
            "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    target=open_rgba(teacher_path);actual=open_rgba(candidate);blank=open_rgba(out/"candidate-blank.png")
    result["candidate_error"]=pixel_error(target,actual)
    result["blank_error"]=pixel_error(target,blank)
    result["gain"]=result["blank_error"]-result["candidate_error"]
    result["verdict"]="IMPROVED" if result["gain"]>0 else "WORSENED" if result["gain"]<0 else "TIE"
    sheet=Image.new("RGB",(SIDE*3,SIDE+18),"white");pen=ImageDraw.Draw(sheet)
    for idx,(label,img) in enumerate((("TEACHER",target),("BLANK",blank),("RECALL",actual))):
        pen.text((idx*SIDE+1,1),label,fill="black")
        sheet.paste(img.convert("RGB"),(idx*SIDE,18))
    sheet.save(out/"comparison.png")
    (out/"exam.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result

def demo(output):
    root=Path(output)
    if root.exists():raise ValueError("archive exists")
    root.mkdir(parents=True)
    train=root/"train-rectangle.png"
    img=Image.new("L",(SIDE,SIDE),255)
    draw_shape(ImageDraw.Draw(img),"rectangle",[12,10,33,31]);img.save(train)
    # Learn ONCE, use the same frozen candidate memory across later lessons.
    teach(root,0,"rectangle",train)
    specs=(([[5,5,27,27]],"01-recall"),([[6,8,28,30],[35,33,57,55]],"02-recomposition"),
           ([[5,5,22,22],[33,5,55,27],[14,35,38,57]],"03-transfer"))
    rows=[]
    for boxes,label in specs:
        inputs=root/(label+"-teacher");inputs.mkdir()
        layout=inputs/"layout.json";layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":boxes}))
        gold=Image.new("L",(SIDE,SIDE),255);d=ImageDraw.Draw(gold)
        for box in boxes:draw_shape(d,"rectangle",box)
        teacher=inputs/"target.png";gold.save(teacher)
        rows.append({"lesson":label,**exam(root,1,"rectangle",layout,teacher,root/label)})
    report={"schema":"BRODY_F3C_CUMULATIVE_DEMO_V0","training_count":1,
            "exams_without_retraining":len(rows),"rows":rows,
            "progressive_ability_increase_proven":False,
            "frozen_candidate_reuse_proven":True,
            "native_memory_write":False}
    (root/"summary.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--demo",action="store_true");p.add_argument("--out",required=True)
    a=p.parse_args()
    if not a.demo:p.error("specify --demo")
    s=demo(a.out)
    print(json.dumps({"training_count":s["training_count"],"reuses":s["exams_without_retraining"],
                      "results":[[r["lesson"],r["gain"],r["verdict"]] for r in s["rows"]]}))
if __name__=="__main__":main()
