"""Brody V4: represent verifiable drawing experiences as MMonde/F12-compatible
candidate world observations, without replacing upstream world or SENS types.

Upstream concepts are owned by obsidia-x108-proofs. Our local contracts_v0
are existing additive, non-sovereign wrappers. All V3 images are SIMULATED
teacher fixtures or GENERATED student outputs, NEVER RealImageObservationV0.

A world view can index facts of an episode, but WORLD_STATE != MEMORY: the
memory is a separate, bounded, readonly candidate linked by source receipts.
No semantic event is executed in SENS; labels and spatial task locations
come from the human-written fixture, not independent visual understanding.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from .contracts_v0 import (
    ExperienceValidationStatusV0,
    MemoryEligibilityV0,
    TransformationEpistemicClassV0,
    WorldExperienceCandidateV0,
    WorldStateDeltaV0,
    WorldTransformationV0,
)
from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes, signature_for
from .drawing_memory_school_v3 import verify_school as verify_v3
from .experience_memory_v1 import stable_bytes

SCHEMA = "BRODY_WORLD_EXPERIENCE_BRIDGE_V4"
EPISODES = ("immediate_pentagon", "delayed_pentagon", "transfer_house")
CODE_PATH = Path(__file__).resolve()


@dataclass(frozen=True)
class _TimeRef:
    observed_at: str


def _sha(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def _observe_pixels(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        gray = image.convert("L")
    if gray.size != (64, 64):
        raise ValueError("unexpected raster dimensions")
    ink = black_pixels(gray)
    if not ink:
        raise ValueError("blank source cannot establish geometry")
    bounds = bbox_of(ink)
    return {
        "ink_pixels": len(ink),
        "bounding_box_xyxy": list(bounds),
        "normalized_8x8_signature": list(signature_for(ink, bounds)),
        "coordinate_frame": "SYNTHETIC_CANVAS_XY_64",
        "depth": None,
        "physical_units": None,
        "semantic_label_predicted": None,
    }


def _spatial_relation_from_instructed_boxes(task: list[dict]) -> dict:
    if len(task) != 2 or {x.get("skill_ref") for x in task} != {
        "cours_triangle", "cours_carre"
    }:
        raise ValueError("fixture does not justify component association")
    roof = next(x for x in task if x["skill_ref"] == "cours_triangle")
    base = next(x for x in task if x["skill_ref"] == "cours_carre")
    a, b, c, d = roof["box"]
    e, f, g, h = base["box"]
    if not (a < c and b < d and e < g and f < h):
        raise ValueError("invalid synthetic part bounds")
    overlap = max(0, min(c, g) - max(a, e))
    return {
        "relation_id": "rel:instructed:roof-over-base",
        "subject_ref": "component:triangle:roof-candidate",
        "object_ref": "component:rectangle:base-candidate",
        "relation_kind": "ABOVE_WITH_HORIZONTAL_OVERLAP" if d <= f and overlap > 0
                         else "UNKNOWN",
        "relation_status": "DERIVED_FROM_TEACHER_PLACEMENT",
        "causal_proven": False,
        "geometry": {
            "roof_box": [a, b, c, d],
            "base_box": [e, f, g, h],
            "x_overlap_px": overlap,
        },
        "inference_source": "EXPLICIT_TEACHER_COMPOSITION_TASK_NOT_AUTONOMOUS_PERCEPTION",
    }


def _canonical_record_of_experience(
    episode: str, outcome: dict, committed: dict, *,
    teacher_path: Path, student_path: Path, run_index: int,
) -> tuple[dict, dict, dict]:
    source_sha = _sha(teacher_path)
    generated_sha = _sha(student_path)
    if generated_sha != committed["output_sha256"] or source_sha != outcome["teacher_sha256"]:
        raise ValueError("V3 source evidence changed")
    state_before = f"world:candidate:{episode}:before"
    state_after = f"world:candidate:{episode}:generated"
    obs_teacher = f"world-observation:simulated-teacher:{episode}"
    obs_student = f"world-observation:generated-pupil:{episode}"
    change = WorldTransformationV0(
        transformation_id=f"transformation:draw:{episode}",
        transformation_kind="DRAW_FROM_STORED_PROCEDURE",
        time=_TimeRef(observed_at=f"simulation-sequence-{run_index:02d}"),
        target_refs=(f"candidate-entity:{episode}",),
        parameters={
            "instrument": committed["instrument_selection"]["chosen_tool"],
            "tool_selector": committed["procedures"]["motor_selection"],
            "gesture_count": len(committed["gestures"]),
        },
        provenance_refs=(f"v3:precommit:{episode}",),
        evidence_refs=(f"sha256:{generated_sha}",),
        epistemic_class=TransformationEpistemicClassV0.SIMULATED,
    )
    delta = WorldStateDeltaV0(
        delta_id=f"delta:teacher-versus-student:{episode}",
        baseline_state_ref=f"world:candidate:{episode}:teacher-heldout",
        observed_world_state_ref=state_after,
        metric_deltas={"binary_pixel_xor": outcome["score"]["pixel_xor"],
                       "teacher_blank_xor": outcome["score"]["blank_pixel_xor"],
                       "pixel_iou": outcome["score"]["pixel_iou"]},
        continuity_status="UNKNOWN",
        explanation_candidates=("RASTER_AND_PROCEDURE_MISMATCH_POSSIBLE",),
        uncertainty=("PIXEL_SCORE_NOT_WORLD_SEMANTICS",
                     "SIMULATED_SOURCE_NOT_REAL_WORLD"),
        provenance_refs=(f"sha256:{source_sha}", f"sha256:{generated_sha}"),
    )
    experiment = WorldExperienceCandidateV0(
        experience_id=f"experience:brody-image:{episode}",
        state_before_ref=state_before,
        state_after_ref=state_after,
        outcome="BETTER_THAN_EMPTY_CANVAS" if outcome["score"]["recall_improves_over_blank"]
                else "NO_IMPROVEMENT_OVER_EMPTY_CANVAS",
        transformation_ref=change.transformation_id,
        delta_ref=delta.delta_id,
        context_refs=(obs_teacher, obs_student),
        replay_refs=(f"v3:student-precommit:{episode}",),
        evidence_refs=(f"sha256:{source_sha}", f"sha256:{generated_sha}"),
        provenance_refs=(f"v3:episode:{episode}",),
        candidate_skill_refs=tuple(
            f"skill:{p['skill_ref']}" for p in (committed["composition_task"] or [])
        ),
        validation_status=ExperienceValidationStatusV0.CANDIDATE,
        memory_eligibility=MemoryEligibilityV0.CANDIDATE_ONLY,
    )
    # Serialize ONLY the canonical local dataclass projections, no second
    # independent WorldExperience/WorldState root class.
    transforms = {
        "schema_version": change.schema_version,
        "transformation_id": change.transformation_id,
        "transformation_kind": change.transformation_kind,
        "time": {"observed_at": change.time.observed_at,
                 "time_basis": "SYNTHETIC_SEQUENCE_NOT_CLOCK"},
        "target_refs": list(change.target_refs),
        "parameters": dict(change.parameters),
        "provenance_refs": list(change.provenance_refs),
        "evidence_refs": list(change.evidence_refs),
        "epistemic_class": change.epistemic_class.value,
        "readonly": change.readonly,
        "execution_authority": change.execution_authority,
        "decision_authority": change.decision_authority,
    }
    deltas = {
        "schema_version": delta.schema_version,
        "delta_id": delta.delta_id,
        "baseline_state_ref": delta.baseline_state_ref,
        "observed_world_state_ref": delta.observed_world_state_ref,
        "metric_deltas": dict(delta.metric_deltas),
        "continuity_status": delta.continuity_status,
        "causal_proof": delta.causal_proof,
        "uncertainty": list(delta.uncertainty),
        "provenance_refs": list(delta.provenance_refs),
        "readonly": delta.readonly,
        "decision_authority": delta.decision_authority,
    }
    memory_candidate = {
        "schema_version": experiment.schema_version,
        "experience_id": experiment.experience_id,
        "state_before_ref": experiment.state_before_ref,
        "state_after_ref": experiment.state_after_ref,
        "outcome": experiment.outcome,
        "transformation_ref": experiment.transformation_ref,
        "delta_ref": experiment.delta_ref,
        "context_refs": list(experiment.context_refs),
        "replay_refs": list(experiment.replay_refs),
        "evidence_refs": list(experiment.evidence_refs),
        "candidate_skill_refs": list(experiment.candidate_skill_refs),
        "validation_status": experiment.validation_status.value,
        "memory_eligibility": experiment.memory_eligibility.value,
        "canonical_memory": experiment.canonical_memory,
        "memory_write_allowed": experiment.memory_write_allowed,
        "auto_promotion_allowed": experiment.auto_promotion_allowed,
        "decision_authority": experiment.decision_authority,
    }
    return transforms, deltas, memory_candidate


def build_candidate_world(v3_dir: str | Path) -> dict:
    root = Path(v3_dir).resolve(strict=True)
    verified = verify_v3(root)
    if verified["episodes_verified"] != 3 or not (
        verified["native_memory_modified"] is False
    ):
        raise ValueError("V3 evidence prerequisite not verified")
    score = json.loads((root / "evaluation.json").read_text(encoding="utf-8"))
    precommit_path = root / "committed_before_teacher_reveal.jsonl"
    entries = [json.loads(s) for s in precommit_path.read_text(encoding="utf-8").splitlines()]
    if tuple(x.get("episode") for x in entries) != EPISODES:
        raise ValueError("unexpected world episode sequence")
    world_observations = []
    graph_edges = []
    experiences = []
    transformations = []
    discrepancies = []
    entities = []
    for i, (ep, item, eval_row) in enumerate(zip(EPISODES, entries, score["results"])):
        if eval_row["episode"] != ep:
            raise ValueError("evaluation and world episode mismatch")
        student_ref = root / "student_images" / (ep + "_drawing.png")
        teacher_ref = root / "teacher_revealed" / (ep + "_reference.png")
        source_sha = _sha(teacher_ref)
        output_sha = _sha(student_ref)
        teacher_geometry = _observe_pixels(teacher_ref)
        output_geometry = _observe_pixels(student_ref)
        # Matching teacher hash across immediate/delayed is evidence of
        # reference continuity, NOT independently recognized object identity.
        identity_group = "candidate-source-sha256:" + source_sha
        entities.append({
            "candidate_entity_ref": f"candidate-entity:{ep}",
            "reference_identity_group": identity_group,
            "identity_link_basis": "EXACT_TEACHER_SOURCE_HASH_ONLY",
            "same_physical_object_proven": False,
            "semantic_type": None,
            "label_source": "TEST_FIXTURE_EPISODE_NAME_ONLY",
        })
        for origin, filepath, geometry, kind, obs_id in (
            ("teacher_reference", teacher_ref, teacher_geometry, "SIMULATED",
             f"world-observation:simulated-teacher:{ep}"),
            ("student_output", student_ref, output_geometry, "GENERATED",
             f"world-observation:generated-pupil:{ep}"),
        ):
            world_observations.append({
                "schema_owner": "OBSIDIA_MMONDE_WORLD_OBSERVATION_V0",
                "compatibility": "STRUCTURAL_READONLY_VIEW_NOT_UPSTREAM_INSTANCE",
                "observation_id": obs_id,
                "entity_ref": f"candidate-entity:{ep}",
                "observed_at": f"simulation-sequence-{i:02d}",
                "time_basis": "SYNTHETIC_SEQUENCE_NOT_CLOCK",
                "source_kind": kind,
                "source_hashes": [_sha(filepath)],
                "source_refs": [filepath.relative_to(root).as_posix()],
                "state": geometry,
                "space": {"frame_ref": "SYNTHETIC_CANVAS_XY_64",
                          "frame_is_physical": False},
                "relations": [],
                "uncertainty": [
                    "NO_INDEPENDENT_SEMANTIC_OBJECT_IDENTITY",
                    "NOT_REAL_WORLD_EVIDENCE",
                ],
                "contradictions": [],
                "evidence_refs": ["sha256:" + _sha(filepath)],
                "causal_status": "UNKNOWN",
                "candidate_reality": True,
                "readonly": True,
                "representation_only": True,
                "memory_object": False,
                "cognition_object": False,
                "allowed_to_decide": False,
                "allowed_to_act": False,
                "decision_authority": "KX108_ONLY",
            })
        transformation, delta, experience = _canonical_record_of_experience(
            ep, eval_row, item, teacher_path=teacher_ref,
            student_path=student_ref, run_index=i,
        )
        transformations.append(transformation)
        discrepancies.append(delta)
        experiences.append(experience)
        graph_edges.extend([
            {"subject_ref": f"world-observation:simulated-teacher:{ep}",
             "object_ref": f"world-observation:generated-pupil:{ep}",
             "relation_kind": "REFERENCE_VERSUS_PRODUCED",
             "relation_status": "DERIVED_FROM_VERIFIED_V3_TEST",
             "causal_proven": False},
            {"subject_ref": f"experience:brody-image:{ep}",
             "object_ref": transformation["transformation_id"],
             "relation_kind": "PROCEDURE_EXECUTED_IN_EXPERIMENT",
             "relation_status": "VERIFIED_BY_LOCAL_REPLAY",
             "causal_proven": False},
        ])
        if ep == "transfer_house":
            graph_edges.append(_spatial_relation_from_instructed_boxes(
                item["composition_task"]
            ))
    a, b = entities[:2]
    continuity_candidate = {
        "from_candidate": a["candidate_entity_ref"],
        "to_candidate": b["candidate_entity_ref"],
        "relation_kind": "CANDIDATE_SAME_REFERENCE_ACROSS_TRIALS"
                         if a["reference_identity_group"] == b["reference_identity_group"]
                         else "UNKNOWN",
        "continuity_basis": "EQUAL_SOURCE_SHA256_NOT_OBJECT_TRACKING",
        "visual_identity_learned": False,
        "physical_identity_proven": False,
        "same_procedure_potentially_reused": True,
        "epistemic_status": "DERIVED",
    }
    graph_edges.append(continuity_candidate)
    return {
        "schema": SCHEMA,
        "source_kind": "SIMULATED_AND_GENERATED",
        "upstream_contract_ownership": {
            "world_observation": "obsidia-x108-proofs/periphery/mmonde/contracts_v0.py",
            "visual_primitive": "obsidia-x108-proofs/periphery/vision/contracts_v0.py",
            "world_dynamics": "obsidia-x108-proofs/periphery/world_dynamics/contracts_v0.py",
            "semantic": "obsidia-x108-proofs/app/semantic/lattice",
            "native_memory": "EXTERNAL_NOT_WRITTEN",
        },
        "views": {
            "world_observations": world_observations,
            "candidate_entities": entities,
            "typed_candidate_relations": graph_edges,
            "transformations": transformations,
            "world_state_deltas": discrepancies,
        },
        "experience_candidates": experiences,
        "provenance": {
            "v3_evaluation_sha256": _sha(root / "evaluation.json"),
            "v3_precommit_sha256": _sha(precommit_path),
            "v4_code_sha256": _sha(CODE_PATH),
            "v3_replay_verified": True,
        },
        "semantic_boundary": {
            "sens_pipeline_executed": False,
            "semantic_event_generated": False,
            "occurrence_claim_generated": False,
            "relation_above_is_derived_from_instructed_boxes": True,
            "candidate_labels_are_not_object_recognition": True,
            "knowledge_promoted": False,
            "world_state_is_memory": False,
            "timestamp_as_freshness_authority": False,
            "causal_proof_claimed": False,
        },
        "readonly": True,
        "canonical_world_state_constructed": False,
        "native_memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
    }


def verify_world_bundle(v3_dir: str | Path, bundle_path: str | Path) -> dict:
    path = Path(bundle_path).resolve(strict=True)
    actual = json.loads(path.read_text(encoding="utf-8"))
    expected = build_candidate_world(v3_dir)
    if stable_bytes(actual) != stable_bytes(expected):
        raise ValueError("candidate world inconsistent with verified V3 source/code")
    return {
        "status": "PASS_WORLD_VIEW_DERIVED_FROM_VERIFIED_EXPERIENCES",
        "world_observations": len(actual["views"]["world_observations"]),
        "candidate_experiences": len(actual["experience_candidates"]),
        "relation_candidates": len(actual["views"]["typed_candidate_relations"]),
        "v3_replayed": True,
        "sens_runtime_executed": False,
        "world_understanding_proven": False,
        "native_memory_write_allowed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create/replay a candidate world view derived from V3 visual experiences"
    )
    parser.add_argument("--v3", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args(argv)
    if bool(args.out) == bool(args.verify):
        parser.error("exactly one of --out or --verify required")
    if args.verify:
        report = verify_world_bundle(args.v3, args.verify)
    else:
        file = args.out.resolve()
        if file.exists():
            raise ValueError("world view output must be new")
        file.parent.mkdir(parents=True, exist_ok=True)
        generated = build_candidate_world(args.v3)
        file.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        report = verify_world_bundle(args.v3, file) | {"output": str(file)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
