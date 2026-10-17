"""Tests for G01 (Visual Edit Intent), O01 (Bounded Orchestrator), and G02 (Diffusion Adapter with Hardware Barrier)."""

import pytest
from PIL import Image, ImageDraw

from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    PropertyConstraintV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualComplianceReportV1,
    VisualEditIntentCandidateV1,
)
from brody_world_physique.bounded_orchestrator_v1 import (
    ALLOWED_CAPABILITIES,
    BoundedInstrumentOrchestratorV1,
    OrchestrationPlanV1,
    ToolExecutionReceiptV1,
    ToolExecutionStepV1,
)
from brody_world_physique.diffusion_generator_adapter_v1 import (
    DiffusionGeneratorAdapterV1,
    GeneratedArtifactV0,
    HardwareProfileV1,
    HeavyDiffusionDownloadBlockedError,
    probe_hardware_profile,
)


class TestG01VisualIntentContracts:
    """Validation of G01 Visual Edit Intent Candidate contracts."""

    def test_intent_creation_and_constitutional_bounds(self):
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-TEST-01",
            goal_description="Draw a circle while preserving background and top header",
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=(
                RegionConstraintV1("HEADER", (0, 0, 64, 10), ConstraintKindV1.LOCK, 0.0),
                RegionConstraintV1("BODY", (0, 10, 64, 54), ConstraintKindV1.FLEX, 50.0),
                RegionConstraintV1("FOOTER", (0, 54, 64, 64), ConstraintKindV1.IGNORE),
            ),
            property_constraints=(
                PropertyConstraintV1("orientation", ConstraintKindV1.LOCK, "TOP"),
                PropertyConstraintV1("stroke_count", ConstraintKindV1.FLEX, 4, 2.0),
            ),
        )

        assert intent.decision_authority == "KX108_ONLY"
        assert intent.readonly is True
        assert intent.is_candidate is True

    def test_compliance_detects_lock_violation(self):
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-TEST-LOCK",
            goal_description="Protect top-left corner",
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=(
                RegionConstraintV1("TOP_LEFT", (0, 0, 16, 16), ConstraintKindV1.LOCK),
            ),
        )

        before = Image.new("L", (64, 64), 255)
        after = before.copy()
        draw = ImageDraw.Draw(after)
        draw.point((5, 5), fill=0)  # Violate locked region

        report = intent.check_compliance(before, after)
        assert report.compliant is False
        assert len(report.lock_violations) == 1
        assert "Region TOP_LEFT altered" in report.lock_violations[0]

    def test_compliance_flex_and_ignore(self):
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-TEST-FLEX",
            goal_description="Flexible center with ignored corner",
            rigor_profile=RigorProfileV1.PERMISSIVE_STYLE,
            region_constraints=(
                RegionConstraintV1("CENTER", (16, 16, 48, 48), ConstraintKindV1.FLEX, 0.20),
                RegionConstraintV1("CORNER", (0, 0, 16, 16), ConstraintKindV1.IGNORE),
            ),
        )

        before = Image.new("L", (64, 64), 255)
        after = before.copy()
        draw = ImageDraw.Draw(after)
        # Modify corner (ignored)
        draw.rectangle([0, 0, 15, 15], fill=0)
        # Modify 5 pixels in center (total 32x32 = 1024 px, 5/1024 << 0.20)
        for i in range(5):
            draw.point((20 + i, 20), fill=0)

        report = intent.check_compliance(before, after)
        assert report.compliant is True
        assert "CORNER" in report.ignored_inspections


class TestO01BoundedOrchestrator:
    """Validation of O01 Bounded Instrument Orchestrator."""

    def test_catalog_forbids_arbitrary_code(self):
        with pytest.raises(ValueError, match="Disallowed tool capability: EXEC_CODE"):
            ToolExecutionStepV1(
                step_index=0,
                capability="EXEC_CODE",
                arguments={"code": "import os; os.system('echo dangerous')"},
            )

        with pytest.raises(ValueError, match="Disallowed tool capability: EVAL"):
            ToolExecutionStepV1(
                step_index=0,
                capability="EVAL",
                arguments={"expr": "1 + 1"},
            )

    def test_bounded_steps_budget_enforced(self):
        orchestrator = BoundedInstrumentOrchestratorV1()
        # Max steps budget is 64
        with pytest.raises(ValueError, match="Plan exceeds max steps"):
            steps = tuple(
                ToolExecutionStepV1(i, "INSPECT_PIXELS") for i in range(65)
            )
            OrchestrationPlanV1(plan_id="OVERFLOW", steps=steps)

    def test_successful_multi_tool_execution(self):
        orchestrator = BoundedInstrumentOrchestratorV1()
        plan = OrchestrationPlanV1(
            plan_id="PLAN-DRAW-PEN",
            steps=(
                ToolExecutionStepV1(0, "INSPECT_PIXELS"),
                ToolExecutionStepV1(1, "SELECT_TOOL", {"tool": "PEN"}),
                ToolExecutionStepV1(2, "DRAW_STROKE", {
                    "points": [(16, 16), (48, 48)],
                    "kind": "LINE",
                    "width": 3,
                }),
                ToolExecutionStepV1(3, "APPLY_INSTRUMENT"),
                ToolExecutionStepV1(4, "INSPECT_PIXELS"),
            ),
        )

        receipt = orchestrator.execute_plan(plan)
        assert receipt.total_steps_executed == 5
        assert receipt.successful_steps == 5
        assert receipt.failed_steps == 0
        assert receipt.reverted_steps == 0
        assert receipt.decision_authority == "KX108_ONLY"
        assert receipt.native_memory_write_allowed is False

    def test_rollback_on_lock_violation(self):
        orchestrator = BoundedInstrumentOrchestratorV1()

        # Define an intent that strictly LOCKS the top half [0, 0, 64, 32]
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-LOCK-TOP",
            goal_description="Only edit bottom half",
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=(
                RegionConstraintV1("TOP_HALF", (0, 0, 64, 32), ConstraintKindV1.LOCK),
            ),
        )

        # Plan attempts to draw a stroke in the locked region
        plan = OrchestrationPlanV1(
            plan_id="PLAN-TRESPASS-LOCK",
            steps=(
                ToolExecutionStepV1(0, "DRAW_STROKE", {
                    "points": [(10, 10), (20, 20)],
                    "kind": "LINE",
                    "width": 3,
                }),
            ),
        )

        initial_sha = orchestrator.canvas_sha256
        receipt = orchestrator.execute_plan(plan, intent=intent)

        # The step must be rolled back
        assert receipt.reverted_steps == 1
        assert receipt.step_receipts[0].status == "REJECTED_LOCK_VIOLATION"
        assert receipt.step_receipts[0].reverted is True
        # Canvas must be restored to untouched state
        assert orchestrator.canvas_sha256 == initial_sha


class TestG02DiffusionAdapterHardwareBarrier:
    """Validation of G02 Diffusion Adapter and Hardware Safety Barrier."""

    def test_hardware_probe_current_machine(self):
        profile = probe_hardware_profile()
        assert profile.os_name == "Windows"
        assert profile.is_heavy_diffusion_capable is False
        assert "NO_CUDA_GPU_DETECTED" in profile.reason or "INSUFFICIENT_VRAM" in profile.reason

    def test_heavy_diffusion_download_strictly_blocked(self):
        adapter = DiffusionGeneratorAdapterV1()
        with pytest.raises(HeavyDiffusionDownloadBlockedError, match="Blocked download of heavy diffusion model"):
            adapter.request_heavy_model_download("flux-1-dev-12B")

    def test_bounded_safe_generation_emits_valid_artifact(self):
        adapter = DiffusionGeneratorAdapterV1()
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-SAFE-GEN",
            goal_description="Draw a circle while locking the corners",
            rigor_profile=RigorProfileV1.SEMANTIC_SKETCH,
            region_constraints=(
                RegionConstraintV1("CORNER_TL", (0, 0, 10, 10), ConstraintKindV1.LOCK),
            ),
        )

        artifact = adapter.generate(intent)

        assert isinstance(artifact, GeneratedArtifactV0)
        assert artifact.is_generated is True
        assert artifact.native_memory_write_allowed is False
        assert artifact.auto_promotion_allowed is False
        assert artifact.decision_authority == "KX108_ONLY"
        assert artifact.generation_mode == "BOUNDED_PROCEDURAL_SAFE_FALLBACK"

        # Check compliance
        assert artifact.compliance_report is not None
        assert artifact.compliance_report.compliant is True
        assert len(artifact.compliance_report.lock_violations) == 0

        # Verify image output
        pil_img = artifact.as_pil_image()
        assert pil_img.size == (64, 64)
