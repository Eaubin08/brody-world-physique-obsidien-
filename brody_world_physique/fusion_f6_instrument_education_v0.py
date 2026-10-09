"""F6: reuse V2 learned instrument choice with F5 candidate skills and F4 receipts.

The two historical learning tracks remain independently verified; this bridge
does not falsely claim a unified semantic world model. Synthetic 64x64 only.
"""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
from .drawing_school_v0 import SIDE
from .fusion_f5_multiskill_course_v0 import course,route
from .fusion_f3c_cumulative_skill_archive_v0 import load_registry
from .fusion_f4_education_journal_v0 import append_event,readonly_context,verify_journal
from .p211b_frozen_gesture_transfer_v0 import read
from .p210a_visual_loop_contract_v0 import digest
from .instrument_school_v2 import (run_school as train_instruments,verify_school as verify_instruments,
    select_tool,render_instrument,TOOLS,TEACHER_ONLY_STYLE_TARGET,UNFAMILIAR,_gray_pixel_loss)

def run(out):
    root=Path(out)
    if root.exists():raise ValueError("output already exists")
    root.mkdir(parents=True)
    visual=root/"visual";course(visual)
    instruments=root/"instruments"
    report=train_instruments(instruments,training_lessons=9)
    verify_instruments(instruments)
    episodes=json.loads((instruments/"instrument_skill_memory.json").read_text())["episodes"]
    frozen=tuple(episodes)
    snapshot=load_registry(visual,3)
    rows=[]
    requests=(("rectangle","LIGHT"),("triangle","UNIFORM"),
              ("ellipse","EXPRESSIVE"),("triangle",UNFAMILIAR))
    for n,(shape,intent) in enumerate(requests,1):
        shape_route=route(visual,3,shape)
        choice=select_tool(frozen,intent)
        tool=choice["chosen_tool"]
        row={"shape":shape,"intent":intent,"shape_route":shape_route["authority"],
             "instrument_status":choice["status"],"instrument":tool,
             "candidate_only":True,"target_used_for_selection":False}
        if shape_route["selected"] is None or tool is None:
            row["verdict"]="HOLD"
            rows.append(row)
            append_event(visual,"INSTRUMENT_SELECTION_HOLD",
                         {"shape":shape,"intent":intent,"reason":choice["status"]})
            continue
        entry=next(x for x in snapshot["skills"] if x["id"]==shape)
        _,gestures=read(visual/entry["memory_path"])
        folder=root/("exam-%02d-%s"%(n,shape))
        folder.mkdir()
        drawing=render_instrument(gestures,tool)
        candidate=folder/"candidate.png";drawing.save(candidate)
        # Persist decision/skill/tool identity before creating a TEST target.
        commitment={"shape":shape,"intent":intent,"instrument":tool,
          "source_memory_sha256":entry["memory_sha256"],
          "candidate_sha256":digest(candidate),
          "instrument_train_episode_ids":choice["based_on_training_ids"],
          "selection_rule":choice["selection_rule"],
          "target_read_before_seal":False}
        (folder/"sealed_choice.json").write_text(json.dumps(commitment,indent=2)+"\n")
        # Synthetic teacher independently chooses a predeclared style for evaluation,
        # but target shares the learned geometry: tests tool choice, NOT shape accuracy.
        target=render_instrument(gestures,TEACHER_ONLY_STYLE_TARGET[intent])
        target_path=folder/"teacher-after-seal.png";target.save(target_path)
        blank=Image.new("L",(SIDE,SIDE),255)
        loss=_gray_pixel_loss(drawing,target)
        baseline=_gray_pixel_loss(blank,target)
        row.update({"candidate_sha256":digest(candidate),
            "candidate_mean_gray_loss":loss,"blank_mean_gray_loss":baseline,
            "gain":baseline-loss,"verdict":"IMPROVED" if loss<baseline else "WORSENED" if loss>baseline else "TIE",
            "heldout_source_kind":"SYNTHETIC_SHARED_GEOMETRY"})
        sheet=Image.new("RGB",(SIDE*3,SIDE+18),"white");pen=ImageDraw.Draw(sheet)
        for j,(label,img) in enumerate((("TEACHER",target),("BLANK",blank),("BRODY",drawing))):
            pen.text((j*SIDE+1,1),label,fill="black")
            sheet.paste(img.convert("RGB"),(j*SIDE,18))
        sheet.save(folder/"comparison.png")
        append_event(visual,"INSTRUMENT_SELECTION_TEST",{
            "shape":shape,"intent":intent,"instrument":tool,"candidate_sha256":digest(candidate),
            "tool_training_ids":choice["based_on_training_ids"],
            "heldout_score":loss,"baseline_score":baseline,
            "target_used_for_training":False})
        rows.append(row)
    summary={"schema":"BRODY_F6_INTEGRATED_INSTRUMENTS_V0",
             "known_proposals":sum(x["instrument"] is not None for x in rows),
             "holds":sum(x["verdict"]=="HOLD" for x in rows),
             "rows":rows,"visual_education_events":len(verify_journal(visual)),
             "prior_v2_verified":True,"same_skill_history_reused":True,
             "instrument_training_historically_separate":True,
             "semantic_tool_understanding_proven":False,
             "native_memory_write":False,"decision_authority":"KX108_ONLY"}
    (root/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    return summary

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    args=p.parse_args()
    result=run(args.out)
    print(json.dumps({"proposals":result["known_proposals"],"holds":result["holds"],
     "rows":[[x["shape"],x["intent"],x["instrument"],x["verdict"]] for x in result["rows"]]}))
if __name__=="__main__":main()
