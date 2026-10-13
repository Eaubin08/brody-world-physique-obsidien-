"""Local candidate knowledge graph joining teacher identity, views, and taught reflex.

Only teacher-confirmed identities are grouped; geometric transformations yield
observations, not automatic semantic identity. Never writes Native Memory.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from .image_external_source_school_v0 import reference
from .image_multiview_identity_school_v0 import views,VIEWS
from .image_structural_observation_v1 import describe
from .image_stabilized_knowledge_school_v1 import fresh,observe,apply
from .fusion_f9_intensive_education_v0 import digest,verify_chain

def build(manifest,out):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PREVIOUS_EVIDENCE")
    groups=json.loads(Path(manifest).read_text(encoding="utf-8-sig"))
    if isinstance(groups,dict):groups=[groups]
    if not isinstance(groups,list) or not groups:raise ValueError("NO_TEACHER_GROUPS")
    # Validate before creating any output.
    identities=set()
    for g in groups:
        if not isinstance(g,dict) or not isinstance(g.get("identity"),str) or not g["identity"].strip() or g["identity"] in identities:
            raise ValueError("BAD_IDENTITY")
        if not isinstance(g.get("examples"),list) or not g["examples"]:raise ValueError("NO_EXAMPLES")
        identities.add(g["identity"])
    state=fresh()
    graph={"schema":"BRODY_CANDIDATE_VISUAL_KNOWLEDGE_GRAPH_V1",
           "identities":{},"observations":{},"transforms":[],"relations":[],
           "native_memory_write":False,"canonical_promotion":False,
           "decision_authority":"KX108_ONLY"}
    events=[];prior=None
    for group in groups:
        identity=group["identity"]
        graph["identities"][identity]={"origin":"TEACHER_LABEL_UNVERIFIED",
            "observation_refs":[],"status":"TAUGHT_CANDIDATE",
            "known_views":["identity","mirror"],"unseen_views":["quarter_turn","half_turn"]}
        for source in group["examples"]:
            p=Path(source);h=hashlib.sha256(p.read_bytes()).hexdigest()
            im=reference(p)
            for view in VIEWS:
                transformed=views(im,view);facts=describe(transformed)
                oid=hashlib.sha256((identity+"|"+h+"|"+view).encode()).hexdigest()[:20]
                if oid in graph["observations"]:continue
                role="LESSON" if view in ("identity","mirror") else "EXAM"
                graph["observations"][oid]={"identity_ref":identity,"source_sha256":h,
                   "view":view,"role":role,"context":facts["context"],
                   "properties":facts["properties"],"parts":facts["parts"],
                   "spatial_relations":facts["relations"]}
                graph["identities"][identity]["observation_refs"].append(oid)
                graph["transforms"].append({"observation_ref":oid,"kind":view,
                    "epistemic_class":"SIMULATED_2D"})
                graph["relations"].append({"subject":oid,"predicate":"TAUGHT_AS_VIEW_OF",
                    "object":identity,"provenance":"TEACHER_MANIFEST"})
                if role=="LESSON":
                    # Teach one invariant *identity label*, not a pixel strategy.
                    # The reusable action remains bounded to a whitelisted reflex.
                    key="identity:"+identity
                    existing=state["concepts"].get(key,{}).get("lessons",[])
                    if not any(x["example_ref"]==oid for x in existing):
                        observe(state,key,"raw","teacher-manifest",oid)
                event={"index":len(events)+1,"previous":prior,"observation_ref":oid,
                       "identity_ref":identity,"role":role,"view":view,
                       "native_memory_write":False,"canonical_promotion":False,
                       "decision_authority":"KX108_ONLY"}
                event["digest"]=digest(event);prior=event["digest"];events.append(event)
    for identity,data in graph["identities"].items():
        key="identity:"+identity
        taught=state["concepts"].get(key)
        data["procedural_state"]=taught["status"] if taught else "UNTAUGHT"
        # Two train views of a single file cannot make a reliable new
        # semantic identity, even if local reflex-state says LEARNING.
        data["semantic_identity_verified"]=False
        data["available_action"]=apply(state,key)["mode"]
    dest.mkdir(parents=True)
    with (dest/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for event in events:f.write(json.dumps(event,sort_keys=True)+"\n")
    n,tip=verify_chain(dest/"receipts.jsonl")
    graph["receipt_tip"]=tip
    graph["digest"]=digest(graph)
    (dest/"knowledge_graph_candidates.json").write_text(json.dumps(graph,indent=2)+"\n",encoding="utf-8")
    report={"schema":"BRODY_UNIFIED_MULTIVIEW_KNOWLEDGE_V1",
            "identities":len(graph["identities"]),"observations":len(graph["observations"]),
            "relations":len(graph["relations"]),"receipts":n,"receipt_tip":tip,
            "semantic_identity_verified":False,"real_3d_proven":False,
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY",
            "status":"TEACHER_GROUPED_LOCAL_KNOWLEDGE_GRAPH_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(build(a.manifest,a.out),indent=2))
if __name__=="__main__":main()
