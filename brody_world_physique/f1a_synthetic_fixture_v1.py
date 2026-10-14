"""Create a deterministic, clearly synthetic F1A smoke dataset (not real physics)."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw

def create(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    train=root/"train";test=root/"test";train.mkdir();test.mkdir()
    labels={}
    for name,colour in (("red","red"),("blue","blue")):
        for i in range(3):
            im=Image.new("RGB",(64,64),"white")
            ImageDraw.Draw(im).ellipse((6+i*3,8+i*2,27+i*3,29+i*2),fill=colour)
            filename=f"{name}_{i}.png";im.save(train/filename)
            labels[filename]=name
        for i in range(2):
            im=Image.new("RGB",(64,64),"white")
            ImageDraw.Draw(im).ellipse((24+i*2,23+i*3,45+i*2,44+i*3),fill=colour)
            im.save(test/f"{name}_heldout_{i}.png")
    (root/"labels.json").write_text(json.dumps(labels,indent=2),encoding="utf8")
    (root/"DATASET_SCOPE.json").write_text(json.dumps({
        "schema":"BRODY_F1A_SYNTHETIC_SMOKE_DATASET_V1",
        "synthetic":True,"physical_motion_observed":False,
        "source":"deterministic PIL shapes","train_images":6,"test_images":4,
        "train_test_images_distinct":True,
        "semantic_identity_proven":False},indent=2),encoding="utf8")
    return root

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args();print(create(args.out))
if __name__=="__main__":main()
