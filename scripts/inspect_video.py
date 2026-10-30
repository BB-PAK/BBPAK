#!/usr/bin/env python3
"""Inspect local video metadata and extract frames; no model calls or audio judgment."""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
from pathlib import Path


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError(f"{Path(command[0]).name} failed: {result.stderr[-1000:].strip()}")
    return result


def probe(source):
    data = json.loads(run([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(source)
    ]).stdout)
    video = next((s for s in data.get("streams", [])
                  if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic")), None)
    if video is None:
        raise ValueError("No video stream found")
    duration = None
    duration_source = None
    for label, candidate in (("video_stream", video.get("duration")), ("container", data.get("format", {}).get("duration"))):
        try:
            number = float(candidate)
        except (ValueError, TypeError):
            continue
        if math.isfinite(number) and number > 0:
            duration, duration_source = number, label
            break
    if duration is None:
        raise ValueError("No finite positive duration available")
    return {
        "duration_seconds": duration, "duration_source": duration_source,
        "video_stream_index": video["index"], "width": video["width"], "height": video["height"],
        "average_frame_rate": video.get("avg_frame_rate"), "sample_aspect_ratio": video.get("sample_aspect_ratio"),
        "display_aspect_ratio": video.get("display_aspect_ratio"),
        "has_audio_stream": any(s.get("codec_type") == "audio" for s in data.get("streams", [])),
        "audio_listened": False, "full_video_reviewed": False,
    }


def sample_times(duration, explicit, interval, max_frames):
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("duration must be finite and positive")
    if isinstance(max_frames, bool) or not isinstance(max_frames, int) or not 1 <= max_frames <= 240:
        raise ValueError("max_frames must be between 1 and 240")
    if explicit is not None:
        try:
            values = [float(value.strip()) for value in explicit.split(",")]
        except ValueError as exc:
            raise ValueError("times must be comma-separated numbers") from exc
        if any(not math.isfinite(t) or t < 0 or t >= duration for t in values):
            raise ValueError("times must be finite and in the range 0 <= time < duration")
        values = sorted(set(values))
        if len(values) > max_frames:
            raise ValueError("explicit times exceed max_frames")
        return values, False
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("interval must be finite and positive")
    # Cap before constructing the list, including for extremely small intervals.
    truncated = (duration / interval) > max_frames
    values = [index * interval for index in range(max_frames) if index * interval < duration]
    return values, truncated


def sha256(source):
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_video(video, output, times=None, interval=1.0, max_frames=30):
    for executable in ("ffmpeg", "ffprobe"):
        if not shutil.which(executable):
            raise ValueError(f"{executable} is required")
    source = Path(video).resolve(strict=True)
    if not source.is_file():
        raise ValueError("video must be a local file")
    destination = Path(output).absolute()
    # Never replace a previous review or write through its symlink.
    if destination.exists() or destination.is_symlink():
        raise ValueError("output already exists; choose a new review directory")
    metadata = probe(source)
    requested, truncated = sample_times(metadata["duration_seconds"], times, interval, max_frames)
    destination.mkdir(parents=True)
    records = []
    for index, requested_time in enumerate(requested):
        filename = f"frame-{index:04d}.png"
        # Decode from the start, normalize to the first decoded video frame, then
        # select the first real frame at/after the request. Do not relabel it as
        # the requested timestamp. This also handles variable frame rate video.
        result = run([
            "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "info", "-n", "-i", str(source),
            "-map", f"0:{metadata['video_stream_index']}", "-an", "-sn", "-dn",
            "-vf", f"setpts=PTS-STARTPTS,select=gte(t\\,{requested_time:.9f}),showinfo",
            "-frames:v", "1", "-vsync", "0", "-threads", "1", str(destination / filename),
        ])
        timestamps = re.findall(r"\bpts_time:([0-9.eE+\-]+)", result.stderr)
        if not timestamps or not (destination / filename).is_file():
            raise ValueError(f"No frame at or after {requested_time}; partial output retained at {destination}")
        records.append({"file": filename, "requested_seconds": requested_time,
                        "selected_frame_seconds": float(timestamps[0])})
    report = {
        "schema_version": 1, "source_file": str(source), "source_sha256": sha256(source),
        **metadata, "timestamp_origin": "first decoded video frame = 0 seconds",
        "selection": "first decoded frame at or after each requested time",
        "sampling_truncated": truncated, "frames": records,
        "limitations": ["Sampled frames do not reveal all intervening motion.",
                        "No audio was listened to or evaluated.",
                        "Rotation metadata may be applied by FFmpeg; reported dimensions are coded stream dimensions."]
    }
    with (destination / "inspection.json").open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    sampling = parser.add_mutually_exclusive_group()
    sampling.add_argument("--times", help="Comma-separated seconds, relative to first video frame")
    sampling.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--max-frames", type=int, default=30)
    args = parser.parse_args()
    try:
        report = inspect_video(args.video, args.output, args.times, args.interval, args.max_frames)
        print(json.dumps({"report": str(args.output / "inspection.json"),
                          "duration_seconds": report["duration_seconds"], "frames": len(report["frames"]),
                          "sampling_truncated": report["sampling_truncated"]}, ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
