"""BRODY_EXPERIENCE_MEMORY_V1 — code-grounded learning episodes, no authority.

Every record joins the observed teacher image, raster-only interpretation,
method choice, *actual whitelisted* code version/hash, all executed gesture
edits, score deltas, rejects, and a reusable candidate skill. Verifier replays
the stored operations with the pinned local routine, not arbitrary remembered
Python. This is a deterministic learning/provenance audit, not cognition.

Obsidia's native MemoryCandidate/MemoryCandidateLedger remain external;
all artifacts here are LOCAL, read-only candidates. No auto promotion.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any

from PIL import Image
import PIL

from .drawing_school_v0 import SIDE, bbox_of, black_pixels, digest_bytes, signature_for
from .drawing_school_v1 import GestureV1, SkillV1, _error, render

SCHEMA = "BRODY_EXPERIENCE_MEMORY_V1"
INDEX_SCHEMA = "BRODY_EXPERIENCE_INDEX_V1"
REGISTRY_SCHEMA = "BRODY_PROCEDURE_SKILL_REGISTRY_V1"
MAX_EPISODES = 64
MAX_STEPS = 64
ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CAPABILITIES = {
    "image-thinning": ("brody_world_physique/drawing_school_v1.py",
                       "suggest_gestures_from_reference"),
    "pixel-feedback-revision": ("brody_world_physique/drawing_school_v1.py",
                                "correct_drawing"),
    "drawing-motor-render": ("brody_world_physique/drawing_school_v1.py", "render"),
    "image-pixel-comparison": ("brody_world_physique/drawing_school_v0.py",
                               "black_pixels"),
}
NAME_RE = re.compile(r"(cours|examen)_[a-z0-9_]{2,48}$")
KINDS = frozenset(("STRAIGHT_STROKE", "CURVED_STROKE"))
ACTIONS = frozenset(("ADD", "ERASE", "REPLACE"))


def stable_bytes(obj:Any)->bytes:
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,
                      separators=(",",":"),allow_nan=False).encode("utf-8")


def code_fingerprint(capability:str)->dict[str,str]:
    if capability not in ALLOWED_CAPABILITIES:
        raise ValueError("unknown capability: refusing to execute remembered code")
    module,symbol=ALLOWED_CAPABILITIES[capability]
    path=(ROOT/module).resolve(strict=True)
    if ROOT not in path.parents or path.is_symlink():
        raise ValueError("unsafe code reference")
    return {"capability":capability,
            "module_path":module,"symbol":symbol,
            "code_sha256":digest_bytes(path.read_bytes()),
            "version_note":"CURRENT_LOCAL_FILE_CONTENT_SHA256"}


def gesture_snapshot(gesture:GestureV1)->dict:
    # JSON-stable coordinates: dataclasses.asdict keeps tuple values in
    # Python, but serialized receipts must remain verifiable after parsing.
    return {"kind":gesture.kind,"points":[list(p) for p in gesture.points]}


def checked_gesture(value:dict)->GestureV1:
    if not isinstance(value,dict) or set(value)!={"points","kind"}:
        raise ValueError("invalid gesture structure")
    if value["kind"] not in KINDS:
        raise ValueError("unsafe gesture kind")
    points=value["points"]
    if not isinstance(points,(list,tuple)) or not 2<=len(points)<=SIDE*4:
        raise ValueError("invalid number of gesture points")
    parsed=[]
    for point in points:
        if not isinstance(point,(list,tuple)) or len(point)!=2:
            raise ValueError("gesture point not 2D")
        if any(type(v) is not int or not 0<=v<SIDE for v in point):
            raise ValueError("gesture point outside canvas")
        parsed.append(tuple(point))
    return GestureV1(points=tuple(parsed),kind=value["kind"])


def verify_recipe(model:Image.Image, initial:list[dict], trace:list[dict],
                  *, rejected_memory:bool, expected_raw_error:int,
                  expected_blank_error:int, expected_final_error:int)->dict:
    """Independently recompute every edit and score; never eval/exec a code ref."""
    if len(trace)>MAX_STEPS:raise ValueError("trace is unbounded")
    source=black_pixels(model)
    memory=[checked_gesture(g) for g in initial]
    if expected_blank_error!=len(source):
        raise ValueError("blank score altered")
    actual_raw=_error(source,memory)
    if actual_raw!=expected_raw_error:
        raise ValueError("raw remembered score altered")
    should_reject=bool(memory and actual_raw>len(source))
    if rejected_memory!=should_reject:
        raise ValueError("memory rejection gate contradiction")
    drawn=[] if should_reject else list(memory)
    current=_error(source,drawn)
    for i,event in enumerate(trace,1):
        if (not isinstance(event,dict) or event.get("revision")!=i or
            event.get("action") not in ACTIONS or event.get("error_before")!=current or
            event.get("choice_rule")!="MIN_PIXEL_XOR_STRICT_IMPROVEMENT_FIRST_TIE" or
            type(event.get("target_index")) is not int):
            raise ValueError(f"invalid action receipt {i}")
        idx=event["target_index"]
        before=event.get("gesture_before")
        after=event.get("gesture_applied")
        action=event["action"]
        if action=="ADD":
            if idx!=len(drawn) or before is not None or after is None:
                raise ValueError("ADD receipt mismatch")
            drawn.append(checked_gesture(after))
        elif action=="ERASE":
            if not 0<=idx<len(drawn) or after is not None or before is None:
                raise ValueError("ERASE receipt mismatch")
            if stable_bytes(gesture_snapshot(drawn[idx]))!=stable_bytes(before):
                raise ValueError("ERASE source gesture differs")
            drawn.pop(idx)
        else:
            if not 0<=idx<len(drawn) or after is None or before is None:
                raise ValueError("REPLACE receipt mismatch")
            if stable_bytes(gesture_snapshot(drawn[idx]))!=stable_bytes(before):
                raise ValueError("REPLACE source gesture differs")
            drawn[idx]=checked_gesture(after)
        next_error=_error(source,drawn)
        if event.get("error_after")!=next_error or next_error>=current or event.get("strict_improvement") is not True:
            raise ValueError("recipe score does not replay / strict improvement violated")
        if type(event.get("alternatives_evaluated")) is not int or event["alternatives_evaluated"]<1:
            raise ValueError("missing candidate-choice evidence")
        current=next_error
    if current!=expected_final_error:
        raise ValueError("final score does not replay")
    return {"replayed_step_count":len(trace),"replayed_final_pixel_error":current,
            "replayed_gestures":[gesture_snapshot(x) for x in drawn],
            "replayed_png_sha256":None}


def _source_path(root:Path, ref:str)->Path:
    if type(ref) is not str or not NAME_RE.fullmatch(ref):
        raise ValueError("invalid lesson/exam ref")
    return root/"teacher_images"/(ref+".png")


def _output_path(root:Path, ref:str, suffix:str)->Path:
    if suffix not in ("_dessin","_apres_correction"):
        raise ValueError("invalid output role")
    if not NAME_RE.fullmatch(ref):
        raise ValueError("invalid output ref")
    return root/"attempts"/(ref+suffix+".png")


def record_episode(root:Path, *, source_ref:str, trial:dict,
                   memory_source_ref:str|None, is_exam:bool)->dict:
    """Capture only an actual executed trial and artifacts; no invented decisions."""
    root=root.resolve(strict=True)
    source_path=_source_path(root,source_ref)
    final_path=_output_path(root,source_ref,
                            "_apres_correction" if is_exam else "_dessin")
    if not source_path.is_file() or not final_path.is_file():
        raise ValueError("the observed and executed drawing must exist first")
    source=Image.open(source_path).convert("L")
    seen=black_pixels(source)
    if source.size!=(SIDE,SIDE):raise ValueError("unsupported image size")
    raw_memory=trial["initial_gestures"]
    if bool(raw_memory)!=bool(memory_source_ref):
        raise ValueError("memory candidate source was not bound to its replay")
    if trial.get("algorithm_choice_reason")!="PIXEL_ERROR_MINIMIZATION_GIVEN_VISIBLE_REFERENCE":
        raise ValueError("choice provenance missing")
    expected_raw=trial["raw_recall_error"]
    if expected_raw is None:
        expected_raw=len(seen)
    recipe=verify_recipe(
        source,raw_memory,trial["changes"],
        rejected_memory=trial["memory_rejected"],
        expected_raw_error=expected_raw,expected_blank_error=trial["blank_error"],
        expected_final_error=trial["final_error"],
    )
    # Preserve the exact generated artifact, not merely the score.
    drawn=render(tuple(checked_gesture(g) for g in recipe["replayed_gestures"]))
    with Image.open(final_path) as saved:
        if list(saved.convert("L").tobytes())!=list(drawn.tobytes()):
            raise ValueError("saved drawing differs from replayed execution")
    output_bytes=final_path.read_bytes()
    source_digest=digest_bytes(source_path.read_bytes())
    output_digest=digest_bytes(output_bytes)
    procedures=[code_fingerprint(name) for name in (
        "image-thinning","pixel-feedback-revision","drawing-motor-render",
        "image-pixel-comparison",
    )]
    mem_invalid=trial["memory_rejected"]
    rejected_paths=[]
    if mem_invalid:
        rejected_paths.append({
            "kind":"NEGATIVE_SKILL_TRANSFER",
            "memory_ref":memory_source_ref,
            "measured_error_px":expected_raw,
            "blank_error_px":trial["blank_error"],
            "recovery":"HOLD_RECALL_AND_REDRAW_FROM_BLANK",
            "source":"MEASURED",
        })
    if trial["rejected_alternative_evaluations"]:
        rejected_paths.append({
            "kind":"ALTERNATE_EDIT_CANDIDATES",
            "considered_and_not_selected":trial["rejected_alternative_evaluations"],
            "why":"NOT_STRICTLY_BETTER_THAN_FIRST_BEST",
            "individual_choices_stored":False,
            "source":"DETERMINISTIC_COUNTER_NOT_FULL_REASONING_TRACE",
        })
    record={
        "schema_version":SCHEMA,
        "episode_id":source_ref,
        "source_kind":"SIMULATED",
        "produced_kind":"GENERATED",
        "observation":{
            "source_ref":str(source_path.relative_to(root)).replace("\\","/"),
            "source_sha256":source_digest,
            "teacher_source_visible":True,
            "intent":"COPY_VISIBLE_REFERENCE_BY_CORRECTING_PIXEL_ERROR",
            "image_space":"PIXEL_XY_64_64",
            "source_overwritten":False,
        },
        "interpretation":{
            "kind":"RASTER_FEATURE_CANDIDATE",
            "algorithmically_observed_black_pixels":len(seen),
            "observed_bbox":list(bbox_of(seen)),
            "observed_8x8_ink_signature":list(signature_for(seen,bbox_of(seen))),
            "semantic_shape_understood":False,
            "text_interpretation_claim":None,
            "uncertainty":["SYNTHETIC_SOURCE","VISIBLE_REFERENCE_FEEDBACK",
                           "NO_SEMANTIC_REASONING_MODULE"],
        },
        "choice":{
            "selection_author":"DETERMINISTIC_PIXEL_SCORE_ALGORITHM",
            "reason":trial["algorithm_choice_reason"],
            "memory_source_ref":memory_source_ref,
            "recall_gate":"REJECTED_HARMFUL" if mem_invalid else
                          "ACCEPTED_CANDIDATE" if raw_memory else "NO_PRIOR_MEMORY",
            "available_actions":["ADD","ERASE","REPLACE","HOLD"],
            "score":"BINARY_PIXEL_XOR",
            "candidate_gestures_from_raster":trial["proposed_gesture_count"],
            "alternative_edit_candidates_not_selected":trial["rejected_alternative_evaluations"],
            "human_free_choice_claimed":False,
        },
        "procedure_ref":{
            "catalogue":"BRODY_IMAGE_V1_PURE_FUNCTIONS",
            "executed_capabilities":procedures,
            "runtime_parameter_refs":{
                "max_revisions":24,"canvas":[SIDE,SIDE],"brush_width":3,
                "recall_source_hash":None,
            },
            "pillow_version":PIL.__version__,
            "executable_code_embedded_in_memory":False,
            "arbitrary_code_execution_allowed":False,
        },
        "execution_trace":{
            "initial_recalled_gestures":raw_memory,
            "initial_recall_error_px":expected_raw,
            "memory_rejected_before_editing":mem_invalid,
            "operations":trial["changes"],
            "replayed_step_count":recipe["replayed_step_count"],
            "final_gestures":recipe["replayed_gestures"],
            "generated_artifact_ref":str(final_path.relative_to(root)).replace("\\","/"),
            "generated_artifact_sha256":output_digest,
        },
        "evaluation":{
            "evaluator":"EXACT_SOURCE_PIXEL_XOR",
            "blank_page_error_px":trial["blank_error"],
            "raw_recall_error_px":expected_raw if raw_memory else None,
            "after_recall_gate_error_px":trial["error_after_recall_gate"],
            "final_error_px":trial["final_error"],
            "improved_vs_blank":trial["final_error"]<trial["blank_error"],
            "source_pixels_visible_during_correction":True,
            "world_knowledge_validated":False,
            "independent_semantic_evaluation":"NOT_RUN",
            "transfer_causality_proven":False,
        },
        "retained_skill":{
            "status":"CANDIDATE_ONLY",
            "candidate_motor_gestures":recipe["replayed_gestures"],
            "source_sha256":source_digest,
            "transfer_verified_across_independent_sources":False,
            "native_memory_eligible":False,
            "trained_weights":False,
        },
        "rejected_paths":rejected_paths,
        "memory_boundary":{
            "model_of_memory":"LOCAL_EXPERIMENTAL_CANDIDATE_ONLY",
            "memory_write_allowed":False,
            "auto_promotion_allowed":False,
            "kernel_mutation":False,
            "emits_act":False,
            "decision_authority":"KX108_ONLY",
            "obsidia_native_memory_adapter":"NOT_CONNECTED",
        },
    }
    save=root/"experience_episodes_v1"
    save.mkdir(exist_ok=True)
    destination=save/(source_ref+".json")
    if destination.exists():raise ValueError("episode already recorded")
    destination.write_text(json.dumps(record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"episode_ref":str(destination.relative_to(root)),
            "sha256":digest_bytes(destination.read_bytes()),
            "episode_id":source_ref,
            "source_sha256":source_digest,
            "final_error_px":trial["final_error"],
            "memory_rejected":mem_invalid}


def finalize_index(root:Path, episodes:list[dict])->dict:
    root=root.resolve(strict=True)
    if not 1<=len(episodes)<=MAX_EPISODES:raise ValueError("invalid episode count")
    if len({e["episode_id"] for e in episodes})!=len(episodes):
        raise ValueError("duplicate episode")
    registry={
        "schema_version":REGISTRY_SCHEMA,
        "references":[code_fingerprint(x) for x in sorted(ALLOWED_CAPABILITIES)],
        "policies":{
            "execution_whitelist_only":True,"never_import_module_from_memory":True,
            "native_memory_write_allowed":False,"auto_promotion_allowed":False,
            "interpretation_is_observation_only":True,
            "decision_authority":"KX108_ONLY",
        },
    }
    registry_path=root/"procedure_registry_v1.json"
    if registry_path.exists():raise ValueError("registry must be new")
    registry_path.write_text(json.dumps(registry,indent=2)+"\n",encoding="utf-8")
    index={
        "schema_version":INDEX_SCHEMA,
        "episode_count":len(episodes),
        "episodes":episodes,
        "procedure_registry_ref":registry_path.name,
        "procedure_registry_sha256":digest_bytes(registry_path.read_bytes()),
        "read_only_export":True,
        "native_memory_write_allowed":False,
        "auto_promotion_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    path=root/"experience_memory_index_v1.json"
    if path.exists():raise ValueError("memory index must be new")
    path.write_text(json.dumps(index,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return verify_memory_bundle(root)


def verify_episode(root:Path, entry:dict)->dict:
    if not isinstance(entry,dict) or not NAME_RE.fullmatch(entry.get("episode_id","")):
        raise ValueError("invalid episode descriptor")
    ref=entry["episode_id"]
    loc=root/"experience_episodes_v1"/(ref+".json")
    if entry.get("episode_ref")!=str(loc.relative_to(root)) or not loc.is_file():
        raise ValueError("unsafe episode file or missing source")
    if digest_bytes(loc.read_bytes())!=entry.get("sha256"):
        raise ValueError("modified episode receipt")
    data=json.loads(loc.read_text(encoding="utf-8"))
    if data.get("schema_version")!=SCHEMA or data.get("episode_id")!=ref:
        raise ValueError("episode schema/id mismatch")
    if data.get("source_kind")!="SIMULATED" or data.get("produced_kind")!="GENERATED":
        raise ValueError("provenance contradiction")
    boundary=data["memory_boundary"]
    for key in ("memory_write_allowed","auto_promotion_allowed","kernel_mutation","emits_act"):
        if boundary.get(key) is not False:
            raise ValueError("memory or action authority escalation")
    if boundary.get("decision_authority")!="KX108_ONLY":
        raise ValueError("kernel authority mismatch")
    if data["retained_skill"].get("status")!="CANDIDATE_ONLY" or data["retained_skill"].get("native_memory_eligible") is not False:
        raise ValueError("unreviewed canonical promotion")
    procedures=data["procedure_ref"]
    used=procedures.get("executed_capabilities")
    if used!=[code_fingerprint(x) for x in (
        "image-thinning","pixel-feedback-revision","drawing-motor-render",
        "image-pixel-comparison",
    )]:
        raise ValueError("procedure code identity changed; refuse stale replay")
    if procedures.get("executable_code_embedded_in_memory") is not False or procedures.get("arbitrary_code_execution_allowed") is not False:
        raise ValueError("code execution boundary violation")
    if procedures.get("pillow_version")!=PIL.__version__:
        raise ValueError("raster library changed; reproducible replay unverified")
    img=_source_path(root,ref)
    if data["observation"].get("source_ref")!=str(img.relative_to(root)) or not img.is_file():
        raise ValueError("reference image source mismatch")
    if digest_bytes(img.read_bytes())!=data["observation"]["source_sha256"]:
        raise ValueError("source image changed")
    if data["retained_skill"]["source_sha256"]!=data["observation"]["source_sha256"]:
        raise ValueError("retained skill source changed")
    with Image.open(img) as source:
        source=source.convert("L")
        pixels=black_pixels(source)
        if data["interpretation"]["algorithmically_observed_black_pixels"]!=len(pixels):
            raise ValueError("observed raster metrics modified")
        if data["interpretation"]["observed_bbox"]!=list(bbox_of(pixels)):
            raise ValueError("bbox mismatch")
        if data["interpretation"]["observed_8x8_ink_signature"]!=list(signature_for(pixels,bbox_of(pixels))):
            raise ValueError("signature mismatch")
        ev=data["evaluation"]
        rec=data["execution_trace"]
        replayed=verify_recipe(
            source,rec["initial_recalled_gestures"],rec["operations"],
            rejected_memory=rec["memory_rejected_before_editing"],
            expected_raw_error=rec["initial_recall_error_px"],
            expected_blank_error=ev["blank_page_error_px"],
            expected_final_error=ev["final_error_px"],
        )
    if replayed["replayed_gestures"]!=rec["final_gestures"] or replayed["replayed_gestures"]!=data["retained_skill"]["candidate_motor_gestures"]:
        raise ValueError("final gestures not what was executed")
    if replayed["replayed_step_count"]!=rec["replayed_step_count"]:
        raise ValueError("edit sequence length differs")
    expected=_output_path(root,ref,"_apres_correction" if ref.startswith("examen_") else "_dessin")
    if rec["generated_artifact_ref"]!=str(expected.relative_to(root)) or not expected.is_file():
        raise ValueError("untrusted output path")
    if digest_bytes(expected.read_bytes())!=rec["generated_artifact_sha256"]:
        raise ValueError("generated artifact was modified")
    regenerated=render(checked_gesture(g) for g in replayed["replayed_gestures"])
    with Image.open(expected) as observed:
        if observed.convert("L").tobytes()!=regenerated.tobytes():
            raise ValueError("stored drawing pixels do not replay")
    if ev["source_pixels_visible_during_correction"] is not True or ev["world_knowledge_validated"] is not False:
        raise ValueError("untrue knowledge claim")
    return {"episode_id":ref,"verified_edits":replayed["replayed_step_count"],
            "pixel_error":replayed["replayed_final_pixel_error"],
            "procedure_sha_verified":True,"source_sha_verified":True,
            "artifact_sha_verified":True}


def verify_memory_bundle(root:str|Path)->dict:
    root=Path(root).resolve(strict=True)
    path=root/"experience_memory_index_v1.json"
    if not path.is_file():raise ValueError("episode index missing")
    data=json.loads(path.read_text(encoding="utf-8"))
    if (data.get("schema_version")!=INDEX_SCHEMA or data.get("native_memory_write_allowed") is not False
        or data.get("auto_promotion_allowed") is not False or
        data.get("decision_authority")!="KX108_ONLY"):
        raise ValueError("invalid memory boundary")
    entries=data["episodes"]
    if not isinstance(entries,list) or not 1<=len(entries)<=MAX_EPISODES or len(entries)!=data["episode_count"]:
        raise ValueError("unbounded or contradictory episode list")
    if len({e["episode_id"] for e in entries})!=len(entries):
        raise ValueError("duplicate episode ref")
    reg=root/"procedure_registry_v1.json"
    if (data["procedure_registry_ref"]!=reg.name or
        digest_bytes(reg.read_bytes())!=data["procedure_registry_sha256"]):
        raise ValueError("procedure registry tampered")
    registry=json.loads(reg.read_text(encoding="utf-8"))
    if registry["schema_version"]!=REGISTRY_SCHEMA or registry["references"]!=[code_fingerprint(x) for x in sorted(ALLOWED_CAPABILITIES)]:
        raise ValueError("unsafe or stale procedure catalogue")
    if registry["policies"]!={"execution_whitelist_only":True,
                             "never_import_module_from_memory":True,
                             "native_memory_write_allowed":False,
                             "auto_promotion_allowed":False,
                             "interpretation_is_observation_only":True,
                             "decision_authority":"KX108_ONLY"}:
        raise ValueError("procedure authority policy mismatch")
    checked=[verify_episode(root,e) for e in entries]
    return {"status":"PASS_LOCAL_REPLAY_ONLY","episodes":len(checked),
            "edits_verified":sum(x["verified_edits"] for x in checked),
            "code_identity_verified":True,
            "native_memory_modified":False,
            "all_generated_artifacts_replayed":True,
            "world_knowledge_validated":False,
            "episodes_verified":checked}


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Verify bounded Brody image memory episodes without executing remembered code")
    parser.add_argument("--verify",type=Path,required=True)
    args=parser.parse_args(argv)
    print(json.dumps(verify_memory_bundle(args.verify),ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
