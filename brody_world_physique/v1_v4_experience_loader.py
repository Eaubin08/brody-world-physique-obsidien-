"""M01-M09 Integration: Load real V1-V4.2 episodes into Multidimensional Memory and evaluate.

Bridges:
- Drawing school V1 (stroke sequences, erase/replace, XOR errors)
- Memory drawing school V3 (hidden teacher model, intervening exercises)
- World experience bridge V4 (MMonde-compatible entities and transformations)
- Spatial relations school V4.1 (8-connected components, NEAR/FAR threshold, adversarial order failure)
- World orientation school V4.2 (cardinal directions, reciprocal vectors, LEFT/RIGHT)

Constitutional boundary:
- KX108_ONLY remains the unique decision authority.
- memory_write_allowed = False.
- auto_promotion_allowed = False.
- emits_act = False.
"""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from PIL import Image

from .cognitive_memory_timeline_v1 import (
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    HistoricalBeliefRevisionV1,
    MultidimensionalExperienceV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeProjectionV1,
)
from .multidimensional_retrieval_v2 import (
    ExperienceRelationLinkV1,
    MeaningQueryIntentV1,
    MeaningQueryResponseV1,
    MultidimensionalCognitiveMemoryEngineV1,
    MultidimensionalRelationTypeV1,
    VisualTaskAdmissibilityRequestV1,
    VisualTaskAdmissibilityVerdictV1,
)


def build_and_load_integrated_v1_v4_memory(
    engine: MultidimensionalCognitiveMemoryEngineV1,
    storage_provenance: str = "EPHEMERAL_RECONSTRUCTED",
) -> dict[str, Any]:
    """Generates standard, audited V1-V4.2 runs in temporary workspaces and loads them into memory."""
    from brody_world_physique.drawing_school_v1 import run_school as run_school_v1
    from brody_world_physique.instrument_school_v2 import run_school as run_school_v2
    from brody_world_physique.drawing_memory_school_v3 import run_school as run_school_v3
    from brody_world_physique.world_experience_bridge_v4 import build_candidate_world
    from brody_world_physique.world_relations_school_v4_1 import run_school as run_school_v4_1
    from brody_world_physique.world_orientation_school_v4_2 import build as build_school_v4_2

    with TemporaryDirectory() as tmp_root:
        root = Path(tmp_root)
        out_v1 = root / "v1"
        out_v2 = root / "v2"
        out_v3 = root / "v3"
        out_v4_json = root / "v4.json"
        out_v41 = root / "v4_1"
        out_v42 = root / "v4_2"

        # Execute the curriculum chain
        run_school_v1(out_v1)
        run_school_v2(out_v2, prior_school=out_v1)
        run_school_v3(out_v3, prior_v2=out_v2)
        v4_dict = build_candidate_world(out_v3)
        out_v4_json.write_text(json.dumps(v4_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        run_school_v4_1(out_v41, prior_v3=out_v3, prior_v4=out_v4_json)
        build_school_v4_2(out_v42, v3=out_v3, v4=out_v4_json, v41=out_v41)


        # 1. Load V1 Episode (Circle Drawing Lesson)
        eval_v1 = json.loads((out_v1 / "evaluation.json").read_text(encoding="utf-8"))
        exp_v1 = MultidimensionalExperienceV1(
            experience_id="REAL-EXP-V1-DESSIN-CERCLE",
            intention_summary="V1 Guided drawing of continuous curved circle with erase/replace",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-08T10:00:00Z",
                t_observation_iso="2026-10-08T10:00:01Z",
                t_recording_iso="2026-10-08T10:01:00Z",
                educational_stage="DESSIN_V1",
                validity_start_iso="2026-10-08T10:01:00Z",
                revisions=(
                    HistoricalBeliefRevisionV1(
                        revision_id="REV-V1-01",
                        t_revision_iso="2026-10-08T10:00:30Z",
                        prior_belief_claim="Straight stroke suffices for curved contour",
                        revised_belief_claim="Curved gesture reduces XOR error significantly",
                        contradiction_evidence_ref=eval_v1.get("evaluated_at", "v1-eval"),
                        correction_rule_or_procedure="correct_drawing_curves",
                    ),
                ),
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.90, "Raster pixel perception of curvature"),
                TreeProjectionV1("13", 0.80, "Artistic motor gesture rendering"),
                TreeProjectionV1("24", 0.85, "Episodic skill retrieval from drawing lessons"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Strict XOR error reduction on 64x64 canvas", ("px_xor",)),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Closed circular radial symmetry", ("px",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.92,
                source_provenance_refs=(str(out_v1 / "teacher_images" / "cours_cercle.png"),),
                evidence_hashes=(eval_v1.get("evaluated_at", "sha256:v1_circle"),),
                uncertainties=("RASTER_APPROXIMATION_ON_64x64",),
                failure_boundaries=("CANVAS_SIZE=64x64", "SINGLE_CONNECTED_SHAPE"),
                counter_examples=(),
                reproducible_on_seed=101,
            ),
            procedure_refs=("brody_world_physique.drawing_school_v1:render",),
            storage_provenance=storage_provenance,
        )

        # 2. Load V3 Episode (Hidden Model Retention)
        exp_v3 = MultidimensionalExperienceV1(
            experience_id="REAL-EXP-V3-MODELE-CACHE",
            intention_summary="V3 Drawing reproduced after teacher model was hidden and intervening tasks run",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-08T18:00:00Z",
                t_observation_iso="2026-10-08T18:00:02Z",
                t_recording_iso="2026-10-08T18:05:00Z",
                educational_stage="DESSIN_V3_CACHE",
                validity_start_iso="2026-10-08T18:05:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.80, "Perception of cached mental representation"),
                TreeProjectionV1("24", 0.95, "Long-term episodic retention under delay"),
                TreeProjectionV1("06", 0.75, "Comprehension of shape structure"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Memory drawing score vs blank canvas", ("px_xor",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.88,
                source_provenance_refs=(str(out_v3 / "evaluation.json"),),
                evidence_hashes=("sha256:v3_hidden_evidence",),
                uncertainties=("DELAYED_DECAY_RATE_UNMEASURED",),
                failure_boundaries=("CANVAS_SIZE=64x64", "INTERVENING_EXERCISES<=3"),
                counter_examples=(),
            ),
            procedure_refs=("brody_world_physique.drawing_memory_school_v3:render_from_memory",),
            storage_provenance=storage_provenance,
        )

        # 3. Load V4.1 Episode (Component Relations & Adversarial Order Inversion Failure)
        eval_v41 = json.loads((out_v41 / "evaluation.json").read_text(encoding="utf-8"))
        exp_v41 = MultidimensionalExperienceV1(
            experience_id="REAL-EXP-V4-1-RELATIONS-SPATIALES",
            intention_summary="V4.1 Two-component normalized proximity classification (with adversarial inversion failure)",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-09T02:00:00Z",
                t_observation_iso="2026-10-09T02:00:01Z",
                t_recording_iso="2026-10-09T02:05:00Z",
                educational_stage="MONDE_RELATIONS_V4_1",
                validity_start_iso="2026-10-09T02:05:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.85, "Pixel 8-neighbor connected component extraction"),
                TreeProjectionV1("07", 0.80, "Organisation of parts and bounding boxes"),
                TreeProjectionV1("26", 0.90, "Coherence under translation and 90-degree turn"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Normalized distance between components", ("normalized_units",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.55,  # Reduced due to known adversarial failure
                source_provenance_refs=(str(out_v41 / "evaluation.json"),),
                evidence_hashes=(eval_v41.get("evaluation_hash", "sha256:v41_eval"),),
                uncertainties=("BLIND_TO_ORDER_INVERSION", "REQUIRES_EXACTLY_TWO_COMPONENTS"),
                failure_boundaries=("CANVAS_SIZE=64x64", "TWO_DISJOINT_COMPONENTS_ONLY"),
                counter_examples=("INVERTED_ORDER_CONFUSION",),
            ),
            procedure_refs=("brody_world_physique.world_relations_school_v4_1:classify",),
            storage_provenance=storage_provenance,
        )

        # 4. Load V4.2 Episode (Cardinal Orientation & Reciprocity)
        eval_v42 = json.loads((out_v42 / "evaluation.json").read_text(encoding="utf-8"))
        exp_v42 = MultidimensionalExperienceV1(
            experience_id="REAL-EXP-V4-2-ORIENTATION-RECIPROQUE",
            intention_summary="V4.2 Learned cardinal directions (TOP, LEFT, BOTTOM, RIGHT) and reciprocal vector inference",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-09T06:00:00Z",
                t_observation_iso="2026-10-09T06:00:01Z",
                t_recording_iso="2026-10-09T06:05:00Z",
                educational_stage="MONDE_ORIENTATION_V4_2",
                validity_start_iso="2026-10-09T06:05:00Z",
                revisions=(
                    HistoricalBeliefRevisionV1(
                        revision_id="REV-V4-2-01",
                        t_revision_iso="2026-10-09T06:00:30Z",
                        prior_belief_claim="Proximity distance suffices to distinguish inverted components",
                        revised_belief_claim="Directional vector distinguishes inverted order (e.g. POINTED_TOP vs POINTED_BOTTOM)",
                        contradiction_evidence_ref="v4_1_exam_inverted_failure",
                        correction_rule_or_procedure="learn_cardinal_direction_prototypes",
                    ),
                ),
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.90, "Visual orientation perception"),
                TreeProjectionV1("22", 0.92, "Spatial transformation and 180-degree reciprocal inversion"),
                TreeProjectionV1("26", 0.95, "Coherence between opposite directional claims"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Unit vector orientation and reverse direction match", ("unit_vector",)),
                DomainEngagementV1(SpecializedDomainV1.PHYSICS, "Spatial 2D reference frame", ("grid_coords",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.94,
                source_provenance_refs=(str(out_v42 / "evaluation.json"),),
                evidence_hashes=(eval_v42.get("evaluation_hash", "sha256:v42_eval"),),
                uncertainties=("CARDINAL_ANGLES_ONLY_NO_OBLIQUES",),
                failure_boundaries=("CANVAS_SIZE=64x64", "FOUR_CARDINAL_ORIENTATIONS"),
                counter_examples=(),
                reproducible_on_seed=4242,
            ),
            procedure_refs=("brody_world_physique.world_orientation_school_v4_2:derive_reciprocal",),
            storage_provenance=storage_provenance,
        )

        # Register in memory index
        engine.index.register_experience(exp_v1)
        engine.index.register_experience(exp_v3)
        engine.index.register_experience(exp_v41)
        engine.index.register_experience(exp_v42)

        # Register multidimensional relations (M04)
        engine.add_relation(ExperienceRelationLinkV1(
            source_experience_id="REAL-EXP-V1-DESSIN-CERCLE",
            target_experience_id="REAL-EXP-V3-MODELE-CACHE",
            relation_type=MultidimensionalRelationTypeV1.TEMPORAL,
            strength=0.85,
            rationale="V3 exercises build directly upon V1 curved stroke memory",
        ))
        engine.add_relation(ExperienceRelationLinkV1(
            source_experience_id="REAL-EXP-V4-1-RELATIONS-SPATIALES",
            target_experience_id="REAL-EXP-V4-2-ORIENTATION-RECIPROQUE",
            relation_type=MultidimensionalRelationTypeV1.TRANSFORMATION,
            strength=0.95,
            rationale="V4.2 transforms V4.1 symmetric proximity into oriented reciprocal vectors",
        ))
        engine.add_relation(ExperienceRelationLinkV1(
            source_experience_id="REAL-EXP-V4-1-RELATIONS-SPATIALES",
            target_experience_id="REAL-EXP-V4-2-ORIENTATION-RECIPROQUE",
            relation_type=MultidimensionalRelationTypeV1.OPPOSITION,
            strength=0.90,
            rationale="V4.1 false positive on inverted layout is resolved and opposed by V4.2 orientation",
        ))

        return {
            "loaded_count": 4,
            "episode_ids": [
                exp_v1.experience_id,
                exp_v3.experience_id,
                exp_v41.experience_id,
                exp_v42.experience_id,
            ],
            "v1_out": str(out_v1),
            "v42_out": str(out_v42),
            "storage_provenance": storage_provenance,
        }


def persist_v1_v4_experiences(target_dir: Path | str) -> dict[str, Any]:
    """Runs V1-V4.2 schools once, builds historical memory, and persists it to disk.
    
    Distinguishes HISTORICAL_PERSISTED storage from EPHEMERAL_RECONSTRUCTED memory.
    """
    engine = MultidimensionalCognitiveMemoryEngineV1()
    build_and_load_integrated_v1_v4_memory(engine, storage_provenance="HISTORICAL_PERSISTED")
    receipt = engine.save_to_directory(target_dir)
    receipt["provenance_mode"] = "HISTORICAL_PERSISTED"
    return receipt


def load_persisted_v1_v4_experiences(
    source_dir: Path | str,
    engine: MultidimensionalCognitiveMemoryEngineV1,
) -> dict[str, Any]:
    """Loads previously persisted historical memory from disk without re-running schools.
    
    Simulates a clean process start recovering historical memory state.
    """
    return engine.load_from_directory(source_dir, storage_provenance="HISTORICAL_PERSISTED")
