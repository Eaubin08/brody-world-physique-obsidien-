"""F7: TRAIN-only tool-policy correction, versioned immutable evidence and blind transfer.

Uses V2 empirical select_tool and F4 journal. Does not modify learner weights,
Native Memory or a gesture model. This is policy correction, not art understanding.
"""
import argparse,json
from pathlib import Path
from PIL import Image
from .instrument_school_v2 import TOOLS,select_tool,render_instrument,_gray_pixel_loss
from .drawing_school_v1 import GestureV1
from .fusion_f4_education_journal_v0 import append_event,verify_journal
from .p210a_visual_loop_contract_v0 import digest

GOAL="LIGHT"
def trial(identifier,tool_losses):
    return {"id":identifier,"goal":GOAL,"trial_losses":tool_losses}

def choose(history):
    return select_tool(tuple(history),GOAL)

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("output exists")
    root.mkdir(parents=True)
    # Original empirical memory: PENCIL wins the initial training environment.
    old=[trial("train-old",{"PENCIL":1.0,"PEN":8.0,"NIB":9.0})]
    before=choose(old)
    if before["chosen_tool"]!="PENCIL":raise ValueError("initial policy changed")
    # New TRAIN observation demonstrates a contrary style outcome.
    # A full tool comparison comes from render_instrument vs a PEN target,
    # with gestures acquired from a TRAIN-only procedural drawing exercise.
    train_g=(GestureV1(((8,10),(52,42)),"STRAIGHT_STROKE"),)
    reference=render_instrument(train_g,"PEN")
    teacher=root/"training-feedback.png";reference.save(teacher)
    losses={name:_gray_pixel_loss(render_instrument(train_g,name),reference) for name in TOOLS}
    # Distinct training experiences: sufficient counterexamples to change empirical mean.
    newer=[trial("train-correction-%d"%i,losses) for i in range(1,4)]
    after=choose(old+newer)
    if after["chosen_tool"]!="PEN":raise ValueError("correction not learned")
    for version,records in (("v001",old),("v002",old+newer)):
        loc=root/(version+".json")
        loc.write_text(json.dumps({"schema":"BRODY_F7_TOOL_CANDIDATE_SNAPSHOT_V0",
          "records":records,"native_memory_write":False,"canonical_promotion":False,
          "decision_authority":"KX108_ONLY"},indent=2)+"\n")
    append_event(root,"TRAIN_OLD",{"memory_version":"v001","winner":before["chosen_tool"],
      "source":"EXPLICIT_SYNTHETIC_TRAIN"})
    append_event(root,"TRAIN_CORRECTION",{"memory_version":"v002",
      "previous_version":"v001","new_train_losses":losses,
      "old_tool":before["chosen_tool"],"new_tool":after["chosen_tool"],
      "no_test_feedback_used":True})
    # Heldout geometry DIFFERENT from the correction geometry, and target
    # is rendered only after BOTH proposed candidates are sealed on disk.
    unseen=(GestureV1(((6,52),(28,7)),"STRAIGHT_STROKE"),
            GestureV1(((28,7),(57,43)),"STRAIGHT_STROKE"))
    old_candidate=root/"old-candidate.png"
    new_candidate=root/"new-candidate.png"
    render_instrument(unseen,before["chosen_tool"]).save(old_candidate)
    render_instrument(unseen,after["chosen_tool"]).save(new_candidate)
    sealed={"old_tool":before["chosen_tool"],"new_tool":after["chosen_tool"],
            "old_sha256":digest(old_candidate),"new_sha256":digest(new_candidate),
            "teacher_not_opened_before_sealing":True,
            "selection_based_on_train_only":True}
    (root/"sealed-before-test.json").write_text(json.dumps(sealed,indent=2)+"\n")
    target=render_instrument(unseen,"PEN")
    target_path=root/"heldout-teacher.png";target.save(target_path)
    err_old=_gray_pixel_loss(Image.open(old_candidate),target)
    err_new=_gray_pixel_loss(Image.open(new_candidate),target)
    append_event(root,"HELD_OUT_COMPARE",{"old_error":err_old,"new_error":err_new,
     "old_candidate_sha256":sealed["old_sha256"],"new_candidate_sha256":sealed["new_sha256"],
     "feedback_promoted_to_training":False})
    result={"schema":"BRODY_F7_TRAIN_CORRECTION_V0",
      "old_tool":before["chosen_tool"],"new_tool":after["chosen_tool"],
      "old_test_loss":err_old,"new_test_loss":err_new,
      "improvement":err_old-err_new,"better_on_this_test":err_new<err_old,
      "old_memory_preserved":True,"test_hidden_until_both_candidates_sealed":True,
      "teacher_synthetic_shared_renderer":True,
      "correction_type":"INSTRUMENT_ROUTING_NOT_GESTURE_REFINEMENT",
      "not_generalization_proof":True,
      "journal_events":len(verify_journal(root)),
      "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (root/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    a=p.parse_args();r=run(a.out)
    print(json.dumps({k:r[k] for k in ("old_tool","new_tool","old_test_loss","new_test_loss","better_on_this_test")}))
if __name__=="__main__":main()
