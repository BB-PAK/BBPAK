import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.inspect_video import inspect_video, sample_times


class SamplingTests(unittest.TestCase):
    def test_invalid_times_and_oversized_requests_rejected(self):
        for value in ("-1", "5", "nan", "inf", "", "0,1,2,3"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sample_times(5, value, 1, 3)
        self.assertEqual(sample_times(5, "1,0,1", 1, 3), ([0, 1], False))

    def test_default_sampling_includes_zero_and_marks_truncation(self):
        self.assertEqual(sample_times(5, None, 1, 3), ([0, 1, 2], True))
        self.assertEqual(sample_times(0.3, None, 1, 3), ([0], False))
        for interval in (0, -1, float("inf"), float("nan")):
            with self.assertRaises(ValueError):
                sample_times(5, None, interval, 3)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg and FFprobe required")
class VideoIntegrationTests(unittest.TestCase):
    def test_actual_duration_and_selected_frame_time(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            video = root / "input.mkv"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                            "testsrc2=size=160x90:rate=10:duration=2", "-c:v", "ffv1", str(video)], check=True)
            output = root / "review"
            report = inspect_video(video, output, "0,0.55,1.9")
            self.assertAlmostEqual(report["duration_seconds"], 2, places=2)
            self.assertEqual((report["width"], report["height"]), (160, 90))
            self.assertEqual(len(report["source_sha256"]), 64)
            self.assertFalse(report["audio_listened"])
            self.assertFalse(report["has_audio_stream"])
            expected_times = [0, 0.6, 1.9]
            for frame, expected in zip(report["frames"], expected_times):
                self.assertAlmostEqual(frame["selected_frame_seconds"], expected, places=4)
                self.assertTrue((output / frame["file"]).read_bytes().startswith(b"\x89PNG"))
            self.assertEqual(report["frames"][1]["requested_seconds"], 0.55)
            self.assertEqual(json.loads((output / "inspection.json").read_text()), report)
            before = (output / "inspection.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "already exists"):
                inspect_video(video, output, "0")
            self.assertEqual((output / "inspection.json").read_bytes(), before)

    def test_variable_frame_rate_records_real_time(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            video = root / "vfr.mkv"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                            "testsrc2=size=160x90:rate=10:duration=2", "-vf",
                            "select='eq(n,0)+eq(n,3)+eq(n,9)+eq(n,18)'",
                            "-vsync", "vfr", "-c:v", "ffv1", str(video)], check=True)
            report = inspect_video(video, root / "review", "0.35")
            self.assertAlmostEqual(report["frames"][0]["selected_frame_seconds"], 0.9, places=4)


if __name__ == "__main__":
    unittest.main()
