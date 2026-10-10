"""Teacher-bound multiple views: one identity candidate, many observations.

No automatic semantic object discovery. A teacher identity groups evidence;
unseen transformations are assessed without relabeling by filename.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageOps
from .image_external_source_school_v0 import reference
from .image_structural_observation_v1 import describe
from .fusion_f9_intensive_education_v0 import digest,verify_chain

VIEWS=("identity","mirror","quarter_turn","half_turn")
def views(im,kind):
    if kind=="identity":return im.copy()
    if kind=="mirror":return ImageOps.mirror(im)
    if kind=="quarter_turn":return im.transpose(Image.Transpose.ROTATE_90)
    if kind=="half_turn":return im.transpose(Image.Transpose.ROTATE_180)
    raise ValueError("UNKNOWN_VIEW")
def run(manifest,out):
    target=Path(out)
    if target.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    roots=json.loads(Path(manifest).read_text(encoding="utf-8-sig"))
    if not isinstance(roots,list) or not roots:raise ValueError("NO_TAUGHT_IDENTITIES")
    target.mkdir(parents=True)
    seen_ids=set();rows=[];prev=None
    with (target/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for item in roots:
            object_id=item["identity"];files=item["examples"]
            if not isinstance(object_id,str) or not object_id or object_id in seen_ids:
                raise ValueError("INVALID_IDENTITY")
            if not isinstance(files,list) or not files:raise ValueError("NO_EXAMPLES")
            seen_ids.add(object_id);training=[];exam=[]
            for filename in files:
                image=reference(Path(filename))
                source_hash=hashlib.sha256(Path(filename).read_bytes()).hexdigest()
                baseline=describe(image)
                # Train on original/mirror, evaluate unseen quarter-turn/half-turn.
                for kind in VIEWS:
                    feature=describe(views(image,kind))
                    record={"identity_candidate":object_id,"image_sha256":source_hash,
                        "view":kind,"observation_context":feature["context"],
                        "observed_parts":feature["parts"],"observed_relations":feature["relations"]}
                    if kind in ("identity","mirror"):training.append(record)
                    else:exam.append(record)
            contexts={r["observation_context"] for r in training}
            for example in exam:
                # Context equality alone is a weak transfer heuristic.
                supported=example["observation_context"] in contexts
                row={"index":len(rows)+1,"previous":prev,
                    "teacher_identity":object_id,"view":example["view"],
                    "image_sha256":example["image_sha256"],
                    "context":example["observation_context"],
                    "known_context_match":supported,
                    "identity_claim":"TEACHER_ASSIGNED_NOT_MODEL_INFERRED",
                    "native_memory_write":False,"canonical_promotion":False,
                    "decision_authority":"KX108_ONLY"}
                row["digest"]=digest(row);prev=row["digest"]
                f.write(json.dumps(row,sort_keys=True)+"\n");rows.append(row)
    n,tip=verify_chain(target/"receipts.jsonl")
    report={"schema":"BRODY_MULTIVIEW_TEACHER_IDENTITY_V0",
        "taught_identities":len(seen_ids),"heldout_views":n,
        "heldout_context_matches":sum(r["known_context_match"] for r in rows),
        "heldout_context_misses":sum(not r["known_context_match"] for r in rows),
        "receipt_tip":tip,"identity_learned_from_pixels":False,
        "training_views":["identity","mirror"],"exam_views":["quarter_turn","half_turn"],
        "semantic_object_recognition_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "status":"TEACHER_GROUPED_MULTIVIEW_CONTEXT_TRANSFER_ONLY"}
    (target/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.manifest,a.out),indent=2))
if __name__=="__main__":main()
