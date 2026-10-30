# 프로젝트 프로필 작성

`profiles/bbpak-default.json`을 로컬 `projects/` 아래에 복사해 수정합니다. 해당 폴더는 기본적으로 Git 커밋 대상에서 제외됩니다.

아래는 형식 설명을 위한 가상 예시입니다. 실제 작품의 장면이나 길이가 아닙니다.

```json
{
  "schema_version": 1,
  "project_title": "프로젝트 제목",
  "script_status": "missing_source",
  "total_duration_seconds": 12,
  "aspect_ratio": "16:9",
  "clips": [
    {"id": "CLIP01", "duration_seconds": 5, "script": null},
    {"id": "CLIP02", "duration_seconds": 7, "script": null}
  ],
  "references": [
    {"id": "main-character", "role": "주인공", "uri": null, "status": "unverified"}
  ]
}
```

CLIP 길이는 양수여야 하고, 총길이를 지정했다면 CLIP 합계와 맞아야 합니다. 총길이가 미정이면 `null`, CLIP이 미정이면 빈 목록을 씁니다. 프로젝트·에피소드·CLIP의 식별자는 영문·숫자·하이픈·밑줄을 사용합니다. 첫 글자는 영문 또는 숫자이고 80자를 넘기지 않습니다. 한국어 작품명은 `project_title`에 자유롭게 적습니다.

```bash
python scripts/new_project.py --project my-video --episode EP02 --profile projects/my-profile.json
```

기존 프로젝트는 재실행해도 수정하지 않습니다. 기존 프로젝트를 수정하려면 확정본을 보존하고 `docs/change-policy.md`에 따라 새 버전으로 편집하세요. 새로운 CLIP도 기존 폴더에 자동 추가되지 않습니다.
