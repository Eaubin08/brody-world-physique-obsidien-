"""P2.9e: reciprocal multi-representation preflight, without a TEST oracle.

Consumes already measured visual displacements, tests inverse relation and
independent-looking fiducial agreement. An inverse consistency check is
algebraic, not independent physical proof. No automatic frame calibration.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from statistics import median
from .p29d_reconnect_organs_v0 import reconnect

@dataclass(frozen=True)
class MotionView:
    frame_ref: str
    object_apparent_dx: float | None
    candidate_camera_dx: float | None
    object_relative_dx: float | None
    reverse_relative_dx: float | None
    reciprocal_residual: float | None
    candidate_group_count: int
    status: str

def analyze(measurement: dict | None, *, frame_ref: str, min_consensus: int=3,
            max_spread: float=2.0):
    if not frame_ref:
        raise ValueError("frame required")
    if measurement is None:
        return MotionView(frame_ref,None,None,None,None,None,0,"HOLD_PERCEPTION")
    shifts=tuple(measurement["shifts"])
    if len(shifts)!=5 or not 2<=min_consensus<=5 or max_spread<0:
        raise ValueError("measurement/limits")
    apparent=float(measurement["apparent"])
    groups=[]
    for shift in sorted(set(shifts)):
        members=[v for v in shifts if abs(v-shift)<=max_spread]
        if len(members)>=min_consensus:
            groups.append((len(members),median(members)))
    # The largest agreeing cluster can be *correlated and wrong*.
    # It is never silently promoted to a reliable camera measurement.
    if not groups:
        return MotionView(frame_ref,apparent,None,None,None,None,0,
                          "HOLD_NO_CONSENSUS")
    groups.sort(reverse=True)
    estimate=groups[0][1]
    relative=apparent-estimate
    reverse=estimate-apparent
    return MotionView(frame_ref,apparent,estimate,relative,reverse,
                      abs(relative+reverse),len(groups),
                      "CANDIDATE_CORRELATED_CONSENSUS_ONLY")

def reconnect_multiview(*, pair_id: str, source_ref: str,
                        measurement: dict | None, observation_status: str,
                        frame_ref: str, goal: str, anchor_id: int | None,
                        prior_prediction: float | None = None):
    view=analyze(measurement if observation_status=="MEASURED_PIXELS" else None,
                 frame_ref=frame_ref)
    linked=reconnect(pair_id=pair_id,source_ref=source_ref,measurement=measurement,
                     observation_status=observation_status,frame_ref=frame_ref,
                     anchor_id=anchor_id,goal=goal,
                     prior_prediction=prior_prediction)
    prediction=linked["belief"]["inferred_world_dx"]
    disagreements=list(linked["delta"]["contradictions"])
    if prediction is not None and view.object_relative_dx is not None:
        if abs(prediction-view.object_relative_dx)>2:
            disagreements.append("ANCHOR_VS_CORRELATED_CONSENSUS")
    # Without an independently checked camera transform, different hypotheses
    # imply HOLD, not choosing whichever cluster makes TEST labels look good.
    if disagreements or view.status.startswith("HOLD"):
        status="HOLD_CONFLICT_OR_MISSING_OBSERVATION"
        proposed=None
    elif prediction is not None:
        status="WORKING_CANDIDATE_UNVERIFIED"
        proposed=prediction
    else:
        status="HOLD_NO_HISTORICAL_ANCHOR"
        proposed=None
    return {"schema":"BRODY_P29E_RECIPROCAL_MULTIVIEW_V0",
            "view":asdict(view),"source_ref":source_ref,
            "historical_prediction":prediction,
            "proposed_prediction":proposed,"status":status,
            "contradictions":disagreements,
            "inverse_is_independent_proof":False,
            "majority_is_physical_truth":False,
            "experience":linked["experience"],
            "learning_triage":linked["learning_triage"],
            "goal":linked["goal"],"native_memory_write":False,
            "b8_promotion":False,"decision_authority":"KX108_ONLY"}
