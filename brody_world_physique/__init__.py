"""Brody World Physique Obsidia — bounded physical/world learning contracts."""

from .contracts_v0 import (
    ExperienceValidationStatusV0,
    MemoryEligibilityV0,
    ProjectionKindV0,
    TransformationEpistemicClassV0,
    TransitionTransformationBindingV0,
    WorldExperienceCandidateV0,
    WorldStateDeltaV0,
    WorldStateProjectionV0,
    WorldTransformationV0,
)
from .cognitive_memory_timeline_v1 import (
    CANONICAL_34_TREES,
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    HistoricalBeliefRevisionV1,
    MultidimensionalExperienceV1,
    NativeMemoryAdmissibilityReportV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeDefinitionV1,
    TreeFamilyV1,
    TreeProjectionV1,
)
from .multidimensional_retrieval_v2 import (
    ExperienceRelationLinkV1,
    MeaningQueryIntentV1,
    MeaningQueryResultItemV1,
    MeaningQueryResponseV1,
    MultidimensionalCognitiveMemoryEngineV1,
    MultidimensionalRelationTypeV1,
    VisualTaskAdmissibilityRequestV1,
    VisualTaskAdmissibilityVerdictV1,
)
from .brody_image_cognitive_loop_v1 import (
    BrodyCognitiveCycleReceiptV1,
    BrodyImageCognitiveLoopV1,
)
from .progressive_visual_curriculum_e05 import (
    SVGVisualPlanV1,
    ShadedVisualObjectV1,
    convert_object_to_svg_plan,
    render_shaded_object,
)
from .programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    ProgrammaticExecutionReceiptO04,
    WorkflowInstructionV1,
    WorkflowPredicateV1,
)
from .negative_transfer_detector_v1 import (
    NegativeTransferDetectorV1,
    NegativeTransferDiagnosticV1,
)
from .real_learning_audit_v1 import (
    AutonomousVisualFeatureExtractorV1,
    LearningAuditResultV1,
    RealLearningAuditorV1,
    TeacherVisualCurriculumV1,
    VisualFeatureComponentV1,
    generate_learning_audit_artifacts,
)

from .temporal_video_learning_v1 import (
    MotionAttributionV1,
    PreverbalForecastV1,
    TemporalConfrontationReceiptV1,
    TemporalFrameObservationV1,
    TemporalVideoCognitiveEngineV1,
)
from .f16_real_image_contracts_v1 import (
    BrodyMeasuredObservationV1,
    RealImageObservationF16V1,
    RealImagePipelineAuditReceiptV1,
    audit_real_image_pipeline,
    ingest_real_image_f16,
)

from .real_stack_connection_audit_v1 import (
    RealStackConnectionAuditorV1,
    StackConnectionAuditReportV1,
    SubsystemConnectionStatusV1,
)
from .temporal_multiclip_evaluation_v1 import (
    ClipEvaluationReportV1,
    MultiClipVideoEvaluatorV1,
)
from .novel_situation_transfer_loop_v1 import (
    EmpiricalTransferProofReportV1,
    ExerciseOutcomeReceiptV1,
    NovelSituationTransferHarnessV1,
)
from .generic_transfer_benchmark_v1 import (
    ConditionAggregateMetricsV1,
    GenericTransferBenchmarkHarnessV1,
    GenericTransferBenchmarkReportV1,
    TaskEvaluationOutcomeV1,
)
from .persistent_process_restart_test_v1 import (
    PersistentProcessRestartHarnessV1,
    ProcessRestartProofReceiptV1,
)
from .obsidia_interstack_connection_tracer_v1 import (
    InterstackTraceAuditReportV1,
    ObsidiaConnectionTierV1,
    ObsidiaInterstackConnectionTracerV1,
    StackCallTraceV1,
)
from .filmed_video_evaluation_v1 import (
    FilmedClipEvaluationV1,
    FilmedVideoEvaluationReportV1,
    FilmedVideoEvaluatorV1,
    FilmedVideoFrameV1,
    VideoProvenanceV1,
)
from .observation_to_creation_loop_v1 import (
    CreativeExecutionReceiptV1,
    ObservationToCreationLoopV1,
    ObservationToCreationReportV1,
)
from .workstation_neural_generation_auditor_v1 import (
    LocalBoundedNeuralGeneratorV1,
    LocalHardwareModelAuditReceiptV1,
    NeuralExecutionReceiptV1,
    NeuralGenerationAuditAndExecutionReportV1,
    WorkstationNeuralGenerationAuditorV1,
)

__all__ = [
    "AutonomousVisualFeatureExtractorV1",
    "BrodyCognitiveCycleReceiptV1",
    "BrodyImageCognitiveLoopV1",
    "BrodyMeasuredObservationV1",
    "CANONICAL_34_TREES",
    "ClipEvaluationReportV1",
    "CognitiveMemoryIndexV1",
    "DomainEngagementV1",
    "EmpiricalTransferProofReportV1",
    "EpistemicCalibrationV1",
    "ExerciseOutcomeReceiptV1",
    "ExperienceRelationLinkV1",
    "ExperienceValidationStatusV0",
    "HistoricalBeliefRevisionV1",
    "LearningAuditResultV1",
    "MeaningQueryIntentV1",
    "MeaningQueryResultItemV1",
    "MeaningQueryResponseV1",
    "MemoryEligibilityV0",
    "MotionAttributionV1",
    "MultiClipVideoEvaluatorV1",
    "MultidimensionalCognitiveMemoryEngineV1",
    "MultidimensionalExperienceV1",
    "MultidimensionalRelationTypeV1",
    "NativeMemoryAdmissibilityReportV1",
    "NegativeTransferDetectorV1",
    "NegativeTransferDiagnosticV1",
    "NovelSituationTransferHarnessV1",
    "PreverbalForecastV1",
    "ProgrammaticBoundedOrchestratorO04",
    "ProgrammaticExecutionReceiptO04",
    "ProjectionKindV0",
    "RealImageObservationF16V1",
    "RealImagePipelineAuditReceiptV1",
    "RealLearningAuditorV1",
    "RealStackConnectionAuditorV1",
    "SVGVisualPlanV1",
    "ShadedVisualObjectV1",
    "SpecializedDomainV1",
    "StackConnectionAuditReportV1",
    "SubsystemConnectionStatusV1",
    "TeacherVisualCurriculumV1",
    "TemporalConfrontationReceiptV1",
    "TemporalFrameObservationV1",
    "TemporalVideoCognitiveEngineV1",
    "TimelineEnvelopeV1",
    "TransformationEpistemicClassV0",
    "TransitionTransformationBindingV0",
    "TreeDefinitionV1",
    "TreeFamilyV1",
    "TreeProjectionV1",
    "VisualFeatureComponentV1",
    "VisualTaskAdmissibilityRequestV1",
    "VisualTaskAdmissibilityVerdictV1",
    "WorkflowInstructionV1",
    "WorkflowPredicateV1",
    "WorldExperienceCandidateV0",
    "WorldStateDeltaV0",
    "WorldStateProjectionV0",
    "WorldTransformationV0",
    "audit_real_image_pipeline",
    "convert_object_to_svg_plan",
    "generate_learning_audit_artifacts",
    "ingest_real_image_f16",
    "render_shaded_object",
]


