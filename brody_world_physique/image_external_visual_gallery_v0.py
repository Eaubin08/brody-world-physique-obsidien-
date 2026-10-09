"""Visual proof gallery with a sealed baseline, supervised correction and diff.

This reuses existing archived external-image inputs, does not overwrite the
existing 315-case report, and never writes Native Memory / sovereign kernel.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image,ImageChops,ImageOps,ImageDraw
from .image_external_source_school_v0 import load_sources,reference,transform,MODES
from .drawing_school_v1 import suggest_gestures_from_reference
from .instrument_school_v2 import TOOLS,render_instrument,_gray_pixel_loss
from .fusion_f9_intensive_education_v0 import digest,verify_chain

def panel(images,names):
    board=Image.new("RGB",(64*len(images),88),"white")
    for index,(im,title) in enumerate(zip(images,names)):
        board.paste(im.convert("RGB"),(index*64,24))
        ImageDraw.Draw(board).text((index*64+2,5),title,fill="black")
    return board

def examine(im,mode,out_dir,stem):
    observed=transform(im,mode)
    gestures=suggest_gestures_from_reference(observed)
    blank=Image.new("L",(64,64),255)
    # Baseline selection is fixed independently of the reference.
    baseline_tool=TOOLS[0]
    initial=render_instrument(gestures,baseline_tool) if gestures else blank
    initial_bytes=initial.tobytes()
    commitment=hashlib.sha256(initial_bytes).hexdigest()
    before=_gray_pixel_loss(initial,observed)
    if gestures:
        candidates={tool:render_instrument(gestures,tool) for tool in TOOLS}
        winner=min(TOOLS,key=lambda t:(_gray_pixel_loss(candidates[t],observed),TOOLS.index(t)))
        reconstructed=candidates[winner]
        after=_gray_pixel_loss(reconstructed,observed)
        status="SUPERVISED_CANDIDATE"
    else:
        winner=None;reconstructed=blank;after=None
        status="HOLD_NO_TRACED_STROKE"
    diff=ImageChops.difference(observed,reconstructed)
    # Amplify to reveal faint error while preserving reproducible raw error.
    enhanced=diff.point(lambda x:min(255,x*3))
    out_dir.mkdir(parents=True,exist_ok=True)
    gallery=panel([observed,initial,reconstructed,enhanced],
                  ["Target","Baseline","Corrected","Diff x3"])
    image_path=out_dir/(stem+".png")
    gallery.save(image_path)
    return {"status":status,"baseline_tool":baseline_tool,"chosen_tool":winner,
      "before_loss":before,"after_loss":after,
      "improved":after is not None and after<before-1e-10,
      "worsened":after is not None and after>before+1e-10,
      "initial_commitment_sha256":commitment,
      "gallery_file":image_path.name,"gallery_sha256":hashlib.sha256(image_path.read_bytes()).hexdigest(),
      "gestures":len(gestures),"feedback_used_for_correction":True}

def run(images,out,max_images=100):
    paths=load_sources(images)[:max_images]
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    root.mkdir(parents=True)
    rows=[];prev=None
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as handle:
        for index,path in enumerate(paths,1):
            im=reference(path)
            src_hash=hashlib.sha256(path.read_bytes()).hexdigest()
            for mode in MODES:
                case_id=f"{index:04d}_{mode}"
                event=examine(im,mode,root/"gallery",case_id)
                row={"index":len(rows)+1,"previous":prev,"file":path.name,
                    "source_sha256":src_hash,"transform":mode,**event,
                    "source_kind":"ARCHIVED_PROJECT_IMAGE_UNVERIFIED_ORIGIN",
                    "memory_write":False,"kernel_mutation":False,"decision_authority":"KX108_ONLY"}
                row["digest"]=digest(row);prev=row["digest"]
                handle.write(json.dumps(row,sort_keys=True)+"\n");rows.append(row)
    count,tip=verify_chain(root/"receipts.jsonl")
    if count!=len(paths)*len(MODES):raise RuntimeError("MISSING_CASES")
    report={"schema":"BRODY_EXTERNAL_IMAGE_VISUAL_GALLERY_V0",
        "images":len(paths),"cases":count,"receipt_tip":tip,
        "galleries":count,"holds":sum(x["status"].startswith("HOLD") for x in rows),
        "improved":sum(x["improved"] for x in rows),
        "worsened":sum(x["worsened"] for x in rows),
        "mean_before":sum(x["before_loss"] for x in rows)/count,
        "mean_after":(sum(x["after_loss"] for x in rows if x["after_loss"] is not None)/
                      max(1,sum(x["after_loss"] is not None for x in rows))),
        "baseline":"FIXED_PENCIL_NOT_LEARNED_POLICY",
        "correction":"VISIBLE_REFERENCE_EXHAUSTIVE_THREE_TOOL_SEARCH",
        "image_origin_authenticated":False,"semantic_vision_proven":False,
        "blind_generalization_proven":False,"memory_write":False,
        "kernel_mutation":False,"decision_authority":"KX108_ONLY",
        "status":"VISUAL_ERROR_GALLERY_RECORDED_SYNTHETIC_TOOLS"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--images",required=True)
    parser.add_argument("--out",required=True)
    parser.add_argument("--max-images",type=int,default=100)
    args=parser.parse_args()
    print(json.dumps(run(args.images,args.out,args.max_images),indent=2))
if __name__=="__main__":main()
