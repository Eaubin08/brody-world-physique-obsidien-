"""P2.10a: bounded, reversible visual generation attempt ledger.

Supervised image comparison ONLY. An existing generator must create initial
and candidate images BEFORE this evaluator sees them. Not a trained generator.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from PIL import Image, ImageChops

SCHEMA = "BRODY_P210A_VISUAL_LOOP_V0"
MAX_PIXELS=20_000_000

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def open_rgba(path):
    with Image.open(path) as im:
        if im.width*im.height > MAX_PIXELS:raise ValueError("image too large")
        return im.convert("RGBA")

def pixel_error(reference, attempt):
    if reference.size != attempt.size:raise ValueError("image dimensions differ")
    a=reference.convert("RGBA")
    b=attempt.convert("RGBA")
    # Number of pixels differing in one or more channels (not a semantic metric).
    d=ImageChops.difference(a,b).convert("RGB")
    return sum(any(channel for channel in pixel) for pixel in d.getdata())

def _record(path):
    p=Path(path)
    if not p.is_file():raise ValueError("image missing")
    return {"path":str(p.resolve()),"sha256":digest(p)}

def evaluate(source,initial,candidate,out,*,max_attempts=1):
    if max_attempts < 1 or max_attempts > 64:raise ValueError("invalid attempt budget")
    dest=Path(out)
    if dest.exists():raise ValueError("output already exists")
    src,ini,cand=map(open_rgba,(source,initial,candidate))
    if src.size != ini.size or src.size != cand.size:raise ValueError("dimension mismatch")
    source_ref=_record(source)
    initial_ref=_record(initial)
    candidate_ref=_record(candidate)
    initial_score=pixel_error(src,ini)
    proposed_score=pixel_error(src,cand)
    verdict="ACCEPTED" if proposed_score < initial_score else (
        "ROLLED_BACK" if proposed_score > initial_score else "HOLD_EQUAL")
    chosen=initial if verdict!="ACCEPTED" else candidate
    best=_record(chosen)
    result={
        "schema":SCHEMA,"mode":"SUPERVISED_REFERENCE_SCORING",
        "source":source_ref,"initial":initial_ref,"candidate":candidate_ref,
        "best":best,"initial_pixel_error":initial_score,
        "candidate_pixel_error":proposed_score,"verdict":verdict,
        "attempts":[{"index":1,"capability":"EXTERNAL_PREGENERATED_IMAGE",
            "candidate_sha256":candidate_ref["sha256"],
            "error_delta_pixels":proposed_score-initial_score,
            "verdict":verdict,"preserved_even_if_rejected":True}],
        "max_attempts":max_attempts,"generation_engine_executed":False,
        "memory_promotion":False,"native_memory_write":False,
        "decision_authority":"KX108_ONLY"}
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def verify(out):
    record=json.loads(Path(out).read_text(encoding="utf-8"))
    if record["schema"]!=SCHEMA:raise ValueError("schema")
    for field in ("source","initial","candidate","best"):
        if digest(record[field]["path"])!=record[field]["sha256"]:
            raise ValueError("image tampered: "+field)
    src,ini,cand=map(lambda x:open_rgba(record[x]["path"]),("source","initial","candidate"))
    first=pixel_error(src,ini)
    second=pixel_error(src,cand)
    verdict="ACCEPTED" if second<first else "ROLLED_BACK" if second>first else "HOLD_EQUAL"
    expected_best=record["candidate"] if verdict=="ACCEPTED" else record["initial"]
    if (first!=record["initial_pixel_error"] or second!=record["candidate_pixel_error"]
        or verdict!=record["verdict"] or expected_best!=record["best"]
        or len(record["attempts"])!=1
        or record["attempts"][0]["verdict"]!=verdict
        or record["attempts"][0]["error_delta_pixels"]!=second-first
        or record["generation_engine_executed"] is not False
        or record["native_memory_write"] is not False
        or record["decision_authority"]!="KX108_ONLY"):
        raise ValueError("replay mismatch")
    return {"verified":True,"verdict":verdict,"best":record["best"]["path"]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--initial")
    parser.add_argument("--candidate")
    parser.add_argument("--out",required=True)
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    if args.verify:result=verify(args.out)
    else:
        if not all((args.source,args.initial,args.candidate)):
            parser.error("--source, --initial and --candidate required")
        report=evaluate(args.source,args.initial,args.candidate,args.out)
        result={k:report[k] for k in ("verdict","initial_pixel_error","candidate_pixel_error","best")}
    print(json.dumps(result))
if __name__=="__main__":main()
