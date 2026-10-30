#!/usr/bin/env python3
"""Create a local video project without overwriting an existing episode."""
import argparse
import json
import math
import re
from pathlib import Path

IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}\Z")


def identifier(value, label):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f"{label}: use 1–80 ASCII letters, digits, - or _, starting with a letter/digit")
    return value


def positive_number(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{label}: must be a finite positive number")
    return value


def validate_profile(profile):
    if not isinstance(profile, dict):
        raise ValueError("profile must be a JSON object")
    if profile.get("schema_version", 1) != 1:
        raise ValueError("unsupported profile schema_version")
    clips = profile.get("clips", [])
    if not isinstance(clips, list):
        raise ValueError("clips must be a list")
    seen = set()
    for clip in clips:
        if not isinstance(clip, dict):
            raise ValueError("each clip must be an object")
        clip_id = identifier(clip.get("id"), "clip id")
        if clip_id in seen:
            raise ValueError(f"duplicate clip id: {clip_id}")
        seen.add(clip_id)
        positive_number(clip.get("duration_seconds"), f"{clip_id} duration")
    total = profile.get("total_duration_seconds")
    if total is not None:
        positive_number(total, "total duration")
        if clips and not math.isclose(sum(c["duration_seconds"] for c in clips), total, abs_tol=0.001, rel_tol=0):
            raise ValueError("sum of clip durations does not match total_duration_seconds")
    refs = profile.get("references", [])
    if not isinstance(refs, list) or any(not isinstance(ref, dict) for ref in refs):
        raise ValueError("references must be a list of objects")
    return profile


def write_json(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def write_text(path, value):
    with path.open("x", encoding="utf-8") as handle:
        handle.write(value)


def create_project(output_root, project, episode, profile):
    identifier(project, "project")
    identifier(episode, "episode")
    validate_profile(profile)
    # Reject NaN/Infinity even in optional fields before making any directory.
    json.dumps(profile, allow_nan=False)
    root = Path(output_root).resolve()
    destination = root / project / episode
    # Prevent an existing symlink from redirecting project writes outside output_root.
    if not destination.resolve().is_relative_to(root):
        raise ValueError("project path escapes output_root")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination.mkdir()
    except FileExistsError:
        if not destination.is_dir():
            raise ValueError("episode path exists and is not a directory")
        return {"status": "already_exists", "path": str(destination), "message": "No existing files changed."}

    write_json(destination / "project.json", {
        "schema_version": 1, "project": project, "episode": episode,
        "status": "draft", "profile_snapshot": profile,
    })
    write_json(destination / "references.json", profile.get("references", []))
    write_text(destination / "brief.md", f"# {project} / {episode}\n\n"
               "- 목표: 확인 필요\n- 플랫폼: 확인 필요\n- 상태: 초안\n"
               "- 실제 확정 원문: script-source.md에 연결\n"
               "- 참조 파일: references.json에 연결하고 실제 접근 여부 확인\n\n"
               "project.json의 프로필은 초기 기록이며 최신 사용자 지시와 확정 원문이 우선합니다.\n")
    write_text(destination / "script-source.md", "# 확정 시나리오 원문\n\n"
               "상태: missing_source\n\n출처 / 버전 / 승인 일자: 확인 필요\n\n"
               "실제 승인된 원문을 입력하세요. 프로필의 짧은 메모로 전체 대사를 복원하지 않습니다.\n")
    write_text(destination / "changes.md", "# 변경 이력\n\n| 버전 | 대상 | 변경 | 이유 | 승인 상태 |\n|---|---|---|---|---|\n")
    for clip in profile.get("clips", []):
        clip_dir = destination / "clips" / clip["id"]
        clip_dir.mkdir(parents=True)
        write_json(clip_dir / "clip.json", {**clip, "status": "draft"})
        write_text(clip_dir / "prompt-image-v001.md", "# 이미지 프롬프트 v001\n\n상태: 초안\n\n"
                   "## 참조 파일과 역할\n확인 필요\n\n## 복사용 프롬프트\n확정 원문과 실제 참조 확인 후 작성\n")
        write_text(clip_dir / "prompt-video-v001.md", "# 영상 프롬프트 v001\n\n상태: 초안\n\n"
                   "## 실행 설정\n확인 필요\n\n## 참조 역할\n\n## 전체 장면\n\n## 시간별 동작\n\n## 유지 조건\n")
        write_text(clip_dir / "review-v001.md", "# 검수 v001\n\n상태: 미검수\n\n"
                   "## 실제 확인 범위\n영상 재생: 미확인\n프레임 확인: 미확인\n음향 청취: 미확인\n\n"
                   "## 관찰과 최소 수정\n| 실제 시각 | 관찰 | 영향 | 수정 | 근거 |\n|---|---|---|---|---|\n")
    return {"status": "created", "path": str(destination), "clips": len(profile.get("clips", []))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--episode", required=True)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parents[1] / "projects")
    args = parser.parse_args()
    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8")) if args.profile else {
            "schema_version": 1, "script_status": "missing_source", "clips": [], "references": []}
        print(json.dumps(create_project(args.output_root, args.project, args.episode, profile), ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
