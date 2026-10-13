"""Brody P131: heterogeneous competency probes, NOT repeated motion tests.

Each probe uses a different mechanism / falsifiable criterion. No fabricated
PASS for absent modules; missing capability is TODO and fails coverage.
"""
from __future__ import annotations
import argparse,hashlib,json,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from .image_structural_observation_v1 import describe
from .image_real_transfer_exam_v2 import features,train,predict,load_memory
from .image_reciprocal_generation_school_v1 import decode
from .image_context_transition_transfer_v1 import context
from .image_persistent_identity_teacher_loop_v1 import new_state,remember
from .fusion_f9_intensive_education_v0 import digest

def canvas(draw_fn):
    im=Image.new("RGB",(64,64),"white");draw_fn(ImageDraw.Draw(im));return im
def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True)
    cases=[]
    def record(key,domain,claim,condition,detail):
        cases.append({"id":key,"domain":domain,"claim":claim,
                      "status":"PASS" if condition else "FAIL","detail":detail})
    # 1: perception spatial structures.
    im=canvas(lambda d:(d.rectangle((5,12,14,24),fill="black"),d.rectangle((38,40,50,53),fill="black")))
    facts=describe(im)
    record("P-01","perception","two separate parts and relation",len(facts["parts"])==2 and len(facts["relations"])==1,
        {"parts":len(facts["parts"]),"relations":len(facts["relations"])})
    # 2: RGB perception.
    red=root/"red.png";blue=root/"blue.png"
    canvas(lambda d:d.rectangle((10,10,43,43),fill="red")).save(red)
    canvas(lambda d:d.rectangle((10,10,43,43),fill="blue")).save(blue)
    r,b=features(red),features(blue)
    record("P-02","perception","RGB evidence differs for red and blue",r["colour_grid"]!=b["colour_grid"],
       {"r_signature_sha":digest(r["colour_grid"]),"b_signature_sha":digest(b["colour_grid"])})
    # 3: view invariance is not asserted; test that rotation changes geometry.
    horizontal=canvas(lambda d:d.rectangle((5,24,55,29),fill="black"))
    vertical=horizontal.transpose(Image.Transpose.ROTATE_90)
    record("V-01","multiview","orientation detection distinguishes rotated shape",
       describe(horizontal)["context"]!=describe(vertical)["context"],
       {"before":describe(horizontal)["context"],"after":describe(vertical)["context"]})
    # 4: generation from representation rather than source.
    output=root/"reconstructed.png";decode([0,0,0]*8+[7,0,0]*8,output)
    with Image.open(output) as rendered:
        generated=rendered.copy()
    record("G-01","generation","produce RGB image from abstract 4x4 learned-format grid",
       generated.size==(64,64) and generated.getpixel((8,8))!=generated.getpixel((8,56)),
       {"rendered":"reconstructed.png","resolution":"64x64","quality":"coarse RGB tiles"})
    # 5: memory refuses two incompatible labels for exactly same evidence.
    state=new_state()
    with Image.open(red) as source:
        image=source.copy()
    image_hash=hashlib.sha256(red.read_bytes()).hexdigest()
    first=remember(state,image_hash,"A",image,"teacher")
    second=remember(state,image_hash,"B",image,"teacher")
    record("M-01","memory","contradictory identity evidence quarantined",
        first=="TEACHER_EXAMPLE_ADDED" and second=="HOLD_CONTRADICTION" and len(state["identities"])==1,
        {"first":first,"second":second})
    # 6: reason about temporal event rather than memorized object label.
    movement=[{"t":i,"x":30.0,"y":y,"radius":3.0} for i,y in enumerate((10,20,30,25))]
    ev=context(movement)
    record("R-01","reasoning","observed direction reversal extracted from successive velocities",
        ev["event"]=="REVERSAL",{"event":ev["event"],"axis":ev["axis"]})
    # 7: prevent exact source evidence from being counted twice in memory.
    dup=remember(state,image_hash,"A",image,"teacher")
    record("E-01","education","identical example not counted as independent lesson",
        dup=="DUPLICATE_NOT_NEW_EVIDENCE" and len(state["seen_hashes"])==1,
        {"outcome":dup})
    # 8: fail closed when generation receives corrupted representation.
    rejected=False
    try:decode([1,2,3],root/"forbidden.png")
    except ValueError:rejected=True
    record("S-01","safety","reject invalid generative memory dimensions",
        rejected and not (root/"forbidden.png").exists(),{"invalid_grid_rejected":rejected})
    # Missing capabilities must not be converted into bogus PASS results.
    todo=[
      ("V-02","multiview","true independent 3D 360-degree transfer"),
      ("G-02","generation","render coherent objects rather than colour mosaics"),
      ("P-03","perception","segment multiple overlapping objects"),
      ("T-01","temporal","learn cause rather than fit temporal movement"),
      ("X-01","exploration","discover licensed external lessons autonomously"),
      ("E-02","education","authenticate independent teacher correction"),
      ("W-01","physical_world","learn physical collision mechanics from real video"),
      ("R-02","reasoning","infer previously unseen invariants on new objects")]
    for key,domain,claim in todo:
        cases.append({"id":key,"domain":domain,"claim":claim,"status":"TODO",
                      "detail":{"reason":"capability absent or not empirically demonstrated"}})
    counts={s:sum(x["status"]==s for x in cases) for s in ("PASS","FAIL","TODO")}
    result={"schema":"BRODY_HETEROGENEOUS_CAPABILITY_AUDIT_P131",
            "distinct_probes":len(cases),"domains":len({x["domain"] for x in cases}),
            "counts":counts,"synthetic_or_constructed_evidence_only":True,
            "real_world_transfer_proven":False,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"}
    evidence={"schema":"BRODY_HETEROGENEOUS_EVIDENCE_P131","cases":cases,"report":result}
    evidence["digest"]=digest(evidence)
    (root/"EVIDENCE.json").write_text(json.dumps(evidence,indent=2)+"\n",encoding="utf-8")
    (root/"MASTER_REPORT.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.out),indent=2))
if __name__=="__main__":main()
