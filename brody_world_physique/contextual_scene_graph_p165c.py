"""P165-C: contextual scene relation graph lab. No real sensor or canonical binding."""
import argparse,json
from pathlib import Path
from .modal_signature_fusion_p165b import obs,identity

RELATIONS=("IN_FRONT_OF","BEHIND","OCCLUDES","OVERLAPS","UNKNOWN")
def node(name,observations=(),frame="scene",time_id=0):
    return {"id":name,"observations":list(observations),"frame":frame,"time_id":time_id}
def edge(a,b,relation,source="SIMULATED",evidence=()):
    if relation not in RELATIONS:raise ValueError("RELATION_INVALID")
    return {"a":a,"b":b,"relation":relation,"source":source,"evidence":list(evidence)}
def assess(nodes,edges):
    ids={x["id"] for x in nodes}
    if len(ids)!=len(nodes):return {"status":"HOLD","reason":"DUPLICATE_ENTITY"}
    if any(e["a"] not in ids or e["b"] not in ids for e in edges):
        return {"status":"HOLD","reason":"DANGLING_EDGE"}
    contradictions=[]
    known={}
    for e in edges:
        if e["relation"]=="UNKNOWN":continue
        pair=(e["a"],e["b"])
        prior=known.get(pair)
        if prior and prior!=e["relation"]:contradictions.append({"pair":pair,"values":[prior,e["relation"]]})
        known[pair]=e["relation"]
        inverse={"IN_FRONT_OF":"BEHIND","BEHIND":"IN_FRONT_OF","OCCLUDES":"BEHIND"}
        other=known.get((e["b"],e["a"]))
        if other and e["relation"] in inverse and other!=inverse[e["relation"]]:
            contradictions.append({"pair":pair,"reverse":other,"relation":e["relation"]})
    return {"status":"MULTI" if contradictions else ("HOLD" if not known else "SCENE_CANDIDATE"),
            "relations":list(known.items()),"contradictions":contradictions,
            "metric_depth_proven":False}
def fuse_scene(a,b,edges):
    graph=assess([a,b],edges)
    modalities=identity(a["observations"],b["observations"])
    # Scene topology and identity agreement are different claims.
    if graph["status"]=="MULTI" or modalities["status"]=="MULTI":decision="MULTI"
    elif graph["status"]=="HOLD" or modalities["status"]=="HOLD":decision="HOLD"
    else:decision="SCENE_CANDIDATE"
    return {"status":decision,"graph":graph,"signature":modalities,
            "unique_identity_proven":False,"physical_depth_proven":False}
def fixture(case):
    a=node("A",[obs("RGB",[.8,.1,.1]),obs("GEOMETRY",[.2,.3])])
    b=node("B",[obs("RGB",[.8,.1,.1]),obs("GEOMETRY",[.2,.3])])
    if case=="occlusion_order":
        es=[edge("A","B","OCCLUDES",evidence=["pixel_overlap"])]
    elif case=="depth_unknown":
        es=[edge("A","B","UNKNOWN")]
    elif case=="contradictory_order":
        es=[edge("A","B","IN_FRONT_OF"),edge("A","B","BEHIND")]
    elif case=="camera_ambiguity":
        es=[]
    elif case=="modal_conflict":
        b["observations"][0]=obs("RGB",[.1,.8,.8])
        es=[edge("A","B","OVERLAPS")]
    elif case=="identity_indistinguishable":
        es=[edge("A","B","OVERLAPS")]
    elif case=="frame_mismatch":
        b["frame"]="camera"
        b["observations"]=[obs("RGB",[.8,.1,.1],frame="camera"),obs("GEOMETRY",[.2,.3],frame="camera")]
        es=[edge("A","B","UNKNOWN")]
    else:raise ValueError("UNKNOWN_CASE")
    return a,b,es
CASES=("occlusion_order","depth_unknown","contradictory_order","camera_ambiguity",
       "modal_conflict","identity_indistinguishable","frame_mismatch")
def run(out):
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    result={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf-8") as file:
        for case in CASES:
            a,b,edges=fixture(case)
            v=fuse_scene(a,b,edges)
            result[case]=v["status"]
            file.write(json.dumps({"case":case,"nodes":[a,b],"edges":edges,"decision":v})+"\n")
    report={"schema":"BRODY_P165C_CONTEXTUAL_SCENE_GRAPH_LAB","cases":result,
        "cases_completed":len(result),"scene_graph_semantics":"CANDIDATES_ONLY",
        "layer_count_fixed":False,"metric_depth_proven":False,
        "natural_image_segmentation_connected":False,"camera_estimation_connected":False,
        "hardware_sensor_connected":False,"real_f12_f16_mmonde_runtime_connected":False,
        "legacy_77_p165a_150_not_replayed":True,
        "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.out),indent=2))
if __name__=="__main__":main()
