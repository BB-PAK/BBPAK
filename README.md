# BBPAK — AI Video Skills

비비팍님의 AI 영상 제작 기준을 반복해서 적용하기 위한 **한국어 작업 지침과 보조 도구**입니다. GitHub에는 제작 기준·프롬프트 형식·검수 이력을 관리하고, 실제 생성은 선택한 이미지·영상 서비스에서 진행합니다.

`moongi-video-skills`의 단계별 제작 방식을 참고해 새로 작성했습니다. 원본 전체를 복사하거나 생성 모델을 재학습한 저장소가 아닙니다. 출처와 제외 범위는 [SOURCES.md](SOURCES.md)에 기록했습니다.

## 무엇이 들어 있나요?

| 구성 | 역할 | 사용 예 |
|---|---|---|
| [영상 제작 진행](skills/bbpak-video-director/SKILL.md) | 확정본 확인, CLIP 작업 순서, 변경 이력 관리 | “EP1에서 다음으로 할 작업을 정리해 주세요.” |
| [이미지 프롬프트](skills/bbpak-image-prompts/SKILL.md) | 캐릭터·화풍·공간 참조를 연결한 단일 장면 프롬프트 | “확정 CLIP1로 이미지 프롬프트를 작성해 주세요.” |
| [Seedance 프롬프트](skills/bbpak-seedance-prompts/SKILL.md) | 참조 역할, 시간별 동작, 대사·음향 구분 | “이 확정 이미지로 5초 영상 프롬프트를 작성해 주세요.” |
| [영상 검수](skills/bbpak-video-review/SKILL.md) | 실제 확인한 결함과 미확인 항목을 나눠 최소 수정 제안 | “이 영상에서 손과 컵의 연속성만 검수해 주세요.” |
| `scripts/new_project.py` | 프로젝트·에피소드·CLIP 폴더와 기록 양식 생성 | 확정본을 덮어쓰지 않고 새 작업 준비 |
| `scripts/inspect_video.py` | 로컬 영상의 길이·해상도 확인과 프레임 추출 | 요청 시각과 실제 추출 프레임 시각을 함께 기록 |

## 처음 사용하는 방법

1. 먼저 [기본 제작 기준](profiles/bbpak-default.json)을 확인합니다. 프로젝트마다 실제 확정 기준을 연결해 사용합니다.
2. 현재 작업에 맞는 `SKILL.md`와 프로젝트 기준을 파일을 읽을 수 있는 AI 작업 환경에 제공합니다. 저장소 링크만 전달했을 때 AI가 비공개 파일까지 읽을 수 있는지는 해당 환경의 권한에 달려 있습니다.
3. 승인된 시나리오 원문과 실제 캐릭터·화풍 참조 이미지를 함께 제공합니다. 파일이 없으면 AI는 누락을 표시하고, 완성 프롬프트로 가장하지 않습니다.
4. 생성 서비스에서 결과를 만든 뒤 영상 검수 스킬로 필요한 부분만 수정합니다.

예시 요청:

> 이 저장소의 AGENTS.md와 skills/bbpak-seedance-prompts/SKILL.md를 읽어 주세요. 첨부한 확정 시나리오와 참조 이미지를 기준으로 EP1 CLIP1의 영상 프롬프트를 작성해 주세요. 시나리오·캐릭터·화풍은 유지하고, 아직 확인되지 않은 정보는 표시해 주세요.

스킬 설치를 지원하는 환경에서는 `skills/` 아래 각 스킬 폴더를 설치할 수 있습니다. **저장소 생성과 AI 환경에 스킬 설치는 별도 작업**입니다. 이 저장소를 만들었다고 ChatGPT나 다른 서비스에 자동 설치되지는 않습니다.

## 프로젝트 폴더 만들기

Python 3.10 이상에서 외부 Python 패키지 없이 실행합니다.

```bash
python scripts/new_project.py --project my-video --episode EP01 --profile profiles/bbpak-default.json
```

`projects/my-video/EP01/`에 브리프, 원문 입력 파일, 참조 목록을 만듭니다. 프로필에 CLIP을 정의하면 CLIP별 프롬프트·검수 양식도 생성합니다. 같은 명령을 다시 실행해도 기존 파일을 덮어쓰지 않습니다. 프로필 변경은 이미 만들어진 프로젝트에 자동 적용하지 않습니다.

이 저장소는 비공개 개인 작업용으로 운영합니다. 실제 시나리오와 이미지는 기본적으로 Git에 올리지 않도록 `projects/`와 미디어 파일을 제외했습니다. 프로젝트 자료를 추가할 때는 필요한 파일과 접근 권한을 먼저 확인하세요. 나중에 공개하려면 공개할 자료만 별도로 선별합니다. Git 제외 규칙은 실수 방지 장치이며, 강제 추가나 웹 업로드까지 막아주지는 않습니다.

## 로컬 영상 확인

아래 기능에는 별도로 FFmpeg와 FFprobe가 필요합니다.

```bash
python scripts/inspect_video.py --video /path/to/clip.mp4 --output /path/to/review-new --times 0,0.5,1,2,4
```

새 출력 폴더에 프레임 이미지와 `inspection.json`을 만듭니다. JSON에는 원본 해시, 실제 재생 길이, 요청 시각, 선택된 프레임의 시각을 기록합니다. 이 도구는 음성을 청취하거나 장면의 품질을 자동 판정하지 않습니다. 기존 출력 폴더를 지정하면 중단해 이전 검수 자료를 보존합니다.

## 현재 가능한 일과 별도 연결이 필요한 일

- 포함: 한국어 제작 지침, 프로젝트 초안 생성, 참조·버전 기록 양식, 로컬 영상 프레임 추출.
- 별도 준비: 확정 시나리오 원문, 실제 참조 이미지, 영상 생성 서비스 이용 권한.
- 미구현: 유료 API 자동 호출, Drive 자동 저장, 일괄 다운로드 UI, 완전 자동 편집·업로드.

모델별 가격·지원 길이·해상도는 고정하지 않았습니다. 실행할 때 실제 서비스에서 확인하며, 비용을 발생시키는 기능은 초기 버전에 넣지 않았습니다.

```bash
python -m unittest discover -s tests -v
```

세부 사용법은 [docs/usage.md](docs/usage.md), 기준 변경 방법은 [docs/change-policy.md](docs/change-policy.md)를 참고하세요.

프로필 작성법은 [docs/profile-format.md](docs/profile-format.md), 원본에서 선별한 구조는 [docs/adaptation.md](docs/adaptation.md)에 정리했습니다.
