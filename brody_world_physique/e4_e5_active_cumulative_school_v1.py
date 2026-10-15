"""E4+E5: P159 active probe, P158 unidentifiability, P156 cumulative replay.

One experimental campaign, two independently measured curricula, sealed
pre-probe choice and independent exam. No action or canonical promotion.
"""
from __future__ import annotations
import argparse,json,random
from pathlib import Path
from . import image_probe_selection_p159 as p159
from . import image_active_context_probe_p158 as p158
from . import image_cumulative_education_p156 as p156
from .experiential_skill_learning_v1 import save,seal

def probe_course(root):
    bank=p159.learn(random.Random(419),12)
    save(root/"FROZEN_PIXEL_PROBE_BANK.json",seal({"bank":bank,
        "source":"P159_RENDERED_PIXEL_TRAINING","native_memory_write":False,
        "canonical_promotion":False,"decision_authority":"KX108_ONLY"}))
    rows=[]
    for case,available,regime in (
        ("regular_flat",["observe","tap","tilt"],"flat"),
        ("regular_slope",["observe","tap","tilt"],"slope"),
        ("regular_spring",["observe","tap","tilt"],"spring"),
        ("hidden_novel",["observe","tap","tilt"],"novel"),
        ("no_discriminator",["observe"],"flat")):
        prior=p158.decide([],{"flat":0.,"slope":-1.},"single",probe_available=len(available)>1)
        choice=p159.choose_probe(bank,available)
        pre=seal({"case":case,"prior":prior,"choice":choice,
            "bank_source":"FROZEN_PIXEL_PROBE_BANK",
            "native_memory_write":False,"canonical_promotion":False,
            "decision_authority":"KX108_ONLY"})
        save(root/(case+"_PRE_PROBE.json"),pre)
        if choice["decision"]=="PROBE":
            rng=random.Random(200+len(rows))
            imgs=[p159.image_at(x) for x in p159.trajectory(rng,regime,choice["action"])]
            try:
                measured=p159.response(p159.measure(imgs))
                outcome=p159.classify(bank,choice["action"],measured)
            finally:
                for im in imgs:im.close()
        else:measured=None;outcome={"decision":"HOLD","reason":"NO_INFORMATIVE_PROBE"}
        rows.append({"case":case,"chosen":choice["decision"],
            "action":choice.get("action"),"outcome":outcome,
            "observed_response":measured,"regime_for_exam_grading_only":regime})
    return {"exams":rows,"pixel_induced_training_bank":True,
        "choice_committed_before_probe_result":True,
        "actual_external_world_intervention":False}

def retention_course(root):
    # P156 performs a sequential syllabus using independent feedback,
    # validation/replay and untouched final exam streams.
    out=root/"P156_FULL_CURRICULUM"
    result=p156.run(out,minutes=5,seed=1565,lessons_each=8,
                    feedback_each=8,validation_each=8,exam_each=20)
    return {"cycles_completed":result["cycles_completed"],
        "cycles_expected":result["cycles_expected"],
        "accepted":result["decisions_accepted"],"held":result["decisions_held"],
        "exam_cases":result["exam_cases"],"mean_mae":result["final_mean_error"],
        "full_curriculum_completed":result["full_curriculum_completed"],
        "real_image_skill_memory_shared_with_E1":False,
        "read_only_native_memory":True}

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    root.mkdir(parents=True)
    e4=probe_course(root)
    e5=retention_course(root)
    report={"schema":"BRODY_E4_E5_ACTIVE_CUMULATIVE_EDUCATION_V1",
        "E4":e4,"E5":e5,
        "P158_P159_P156_REUSED":True,
        "E2E3_FUTURE_GENERATOR_POLICY_CONNECTED":False,
        "actual_multiview_reverse360_proven":False,
        "external_video_transfer_proven":False,
        "native_memory_write":False,"canonical_promotion":False,
        "decision_authority":"KX108_ONLY",
        "verdict":"E4_E5_HISTORICAL_EDUCATION_REUSE_BOUNDED"}
    save(root/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({"verdict":r["verdict"],
        "E4_actions":[(q["case"],q["chosen"],q["outcome"]["decision"]) for q in r["E4"]["exams"]],
        "E5":r["E5"]},indent=2))
if __name__=="__main__":main()
