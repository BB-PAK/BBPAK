---
name: bbpak-video-director
description: Plan and continue BBPAK's AI video production in Korean while preserving approved scripts, characters, visual style, and clip timing. Use for project setup, episode and CLIP planning, next-step decisions, reference organization, version tracking, or coordinating image prompts, video prompts, and review. Do not automatically install tools or call paid generation APIs.
---

# 비비팍 영상 제작 진행

제작 순서를 정리하고 지금 필요한 작업을 수행한다. 이미 결정된 사항을 다시 만들지 않는다.

## 기준 확인

1. 사용자의 현재 요청과 첨부한 최신 확정본을 읽는다.
2. 가능하면 프로젝트의 `brief.md`, `script-source.md`, `project.json`, `references.json`을 읽는다. 다른 위치의 파일도 사용할 수 있다.
3. 프로젝트의 원문이 없으면 전체 시나리오를 기억이나 초기 프로필로 복원하지 않는다. 확보한 정보와 누락된 정보만 구분한다.
4. 프로젝트별 인물·화풍·화면 비율·길이를 다른 프로젝트에 자동 적용하지 않는다.

## 진행

- 기획 요청이면 목표·대상·플랫폼·총길이·CLIP별 역할을 정리한다. 확정 내용과 새 제안을 구분한다.
- 이미지 준비 요청이면 장면별 참조 역할과 화면에 필요한 요소를 정리한다.
- 영상 요청이면 확정 이미지·동작·길이·대사·음향을 확인한다.
- 검수 요청이면 실제 결과를 확인해 수정 범위를 좁힌다.
- 전체 작업 요청이면 아직 완료되지 않은 단계부터 이어간다. 매 단계마다 형식적인 승인 질문을 반복하지 않는다.
- 필요한 자료가 없으면 그 자료에 의존하는 최종 생성만 보류한다. 양식·참조 목록·작업 순서 같은 독립적인 준비는 진행한다.

현재 저장소를 함께 사용하는 경우 이미지 작업은 `bbpak-image-prompts`, 영상 작업은 `bbpak-seedance-prompts`, 검수는 `bbpak-video-review`를 참고한다. 별도 스킬이 없더라도 여기의 보존 원칙과 [작업 기록](references/work-record.md)에 따라 준비 작업을 계속할 수 있다.

## 파일 관리

저장소가 있으면 `scripts/new_project.py`의 도움말을 확인해 프로젝트 폴더를 만든다. 스킬 단독 사용 환경에 해당 스크립트가 없으면 실행했다고 주장하지 않고 같은 구조의 작업 기록을 작성한다.

원문, 참조 목록, 이미지 프롬프트, 영상 프롬프트, 결과, 검수를 연결한다. 승인본을 덮어쓰지 않고 변경본의 버전을 올린다. 사용자 승인 없이 `approved` 상태로 바꾸지 않는다.

## 보고

한국어 존댓말로 먼저 결과를 설명한다. 이어서 필요할 때만 다음을 제시한다.

- 확인한 기준과 출처
- 이번에 수행한 작업
- `[확인 필요]` 자료와 그 자료에 의존하는 작업
- 다음에 바로 할 수 있는 한 가지 작업

유료 작업은 기존 허용 범위 안에서만 실행한다. 그 범위가 없거나 바뀌면 모델·수량·예상 비용을 먼저 제시한다. 모델 사양은 현재 사용하는 서비스에서 확인한다.
