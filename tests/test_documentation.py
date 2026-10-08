"""Documentation checks for the Brody Image F0 integration PR.

Structural checks only: they do not prove image inference or generation.
"""
from pathlib import Path
import re
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class BrodyImageDocumentationTests(TestCase):
    def test_image_master_plan_and_branch_map_exist(self):
        for name in ("21_BRODY_IMAGE_MASTER_PLAN.md", "22_IMAGE_BRANCH_AND_DONOR_MAP.md"):
            with self.subTest(name=name):
                self.assertTrue((DOCS / name).is_file(), f"Missing {name}")

    def test_readme_prioritizes_image_and_links_both_documents(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("BRODY IMAGE", readme)
        self.assertIn("21_BRODY_IMAGE_MASTER_PLAN.md", readme)
        self.assertIn("22_IMAGE_BRANCH_AND_DONOR_MAP.md", readme)

    def test_atlas_keeps_numbered_concepts(self):
        atlas = (DOCS / "15_CONCEPT_ATLAS.md").read_text(encoding="utf-8")
        numbers = [int(x) for x in re.findall(r"^# (\d+)\. ", atlas, re.MULTILINE) if int(x) > 0]
        self.assertEqual(numbers, list(range(1, 109)))

    def test_source_matrix_tracks_all_concepts(self):
        matrix = (DOCS / "18_CONCEPT_SOURCE_MATRIX.md").read_text(encoding="utf-8")
        numbers = [int(x) for x in re.findall(r"^\| (\d+) \| ", matrix, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 109)))

    def test_image_documents_local_links_resolve(self):
        for name in ("21_BRODY_IMAGE_MASTER_PLAN.md", "22_IMAGE_BRANCH_AND_DONOR_MAP.md"):
            file = DOCS / name
            content = file.read_text(encoding="utf-8")
            links = re.findall(r"\]\(([^)]+)\)", content)
            for link in links:
                if link.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                path = (file.parent / link.split("#", 1)[0]).resolve()
                with self.subTest(file=name, link=link):
                    self.assertTrue(path.is_file(), f"Broken local documentation link: {link}")
