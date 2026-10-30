import json
import tempfile
import unittest
from pathlib import Path
from scripts.new_project import create_project


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = {"schema_version": 1, "total_duration_seconds": 5,
                        "clips": [{"id": "CLIP01", "duration_seconds": 5}], "references": []}

    def test_rerun_keeps_approved_script_and_snapshot(self):
        result = create_project(self.root, "demo", "EP01", self.profile)
        episode = Path(result["path"])
        script = episode / "script-source.md"
        script.write_text("USER APPROVED SCRIPT", encoding="utf-8")
        changed = {**self.profile, "aspect_ratio": "9:16"}
        again = create_project(self.root, "demo", "EP01", changed)
        self.assertEqual(again["status"], "already_exists")
        self.assertEqual(script.read_text(encoding="utf-8"), "USER APPROVED SCRIPT")
        saved = json.loads((episode / "project.json").read_text(encoding="utf-8"))
        self.assertNotIn("aspect_ratio", saved["profile_snapshot"])
        self.assertTrue((episode / "clips/CLIP01/review-v001.md").is_file())

    def test_invalid_durations_do_not_create_project(self):
        for duration in (0, -1, True, float("nan"), float("inf"), 6):
            with self.subTest(duration=duration):
                bad = {**self.profile, "clips": [{"id": "CLIP01", "duration_seconds": duration}]}
                with self.assertRaises(ValueError):
                    create_project(self.root, "invalid", "EP01", bad)
                self.assertFalse((self.root / "invalid").exists())

    def test_duplicate_ids_and_path_traversal_are_rejected(self):
        bad = {**self.profile, "total_duration_seconds": 10, "clips": self.profile["clips"] * 2}
        with self.assertRaises(ValueError):
            create_project(self.root, "bad", "EP01", bad)
        with self.assertRaises(ValueError):
            create_project(self.root, "../escape", "EP01", self.profile)
        bad_clip = {**self.profile, "clips": [{"id": "../outside", "duration_seconds": 5}]}
        with self.assertRaises(ValueError):
            create_project(self.root, "bad", "EP01", bad_clip)

    def test_symlink_cannot_redirect_writes(self):
        outside = self.root / "outside"
        outside.mkdir()
        output = self.root / "projects"
        output.mkdir()
        (output / "demo").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            create_project(output, "demo", "EP01", self.profile)
        self.assertFalse((outside / "EP01").exists())


if __name__ == "__main__":
    unittest.main()
