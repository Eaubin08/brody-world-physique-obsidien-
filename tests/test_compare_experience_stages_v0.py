"""Evaluate gains on matched test cases, not misleading coverage-shifted means."""
from unittest import TestCase

from examples.compare_experience_stages_v0 import compare


def report(predicted, learned_err=None, *, n_train=0):
    values=[]
    for index in range(4):
        values.append({
            "heldout_ref":f"sha256:test#frame:{index}",
            "learned_error_px":(learned_err[index] if index in predicted else None),
            "static_error_px":10.,
            "linear_error_px":2.,
            "fixed_accel_error_px":1.5,
        })
    return {
        "schema":"BRODY_COLD_START_EXPERIENTIAL_SUITE_V0",
        "source_kind":"SIMULATED",
        "world_knowledge_validated":False,
        "training_candidate_transitions":n_train,
        "test_predictions":len(predicted),
        "test_measures":[{"source_sha256":"b"*64,"errors":values}],
    }


class StageComparisonTests(TestCase):
    def test_coverage_and_paired_errors_are_separate(self):
        cold=report(set(),{},n_train=0)
        one=report({0,1},{0:1.,1:3.},n_train=9)
        many=report({0,1,2,3},{0:2.,1:2.,2:9.,3:12.},n_train=36)
        r=compare(cold,one,many)
        self.assertEqual(r["cold_predictions"],0)
        self.assertEqual(r["one_experience_predictions"],2)
        self.assertEqual(r["many_experience_predictions"],4)
        self.assertEqual(r["shared_predicted_positions"],2)
        self.assertEqual(r["one_error_on_shared_px"],2.)
        self.assertEqual(r["many_error_on_shared_px"],2.)
        self.assertEqual(r["paired_many_wins"],1)
        self.assertEqual(r["paired_one_wins"],1)
        self.assertFalse(r["physical_causality_proven"])

    def test_reject_mismatched_test_sources(self):
        cold=report(set(),{},n_train=0)
        one=report({0},{0:1.},n_train=9)
        many=report({0},{0:1.},n_train=36)
        many["test_measures"][0]["source_sha256"]="c"*64
        with self.assertRaisesRegex(ValueError,"same heldout"):
            compare(cold,one,many)

    def test_reject_prior_predictions_in_cold_start(self):
        cold=report({0},{0:1.},n_train=0)
        one=report({0},{0:1.},n_train=9)
        many=report({0},{0:1.},n_train=36)
        with self.assertRaisesRegex(ValueError,"cold"):
            compare(cold,one,many)
