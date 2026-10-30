---
name: bbpak-seedance-prompts
description: Create or revise a copy-ready Seedance video prompt from approved images and a fixed CLIP script, preserving identity, visual style, timing, props, dialogue, and audio intent. Use for image-to-video prompts, timed action beats, reference mapping, extending or editing a clip, or correcting a local motion issue. Keep provider capabilities unverified until checked and do not add new story beats.
---

# 비비팍 Seedance 프롬프트

확정 장면을 영상으로 옮기는 지시를 작성한다. 같은 Seedance 이름을 사용하는 서비스도 기능과 입력 문법이 다를 수 있으므로, 제작 목표와 실행 설정을 구분한다.

## 작업 범위

현재 요청에서 사용할 서비스·모델·CLIP 길이·화면 비율·참조 이미지·확정 대사·수정 범위를 찾는다. 서비스의 길이·해상도·참조 개수·오디오 지원이 확인되지 않았으면 `[실행 설정 확인 필요]`로 남긴다. 출처 없는 4K·60fps·긴 영상 지원 등을 보장하지 않는다.

이미지 파일을 직접 보고 참조별 역할을 적는다. 파일을 보지 못하면 역할을 제안할 수는 있지만 참조 확인 완료로 표시하지 않는다. `@image1` 등의 문법은 서비스가 지원하는 경우에만 사용한다.

## 네 부분으로 작성

1. **참조 역할**: 캐릭터, 화풍, 공간, 시작·끝 프레임 등 실제 사용할 역할.
2. **전체 장면**: 확정된 사건·인물·감정·시간·공간을 한 문단으로 정리.
3. **시간별 동작**: 시작부터 끝까지 겹치거나 빠지는 구간 없이 배치. 확정 대사의 시작·끝 시점이 없으면 임의 확정하지 않고 초안으로 제안.
4. **유지 조건**: 인물·의상·소품·카메라·화풍·후반 작업 요소와 원하지 않는 변형.

상세 양식은 [영상 프롬프트 형식](references/video-format.md)을 따른다.

연기·카메라·컷 구성이 필요하면 [장면별 연출 기준](references/directing-patterns.md)을 읽는다. 새 생성·연장·국소 수정 중 작업 방식을 고르거나 여러 컷을 연결할 때는 [작업 방식과 연속성](references/modes-and-continuity.md)을 읽는다. 필요한 자료만 읽고, 다른 장르의 기본값을 현재 작품에 자동 적용하지 않는다.

## 연출 원칙

- 요청한 행동을 중심으로 실현 가능한 작은 동작을 지정한다. 짧은 CLIP에 불필요한 사건·카메라 이동을 쌓지 않는다.
- 사용자 요청이 없으면 새 대사·반전·인물을 추가하지 않는다. 모든 CLIP에 별도 훅이나 빠른 컷 전환을 강요하지 않는다.
- 컵 수, 휴대폰 위치, 가방 방향, 손에 든 물건 등 연속성을 적는다.
- 고정 카메라 요청에 줌·팬을 함께 넣지 않는다. 모션 수정 때문에 확정 화풍을 바꾸지 않는다.
- 음향을 대사, 생활음, 음악, 후반 편집 요소로 나눈다. 한숨을 신음이나 과장된 감정 소리로 바꾸지 않는다.
- 의도된 침묵·호흡·알림 타이밍을 보존한다. 후반 편집 문자는 생성 화면에서 제외한다.
- 정확한 초 단위 동작과 입 모양은 목표이며 보장값이 아니다. 실제 생성 결과로 확인한다.

원문이나 참조가 빠지면 필요한 부분만 질문하고 초안을 계속 준비한다. 최종 응답은 복사용 프롬프트, 실행 설정 상태, 이번 변경점 순으로 제공한다. 프롬프트 작성만 요청했을 때 생성 API를 호출하지 않는다.
