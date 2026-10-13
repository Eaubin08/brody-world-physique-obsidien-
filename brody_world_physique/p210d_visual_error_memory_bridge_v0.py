"""P2.10d: append-only local candidate memory of supervised IMAGE corrections.

No autonomous transfer claim, no canonical memory write. All entries are tied to
verified P2.10c image receipts; rejected/equal attempts remain visible.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .p210a_visual_loop_contract_v0 import digest
from .p210c_targeted_image_correction_v0 import verify as verify_correction

SCHEMA="BRODY_P210D_VISUAL_EXPERIENCE_LEDGER_V0"
ALLOWED={"ACCEPTED","HOLD_EQUAL","ROLLED_BACK"}

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def hexdigest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def _entry(source,initial,mask,candidate):
    proof=verify_correction(candidate,source,initial,mask)
    receipt=Path(candidate).with_suffix(".json")
    data=json.loads(receipt.read_text(encoding="utf-8"))
    if proof["verdict"] not in ALLOWED:raise ValueError("unsupported verdict")
    return {"source_path":str(Path(source).resolve()),
            "initial_path":str(Path(initial).resolve()),
            "mask_path":str(Path(mask).resolve()),
            "candidate_path":str(Path(candidate).resolve()),
            "receipt_sha256":digest(receipt),
            "source_sha256":digest(source),
            "initial_sha256":digest(initial),
            "mask_sha256":digest(mask),
            "candidate_sha256":digest(candidate),
            "verdict":proof["verdict"],"before":data["error_before"],
            "after":data["error_after"],"method":"SUPERVISED_MASK_COMPOSITE",
            "reusable_parameters_only":True,
            "teacher_pixels_used":True,"candidate_skill_not_promoted":True}

def append(ledger,source,initial,mask,candidate):
    path=Path(ledger)
    if path.exists():
        previous=verify_ledger(path)
        entries=previous["entries"]
    else:entries=[]
    item=_entry(source,initial,mask,candidate)
    if any(row["candidate_sha256"]==item["candidate_sha256"] and
           row["source_sha256"]==item["source_sha256"] for row in entries):
        raise ValueError("duplicate episode")
    item["previous_digest"]=entries[-1]["entry_digest"] if entries else "GENESIS"
    item["entry_digest"]=hexdigest({k:v for k,v in item.items() if k!="entry_digest"})
    out={"schema":SCHEMA,"entries":entries+[item],"native_memory_write":False,
         "knowledge_promotion":False,"decision_authority":"KX108_ONLY"}
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return {"episodes":len(out["entries"]),"last_entry_digest":item["entry_digest"],
            "verdict":item["verdict"],"improved":item["after"]<item["before"]}

def verify_ledger(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    if (data.get("schema")!=SCHEMA or data.get("native_memory_write") is not False
        or data.get("knowledge_promotion") is not False
        or data.get("decision_authority")!="KX108_ONLY"):raise ValueError("ledger contract")
    chain="GENESIS"
    for row in data["entries"]:
        digest_expected=hexdigest({k:v for k,v in row.items() if k!="entry_digest"})
        if row["entry_digest"]!=digest_expected or row["previous_digest"]!=chain:
            raise ValueError("ledger chain")
        proof=_entry(row["source_path"],row["initial_path"],row["mask_path"],row["candidate_path"])
        for key in proof:
            if row[key]!=proof[key]:raise ValueError("episode tamper: "+key)
        chain=row["entry_digest"]
    return data

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ledger",required=True)
    p.add_argument("--source");p.add_argument("--initial")
    p.add_argument("--mask");p.add_argument("--candidate")
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    if args.verify:
        x=verify_ledger(args.ledger)
        print(json.dumps({"verified":True,"episodes":len(x["entries"])}))
    else:
        if not all((args.source,args.initial,args.mask,args.candidate)):
            p.error("source, initial, mask, candidate needed")
        print(json.dumps(append(args.ledger,args.source,args.initial,args.mask,args.candidate)))
if __name__=="__main__":main()
