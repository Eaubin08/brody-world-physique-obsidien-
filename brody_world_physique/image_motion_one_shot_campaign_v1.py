"""Brody one-shot motion experiment, from independent frame folders to A/B report.

Modes:
 demo: deterministic synthetic sequences, unequivocally not real-world evidence.
 real:  independent recorded scene folders each containing 000..004 images,
        explicit provenance JSON for each scene. Never downloads source media.
Frames are copied/resized only into a new output, never modify originals.
"""
from __future__ import annotations
import argparse,json,random
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from .image_motion_independent_campaign_v1 import campaign
from .image_multihypothesis_motion_memory_v1 import write

EXT={".png",".jpg",".jpeg",".bmp",".webp"}
def prepare(source,dest):
    rows=[]
    for group in sorted(p for p in Path(source).iterdir() if p.is_dir()):
        meta=group/"provenance.json"
        if not meta.is_file():raise ValueError("PROVENANCE_REQUIRED:"+group.name)
        obj=json.loads(meta.read_text(encoding="utf-8-sig"))
        if obj.get("origin") not in ("camera","video") or obj.get("split") not in ("train","exam"):
            raise ValueError("BAD_ORIGIN_OR_SPLIT:"+group.name)
        files=sorted(f for f in group.iterdir() if f.suffix.lower() in EXT and f.is_file())
        if len(files)!=5:raise ValueError("FIVE_FRAMES_REQUIRED:"+group.name)
        episode=dest/group.name;episode.mkdir(parents=True)
        outputs=[]
        for i,src in enumerate(files):
            im=ImageOps.exif_transpose(Image.open(src)).convert("RGB").resize((64,64))
            out=episode/(str(i)+".png");im.save(out)
            outputs.append(str(out.resolve()))
        rows.append({"source_group":obj.get("recording_id",group.name),
          "origin":obj["origin"],"split":obj["split"],
          "observations":[{"t":i,"file":outputs[i]} for i in range(4)],
          "predict_t":4,"actual":outputs[4]})
    if not rows:raise ValueError("NO_SOURCE_GROUPS")
    return rows
def demo(dest):
    specs=[
     ("train_fall_a","train",[7,11,17,25,35],17),
     ("train_fall_b","train",[8,13,20,29,40],28),
     ("train_still","train",[20,20,20,20,20],13),
     ("exam_fall","exam",[9,13,19,27,37],40),
     ("exam_reverse","exam",[12,20,26,20,12],24),
     ("exam_stop","exam",[10,16,22,22,22],32)]
    rows=[]
    for group,split,positions,x in specs:
        frame_dir=dest/group;frame_dir.mkdir(parents=True)
        files=[]
        for i,y in enumerate(positions):
            im=Image.new("RGB",(64,64),"white")
            ImageDraw.Draw(im).ellipse((x-3,y-3,x+3,y+3),fill=(25,25,25))
            # Neutral bright variation makes stationary frames distinct in bytes
            # without changing measured dark-object position.
            im.putpixel((0,0),(235+i,235+i,235+i))
            file=frame_dir/(str(i)+".png");im.save(file)
            files.append(str(file.resolve()))
        rows.append({"source_group":group,"origin":"synthetic","split":split,
            "observations":[{"t":i,"file":files[i]} for i in range(4)],
            "predict_t":4,"actual":files[4]})
    return rows
def run(mode,out,sources=None):
    target=Path(out)
    if target.exists():raise ValueError("PRESERVE_EVIDENCE")
    if mode=="real" and (not sources or not Path(sources).is_dir()):
        raise ValueError("REAL_SOURCE_DIRECTORY_REQUIRED")
    target.mkdir(parents=True)
    rows=demo(target/"frames") if mode=="demo" else prepare(sources,target/"frames")
    manifest=target/"campaign_manifest.json";write(manifest,rows)
    result=campaign(manifest,target/"campaign")
    summary={"schema":"BRODY_END_TO_END_PHYSICS_CAMPAIGN_V1","mode":mode,
       "synthetic_demonstration_only":mode=="demo",
       "source_episodes":len(rows),"train_episodes":result["train_episodes"],
       "exam_episodes":result["exam_episodes"],
       "paired_memory_advantage_px":result["paired_memory_advantage_px"],
       "memory_outperforms_baseline":result["memory_outperforms_baseline_on_paired_cases"],
       "source_independence_verified":False,
       "real_world_generalization_proven":False,
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}
    write(target/"MASTER_REPORT.json",summary)
    return summary
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=("demo","real"),required=True)
    p.add_argument("--sources");p.add_argument("--out",required=True)
    a=p.parse_args()
    print(json.dumps(run(a.mode,a.out,a.sources),indent=2))
if __name__=="__main__":main()
