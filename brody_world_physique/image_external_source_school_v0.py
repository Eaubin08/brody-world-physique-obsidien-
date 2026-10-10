"""External-image school: observable reference, generic raster tracing, held-out transforms.

Inputs are user-supplied raster files, never rendered by the instrument-school
teacher. No auto-claim of real sensor authentication or semantic understanding.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from pathlib import Path
from statistics import mean
from PIL import Image,ImageOps,ImageFilter,ImageChops
from .drawing_school_v1 import suggest_gestures_from_reference
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss
from .fusion_f9_intensive_education_v0 import digest,verify_chain

EXTENSIONS={".png",".jpg",".jpeg",".bmp",".webp"}
MODES=("identity","mirror","rotation","blur","contrast")
def load_sources(root):
    files=sorted(p for p in Path(root).iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS)
    if not files:raise ValueError("NO_INDEPENDENT_IMAGE_FILES")
    return files

def reference(path):
    with Image.open(path) as im:
        if im.width<32 or im.height<32:raise ValueError("SOURCE_TOO_SMALL:"+str(path))
        gray=ImageOps.grayscale(im)
        # Preserve the full frame but normalize input to existing 64x64 motor.
        return ImageOps.pad(gray,(64,64),color=255)

def transform(im,mode):
    if mode=="identity":return im.copy()
    if mode=="mirror":return ImageOps.mirror(im)
    if mode=="rotation":return im.transpose(Image.Transpose.ROTATE_90)
    if mode=="blur":return im.filter(ImageFilter.GaussianBlur(radius=1.2))
    if mode=="contrast":
        from PIL import ImageEnhance
        return ImageEnhance.Contrast(im).enhance(0.6)
    raise ValueError("UNKNOWN_TRANSFORMATION")

def evaluate(image,variant):
    observed=transform(image,variant)
    # Perception/tracing: generic pixels -> skeleton strokes, not image label.
    proposed=suggest_gestures_from_reference(observed)
    renderings={tool:render_instrument(proposed,tool) for tool in TOOLS}
    if not proposed:
        return {"status":"HOLD_NO_TRACED_STROKE","perceived_strokes":0,
                "tool":None,"pixel_loss":None,"reconstruction_sha256":None}
    # Visible-reference feedback is a supervised exhaustive 3-tool evaluation.
    losses={tool:_gray_pixel_loss(renderings[tool],observed) for tool in TOOLS}
    best=min(TOOLS,key=lambda t:(losses[t],TOOLS.index(t)))
    return {"status":"CANDIDATE_RECONSTRUCTION","perceived_strokes":len(proposed),
            "tool":best,"pixel_loss":losses[best],
            "reconstruction_sha256":hashlib.sha256(renderings[best].tobytes()).hexdigest()}

def run(images,out,max_images=100,seed=20261009):
    paths=load_sources(images)
    if len(paths)>max_images:paths=paths[:max_images]
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    # Use real external pixels, never the school renderer as source.
    loaded=[(p,reference(p),hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
    dest.mkdir(parents=True)
    records=[];previous=None
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for idx,(path,im,sha) in enumerate(loaded,1):
            for mode in MODES:
                result=evaluate(im,mode)
                item={"index":len(records)+1,"previous":previous,
                  "filename":path.name,"input_sha256":sha,"transformation":mode,
                  "source_kind":"EXTERNAL_FILE_UNVERIFIED_ORIGIN",
                  **result,"native_memory_write":False,"canonical_promotion":False,
                  "decision_authority":"KX108_ONLY"}
                item["digest"]=digest(item)
                f.write(json.dumps(item,sort_keys=True)+"\n")
                previous=item["digest"];records.append(item)
    n,tip=verify_chain(dest/"receipts.jsonl")
    if n!=len(records):raise RuntimeError("RECEIPT_INTEGRITY_FAILED")
    families={}
    for mode in MODES:
        group=[r for r in records if r["transformation"]==mode]
        scored=[r["pixel_loss"] for r in group if r["pixel_loss"] is not None]
        families[mode]={"cases":len(group),"holds":len(group)-len(scored),
            "mean_pixel_loss":mean(scored) if scored else None}
    report={"schema":"BRODY_EXTERNAL_IMAGE_TRACING_EXAM_V0",
      "source_images":len(loaded),"evaluations":n,"receipt_tip":tip,"by_transform":families,
      "sources_independent_from_school_renderer_by_user_supplied_files":True,
      "source_authenticity_verified":False,"image_semantics_proven":False,
      "physical_prediction_proven":False,"tool_selection_is_supervised":True,
      "cross_episode_learning":False,"native_memory_write":False,
      "kernel_mutation":False,"decision_authority":"KX108_ONLY",
      "status":"EXTERNAL_IMAGE_RECONSTRUCTION_MEASURED_NO_AUTONOMOUS_VISION_PROOF"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--images",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--max-images",type=int,default=100)
    a=p.parse_args()
    print(json.dumps(run(a.images,a.out,a.max_images),indent=2))
if __name__=="__main__":main()
