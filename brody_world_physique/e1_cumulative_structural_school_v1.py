"""Brody E1: cumulative shape memory with blind transfer and interference.

Reuses actual P134 scene/learn/hypothesize/paint/compare. Two independently
named training source groups per shape. The P134 hypotheses use the held-out
image ONLY to perceive component bounding boxes and shape signatures;
therefore this tests mask-reuse, NOT blind object detection or pure generation.
"""
from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
from .image_reciprocal_shape_learning_p134 import (
    scene,learn,hypothesize,paint,compare,memory_fresh,shape_signature)
from .experiential_skill_learning_v1 import save,seal,sha

def draw(path,kind,x,y):
    im=Image.new("RGB",(64,64),"white")
    d=ImageDraw.Draw(im)
    if kind=="square":d.rectangle((x,y,x+10,y+10),fill=(40,45,65))
    elif kind=="circle":d.ellipse((x,y,x+10,y+10),fill=(40,45,65))
    elif kind=="triangle":d.polygon([(x+5,y),(x,y+10),(x+10,y+10)],fill=(40,45,65))
    else:raise ValueError("UNKNOWN_SHAPE")
    im.save(path)

def frozen(mem):
    # Hash includes masks and all individual training source groups.
    return seal({"schema":"BRODY_E1_STRUCTURAL_SKILL_SNAPSHOT",
        "prototypes":mem["prototypes"],
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY"})

def test_case(root,mem,name,kind,x,y,train_hashes):
    path=root/(name+"_target.png");draw(path,kind,x,y)
    h=sha(path)
    if h in train_hashes:raise ValueError("TRAIN_EXAM_LEAK")
    ob=scene(path)
    # No label passed to the P134 estimator. Known geometry is visible through
    # the heldout image, so this is an observational transfer examination.
    pre=hypothesize(mem,ob,"exam_"+name)
    sealed=seal({"case":name,"target_sha":h,"memory_digest":frozen(mem)["digest"],
        "mode":pre["mode"],"reason":pre["reason"],"candidate_parts":pre["parts"],
        "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"})
    save(root/(name+"_pre_feedback.json"),sealed)
    if pre["mode"]=="CANDIDATE":
        generated=root/(name+"_generated.png");paint(pre["parts"],generated)
        metrics=compare(generated,path)
        retained=scene(generated)["count"]
    else:metrics=None;retained=None
    return {"case":name,"mode":pre["mode"],"reason":pre["reason"],
        "mae_rgb":metrics["mae_rgb"] if metrics else None,
        "parts_reconstructed":retained,"parts_observed":ob["count"],
        "truth_not_in_candidate_precommit":True}

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    mem=memory_fresh();train_hashes=set();lessons=[]
    def teach(name,kind,x,y,group):
        path=root/(name+".png");draw(path,kind,x,y)
        if sha(path) in train_hashes:raise ValueError("TRAIN_DUPLICATE")
        train_hashes.add(sha(path))
        obs=scene(path)
        for p in obs["components"]:learn(mem,p,group)
        lessons.append({"lesson":name,"group":group,"kind_taught":kind,
            "source_sha256":sha(path),"components":obs["count"]})
    teach("square_lesson_1","square",4,8,"square_source_1")
    teach("square_lesson_2","square",18,8,"square_source_2")
    memory_before=frozen(mem)
    save(root/"SNAPSHOT_BEFORE_INTERFERENCE.json",memory_before)
    first=test_case(root,mem,"square_before","square",34,12,train_hashes)
    # Interfering different task: train circle WITHOUT deleting square prototypes.
    teach("circle_lesson_1","circle",5,28,"circle_source_1")
    teach("circle_lesson_2","circle",19,28,"circle_source_2")
    memory_after=frozen(mem)
    save(root/"SNAPSHOT_AFTER_INTERFERENCE.json",memory_after)
    square_after=test_case(root,mem,"square_after","square",34,12,train_hashes)
    circle_new=test_case(root,mem,"circle_new","circle",35,31,train_hashes)
    novel=test_case(root,mem,"novel_triangle","triangle",36,31,train_hashes)
    # Retention is compared on the SAME blind item across stages, and its
    # original precommit is untouched. The two stages have different memories.
    result={"schema":"BRODY_E1_CUMULATIVE_SHAPE_TRANSFER_V1",
        "lessons":lessons,"before":first,"after":square_after,
        "circle_transfer":circle_new,"novel":novel,
        "retained_after_interference":first["mode"]=="CANDIDATE"
            and square_after["mode"]=="CANDIDATE"
            and first["mae_rgb"]==square_after["mae_rgb"],
        "independent_training_groups":4,
        "blind_source_hashes_disjoint":True,
        "shared_experimental_memory":True,
        "exam_observation_supplies_geometry_and_shape_signature":True,
        "pure_blind_generation_proven":False,
        "general_semantic_identity_proven":False,
        "real_world_transfer_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"E1_CUMULATIVE_MASK_TRANSFER_BOUNDED"}
    save(root/"MASTER_REPORT.json",result)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],"before":r["before"]["mode"],
        "retained":r["retained_after_interference"],
        "circle":r["circle_transfer"]["mode"],"novel":r["novel"]["mode"]},indent=2))
if __name__=="__main__":main()
