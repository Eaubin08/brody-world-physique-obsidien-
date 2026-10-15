"""P165-D10: focused regression tests. These test invariants, not broad episode counts.

Known limitations (true 3D, actual identity, sensor fusion) remain unproven.
"""
import copy
import hashlib
import json
import unittest
from PIL import Image,ImageDraw
from brody_world_physique.hard_scene_angles_p165d2 import (draw,spec_from_index,ANGLES,MOTIONS,OCCLUSIONS,
 APPEARANCES,BACKGROUNDS,image_only_evaluate)
from brody_world_physique.color_agnostic_perception_p165d3 import components,detect_sequence
from brody_world_physique.persistent_world_state_p165d4 import initial,update,propagate,view,GOALS
from brody_world_physique.image_persistent_tracks_p165d5 import associate,state_from_path
from brody_world_physique.reappearance_gate_p165d6 import infer,evaluate_tracks
from brody_world_physique.goal_multi_continuity_p165d7 import arbitrate,claim,fixtures
from brody_world_physique.goal_track_bridge_p165d8 import views_from_frames,evidence_from_inference
from brody_world_physique.local_epistemic_diagnostic_p165d9 import local_view

def obs(t,x,source="SIMULATED_SENSOR",frame="world_1d",quality=1):
 return {"time":t,"position":x,"source":source,"frame":frame,"quality":quality}

class MatrixProperties(unittest.TestCase):
 def test_01_all_675_unique(self):
  s=[tuple(spec_from_index(i).items()) for i in range(675)]
  self.assertEqual(len(set(s)),675)
 def test_02_factor_dimensions(self):
  self.assertEqual([len(x) for x in (ANGLES,MOTIONS,OCCLUSIONS,APPEARANCES,BACKGROUNDS)],[5,5,3,3,3])
 def test_03_seven_raster_frames(self):
  frames,_=draw(spec_from_index(1),31)
  try:self.assertEqual(len(frames),7)
  finally:
   for f in frames:f.close()
 def test_04_truth_is_separate_from_images(self):
  frames,truth=draw(spec_from_index(2),31)
  try:
   self.assertEqual(len(truth),7)
   self.assertEqual(len(detect_sequence(frames)),7)
  finally:
   for f in frames:f.close()
 def test_05_repeatable_generator_pixels(self):
  a,_=draw(spec_from_index(300),23);b,_=draw(spec_from_index(300),23)
  try:self.assertEqual([i.tobytes() for i in a],[i.tobytes() for i in b])
  finally:
   for i in a+b:i.close()
 def test_06_d2_no_identity_certification(self):
  ims,_=draw(spec_from_index(674),22)
  try:self.assertFalse(image_only_evaluate(ims)["unique_identity_proven"])
  finally:
   for i in ims:i.close()

class DetectionProperties(unittest.TestCase):
 def image(self,color,centers=(50,)):
  im=Image.new("RGB",(168,96),(233,228,216))
  d=ImageDraw.Draw(im)
  for x in centers:d.ellipse((x-5,43,x+5,53),fill=color)
  return im
 def test_07_red_detected(self):
  im=self.image((215,40,50))
  try:self.assertEqual(len(components(im)),1)
  finally:im.close()
 def test_08_blue_detected(self):
  im=self.image((28,120,220))
  try:self.assertEqual(len(components(im)),1)
  finally:im.close()
 def test_09_connected_separate(self):
  im=self.image((215,40,50),(40,100))
  try:self.assertEqual(len(components(im)),2)
  finally:im.close()
 def test_10_blank_returns_no_instances(self):
  im=Image.new("RGB",(168,96),(233,228,216))
  try:self.assertEqual(components(im),[])
  finally:im.close()
 def test_11_no_spatial_identity_proof(self):
  im=self.image((28,120,220),(40,100))
  try:self.assertNotIn("identity_proven",repr(components(im)))
  finally:im.close()
 def test_12_d3_returns_ordered_candidates(self):
  im=self.image((215,40,50),(100,40))
  try:
   detections=components(im)
   self.assertLess(detections[0]["x"],detections[1]["x"])
  finally:im.close()

class PersistentProperties(unittest.TestCase):
 def test_13_initial_empty(self):
  s=initial();self.assertIsNone(s["position"]);self.assertIsNone(s["velocity"])
 def test_14_velocity_from_two_points(self):
  s=update(update(initial(),obs(0,10)),obs(2,18))
  self.assertEqual(s["velocity"],4.)
 def test_15_forward_prediction(self):
  s=update(update(initial(),obs(0,10)),obs(1,14))
  p=propagate(s,3)
  self.assertEqual(p["position"],22.)
 def test_16_uncertainty_monotonic_forward(self):
  s=update(update(initial(),obs(0,10)),obs(1,14))
  self.assertLess(propagate(s,2)["position_uncertainty"],propagate(s,5)["position_uncertainty"])
 def test_17_predict_does_not_mutate_source(self):
  s=update(update(initial(),obs(0,10)),obs(1,14));before=copy.deepcopy(s)
  propagate(s,4);self.assertEqual(s,before)
 def test_18_future_observation_mismatch(self):
  s=update(update(initial(),obs(0,10)),obs(1,14))
  s=propagate(s,3);s=update(s,obs(4,70))
  self.assertIn("POSITION_PREDICTION_MISMATCH",s["contradictions"])
 def test_19_generated_not_observed(self):
  s=update(initial(),obs(0,10,"GENERATED"))
  self.assertEqual(s["mode"],"HOLD_SOURCE")
 def test_20_frame_mismatch_is_not_applied(self):
  s=update(initial(),obs(0,10,frame="camera"))
  self.assertEqual(s["mode"],"HOLD_FRAME")
 def test_21_quality_hold(self):
  s=update(initial(),obs(0,10,quality=.2))
  self.assertEqual(s["mode"],"HOLD_QUALITY")
 def test_22_invalid_nan_rejected(self):
  with self.assertRaises(ValueError):update(initial(),obs(0,float("nan")))
 def test_23_backwards_propagation_rejected(self):
  with self.assertRaises(ValueError):propagate(initial(),-1)
 def test_24_goal_views_do_not_mutate(self):
  s=update(initial(),obs(0,10));original=copy.deepcopy(s)
  for goal in GOALS:view(s,goal)
  self.assertEqual(s,original)

class AssociationAndReappearance(unittest.TestCase):
 def test_25_beam_bounded(self):
  ims,_=draw(spec_from_index(600),12)
  try:self.assertLessEqual(len(associate(ims,4)["tracks"]),4)
  finally:
   for im in ims:im.close()
 def test_26_no_oracle_interface(self):
  ims,_=draw(spec_from_index(600),12)
  try:self.assertFalse(associate(ims)["uses_oracle"])
  finally:
   for im in ims:im.close()
 def test_27_adapter_explicitly_pixel_1d(self):
  v=state_from_path([10,14,None,None,26,30,34])
  self.assertEqual(v["coordinate_system"],"IMAGE_X_AS_SYNTHETIC_1D")
  self.assertFalse(v["camera_compensated"])
 def test_28_all_beam_hypotheses_have_states(self):
  ims,_=draw(spec_from_index(600),12)
  try:
   r=infer(ims,4)
   self.assertEqual(len(r["raw"]["tracks"]),len(r["persistent_hypotheses"]))
  finally:
   for im in ims:im.close()
 def test_29_four_correct_not_same_reappearance(self):
  t=[10,11,12,13,14,15,16]
  v=evaluate_tracks([{"xs":[10,11,12,13,None,100,100]}],t)
  self.assertTrue(v["topk_four_frame_recall"])
  self.assertFalse(v["same_path_pre_post_recall"])
 def test_30_separate_paths_cannot_fake_same(self):
  t=[10,11,12,13,14,15,16]
  v=evaluate_tracks([{"xs":[10,11,12,None,None,None,None]},
                     {"xs":[None,None,None,None,None,15,16]}],t)
  self.assertTrue(v["pre_visible_recall"]);self.assertTrue(v["post_reappearance_recall"])
  self.assertFalse(v["same_path_pre_post_recall"])
 def test_31_true_same_candidate_path(self):
  t=[10,11,12,13,14,15,16]
  v=evaluate_tracks([{"xs":[10,11,None,None,None,15,16]}],t)
  self.assertTrue(v["same_path_pre_post_recall"])
 def test_32_all_missing_is_not_reappearance(self):
  t=[10,11,12,13,14,15,16]
  v=evaluate_tracks([{"xs":[None]*7}],t)
  self.assertFalse(v["post_reappearance_recall"])

class EpistemicProperties(unittest.TestCase):
 def test_33_different_goal_same_claims(self):
  c=fixtures();before=copy.deepcopy(c)
  a=arbitrate("LOCATE",c);b=arbitrate("REIDENTIFY",c)
  self.assertNotEqual(a["focused"],b["focused"]);self.assertEqual(c,before)
 def test_34_global_conflict_preserved(self):
  for g in ("LOCATE","REIDENTIFY","PREDICT"):
   self.assertEqual(arbitrate(g,fixtures())["status"],"MULTI")
 def test_35_local_symbol_without_data_holds(self):
  c=[v for v in fixtures() if v["continuity"]!="symbolic"]
  v=local_view("INTERPRET_SYMBOL",c)
  self.assertEqual(v["local_status"],"HOLD_LOCAL_NO_RELEVANT_EVIDENCE")
 def test_36_global_multi_can_coexist_with_local_hold(self):
  c=[v for v in fixtures() if v["continuity"]!="symbolic"]
  v=local_view("INTERPRET_SYMBOL",c)
  self.assertEqual(v["global_status"],"MULTI")
 def test_37_symbolic_interpretation_not_observation(self):
  c=fixtures()
  symbolic=[x for x in c if x["continuity"]=="symbolic"]
  self.assertEqual(symbolic[0]["status"],"INTERPRETED")
 def test_38_duplicate_claims_rejected(self):
  x=fixtures()[0]
  with self.assertRaises(ValueError):arbitrate("LOCATE",[x,x])
 def test_39_empty_focus_stays_unresolved(self):
  r=arbitrate("INTERPRET_SYMBOL",[fixtures()[0]])
  self.assertEqual(r["focused"],[])
 def test_40_priorities_are_not_evidence(self):
  self.assertFalse(arbitrate("LOCATE",fixtures())["priority_is_evidence"])
 def test_41_invalid_goal_rejected(self):
  with self.assertRaises(ValueError):arbitrate("NON_GOAL",fixtures())
 def test_42_bridge_digest_stable(self):
  ims,_=draw(spec_from_index(120),11)
  try:
   a=views_from_frames(ims);b=views_from_frames(ims)
   self.assertEqual(a["digest"],b["digest"])
  finally:
   for im in ims:im.close()
 def test_43_bridge_goal_does_not_mutate_evidence(self):
  ims,_=draw(spec_from_index(120),11)
  try:self.assertTrue(views_from_frames(ims)["unchanged_under_goals"])
  finally:
   for im in ims:im.close()
 def test_44_bridge_does_not_fabricate_symbolic(self):
  ims,_=draw(spec_from_index(120),11)
  try:self.assertEqual(views_from_frames(ims)["views"]["INTERPRET_SYMBOL"]["focused"],[])
  finally:
   for im in ims:im.close()
 def test_45_d6_claims_have_provenance(self):
  ims,_=draw(spec_from_index(120),11)
  try:
   claims=evidence_from_inference(infer(ims,4))
   self.assertTrue(all(v["source"] for v in claims))
  finally:
   for im in ims:im.close()

if __name__=="__main__":unittest.main()
