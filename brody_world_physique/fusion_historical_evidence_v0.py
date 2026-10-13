"""FUSION-F1: readonly common evidence adapter for historical and new drawing schools.

Consumes a user-authored manifest of ORIGINAL files; does not modify source,
run a learner, infer teacher labels, or promote memory. Only score comparable
pairs with explicit reference. All other scores remain UNKNOWN.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE

SCHEMA="BRODY_FUSION_EVIDENCE_V0"
ROLES=("teacher","first","from_memory","after_feedback","transfer")
STAGES=frozenset("E"+str(i) for i in range(8))
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_image(path):
    with Image.open(path) as src:
        return src.convert("RGB")
def mismatch(a,b):
    if a.size!=b.size: return None
    # Pixel mismatch, not a learned semantic or perceptual metric.
    x=a.tobytes();y=b.tobytes()
    return sum(x[k:k+3]!=y[k:k+3] for k in range(0,len(x),3))
def compile_evidence(manifest,output):
    inp=Path(manifest)
    config=json.loads(inp.read_text(encoding="utf-8"))
    if config.get("schema")!=SCHEMA:raise ValueError("manifest schema")
    episodes=config.get("episodes")
    if not isinstance(episodes,list) or not 1<=len(episodes)<=100:
        raise ValueError("episodes")
    dest=Path(output)
    if dest.exists():raise ValueError("output exists")
    seen=set();rows=[];images=[]
    for episode in episodes:
        if not isinstance(episode,dict) or set(episode)!={"id","stage","mode","files"}:
            raise ValueError("episode contract")
        key=episode["id"]
        if not isinstance(key,str) or not key or key in seen:
            raise ValueError("duplicate/invalid episode ID")
        seen.add(key)
        if episode["stage"] not in STAGES or episode["mode"] not in ("GUIDED","HIDDEN_TARGET","UNSEEN_TRANSFER"):
            raise ValueError("stage/mode")
        files=episode["files"]
        if not isinstance(files,dict) or not files or set(files)-set(ROLES):
            raise ValueError("roles")
        resolved={};screens={}
        for role,name in files.items():
            if not isinstance(name,str):raise ValueError("path")
            p=Path(name)
            if not p.is_file():raise ValueError("missing historical image: "+name)
            im=read_image(p)
            resolved[role]={"sha256":sha(p),"original_path":str(p.resolve()),"size":list(im.size)}
            screens[role]=im
        teacher=screens.get("teacher")
        scores={}
        for role in ROLES[1:]:
            val=mismatch(teacher,screens[role]) if teacher is not None and role in screens else None
            scores[role]={"mismatch_pixels":val,"comparable":val is not None,
                          "status":"SCORED_WITH_TEACHER" if val is not None else "UNKNOWN_NO_COMPARABLE_TEACHER"}
        rows.append({"id":key,"stage":episode["stage"],"mode":episode["mode"],
                     "files":resolved,"scores":scores,"no_ground_truth_inferred":True})
        images.append(screens)
    dest.mkdir(parents=True)
    # Visual montage keeps every image in its original file and marks missing
    # channels N/A, never invents a teacher or feedback.
    cell=SIDE*2
    width=cell*len(ROLES)
    sheet=Image.new("RGB",(width,(cell+28)*len(rows)),"white")
    draw=ImageDraw.Draw(sheet)
    for i,(row,shots) in enumerate(zip(rows,images)):
        y=(cell+28)*i
        for j,role in enumerate(ROLES):
            x=j*cell
            draw.text((x+3,y+2),f"{row['id']} - {role}",fill="black")
            if role in shots:
                image=shots[role]
                image.thumbnail((cell,cell),Image.Resampling.NEAREST)
                sheet.paste(image,(x+(cell-image.width)//2,y+28+(cell-image.height)//2))
            else:
                draw.text((x+6,y+45),"N/A",fill="black")
    sheet.save(dest/"historical_comparison.png")
    result={"schema":"BRODY_FUSION_EVIDENCE_REPORT_V0",
            "input_manifest_sha256":sha(inp),"episodes":rows,
            "count":len(rows),
            "comparable_scores":sum(s["comparable"] for r in rows for s in r["scores"].values()),
            "missing_comparisons":sum(not s["comparable"] for r in rows for s in r["scores"].values()),
            "comparison_sha256":sha(dest/"historical_comparison.png"),
            "historical_images_unchanged":True,"teacher_reference_never_inferred":True,
            "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (dest/"metrics.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();r=compile_evidence(a.manifest,a.out)
    print(json.dumps({k:r[k] for k in ("count","comparable_scores","missing_comparisons")}))
if __name__=="__main__":main()
