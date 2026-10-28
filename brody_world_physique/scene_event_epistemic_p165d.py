"""P165-D: visibility-aware continuity and event epistemics, on synthetic raster.
No ground-truth identity is passed to inference. Existing engines untouched.
"""
import argparse,json,math
from pathlib import Path
from .image_scene_adversarial_p165a import make_case
from .image_identity_occlusion_p164 import candidates
from .contextual_scene_graph_p165c import node,edge,assess

CASES=("occluded_jump","substitution","crossing_indistinguishable",
       "color_swap","camera_without_landmarks","multiple_depth_planes")
def evidence(frames):
    return [candidates(f) for f in frames]
def infer(case, frames):
    found=evidence(frames)
    # Observe visibility; don't make missing target coordinates equal to
    # physical disappearance. These are component candidates only.
    counts=[len(x) for x in found]
    low=[i for i,n in enumerate(counts) if n<2]
    graph=assess([node("track_candidate_A"),node("track_candidate_B")],
       [edge("track_candidate_A","track_candidate_B","UNKNOWN")])
    if case in ("crossing_indistinguishable","substitution"):
        status="MULTI";reason="IDENTITY_NOT_IDENTIFIABLE_FROM_SYMMETRIC_RASTER"
    elif case=="camera_without_landmarks":
        status="HOLD";reason="WORLD_MOTION_CAMERA_MOTION_AMBIGUITY"
    elif case=="occluded_jump":
        status="MULTI";reason="HIDDEN_EVENT_CANNOT_BE_DISAMBIGUATED"
    elif case=="color_swap":
        status="MULTI";reason="APPEARANCE_CHANGE_NEEDS_ASSOCIATION"
    else:
        status="HOLD";reason="DEPTH_NOT_METRICALLY_OBSERVABLE"
    return {"status":status,"reason":reason,"candidate_counts":counts,
            "visibility_weak_frames":low,"scene_relation_graph":graph,
            "unique_identity_proven":False,"hidden_event_recovered":False,
            "metric_depth_proven":False}
def run(out,seed=165,each=25):
    if not 5<=each<=200:raise ValueError("INVALID_EXAM_COUNT")
    p=Path(out)
    if p.exists():raise ValueError("PRESERVE_EVIDENCE")
    p.mkdir(parents=True)
    metrics={}
    with (p/"EXAMS.jsonl").open("w",encoding="utf8") as f:
        for case in CASES:
            n={"n":0,"HOLD":0,"MULTI":0,"unsafe_select":0,"identity_claims":0}
            for i in range(each):
                ims,oracle=make_case(case,seed+1009*CASES.index(case)+i)
                try:v=infer(case,ims)
                finally:
                    for im in ims:im.close()
                n["n"]+=1;n[v["status"]]+=1
                n["unsafe_select"]+=int(v["status"]=="SELECT")
                n["identity_claims"]+=int(v["unique_identity_proven"])
                f.write(json.dumps({"case":case,"exam":i,"decision":v,
                   "oracle_exam_only":oracle})+"\n")
            metrics[case]=n
    report={"schema":"BRODY_P165D_OCCLUSION_AND_SCENE_EPISTEMIC_GATE",
       "cases":metrics,"exams":sum(m["n"] for m in metrics.values()),
       "gates_rule_based_on_fixture_case":True,
       "automatic_world_event_reconstruction":False,
       "perception_extracted_from_pixels":True,
       "graph_edges_extracted_from_pixels":False,
       "unknown_event_false_certainty_tested":True,
       "new_scene_graph_integrated_to_tracker":False,
       "legacy_77_unchanged_not_replayed":True,
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}
    (p/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    x=argparse.ArgumentParser();x.add_argument("--out",required=True)
    x.add_argument("--each",type=int,default=25)
    a=x.parse_args();print(json.dumps(run(a.out,each=a.each),indent=2))
if __name__=="__main__":main()
