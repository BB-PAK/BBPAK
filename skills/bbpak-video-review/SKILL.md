---
name: bbpak-video-review
description: Review generated images, video clips, and audio against BBPAK's approved script and references, distinguishing observed defects from unverified claims. Use for identity drift, hand and prop continuity, timing, dialogue, natural sound, or deciding the smallest useful correction. A sampled frame inspection does not count as full video playback or audio listening.
---

# 비비팍 영상 검수

실제 결과에서 확인한 문제와 가장 작은 수정안을 연결한다. 출력 파일을 보지 않고 결과를 평가하지 않는다.

## 먼저 확인

확정 시나리오, 기준 이미지, 생성 프롬프트, 실제 결과 파일, 요청한 검수 범위를 확보한다. 읽지 못한 파일과 청취하지 못한 음향은 미확인으로 적는다.

메타데이터만 읽었으면 메타데이터 확인, 프레임만 봤으면 표본 프레임 확인, 전체를 재생했으면 전체 재생, 음향을 들었으면 청취로 구분한다. 자막·음성 인식 결과만으로 실제 발음·음색·효과음의 품질을 판정하지 않는다.

저장소가 함께 제공되고 로컬 파일을 쓸 수 있으면 `scripts/inspect_video.py`를 이용해 실제 길이와 관심 시각의 프레임을 확인할 수 있다. 스크립트가 없으면 가능한 재생 도구를 사용한다. 어떤 도구도 사용하지 못하면 검수 체크리스트만 제공하고 결과 판정을 보류한다.

## 검수 순서

1. 요청 범위와 실제 재생 길이·화면 비율을 확인한다.
2. 기준 참조 대비 인물·화풍·공간을 확인한다.
3. 손, 얼굴, 컵·휴대폰·가방 등 소품의 수·위치·접촉을 확인한다.
4. 동작과 카메라가 요청한 시간 구간에 맞는지 확인한다.
5. 실제 청취 가능한 경우 대사·생활음·배경음·의도된 침묵을 확인한다.
6. 후반 편집 예정인 문자와 UI가 원본에 생기지 않았는지 확인한다.

요청과 관계없는 취향 변경을 결함으로 처리하지 않는다. 순간적인 문제는 그 주변을 더 촘촘히 확인하고 표본 사이의 구간은 단정하지 않는다. 프레임 시각은 요청 시각과 실제 선택 시각을 구분해 기록한다.

## 수정 제안

치명적인 연속성 문제, 장면 이해를 방해하는 문제, 선택적인 미세 조정을 구분한다. 후반 편집으로 가능한 해결과 재생성이 필요한 해결을 비교한다. 손 동작 하나를 수정하기 위해 시나리오·캐릭터·화풍 전체를 바꾸지 않는다.

무음 자동 제거로 의도된 쉼·호흡·효과음 간격이 사라질 수 있으므로 구간을 확인하고 처리한다. 볼륨 수치나 무음 검출만으로 자연스러움을 판단하지 않는다.

[검수 기록](references/review-format.md)으로 결과를 제공한다. 실제 확인 범위를 명시하고, 사용자가 승인하지 않은 결과를 최종 승인으로 표시하지 않는다.
