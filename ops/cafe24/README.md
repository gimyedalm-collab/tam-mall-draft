# 탐뷰티 Cafe24 작업 재개

사용자가 **“탐뷰티 카페24 진행해”**라고 요청하면 `state.json`과 `bugs.json`부터
읽고 다음 작업을 이어간다. 기존 기능과 운영 조건을 유지하는 것이 기본이다.
디자인 기준은 `tam-design-fixed-20260917`이며 이번 준비 작업은 운영몰을 변경하지 않았다.

## 전용 에이전트

- 정의: `.codex/agents/tam_cafe24.toml`, 이름 `tam_cafe24`.
- 작업 절차: `.agents/skills/tam-cafe24/SKILL.md`.
- 기록: `feature-inventory.json`, `live-audit-20260917.md`, `bugs.json`, `state.json`.
- 이 저장소를 프로젝트로 연 새 Codex 세션에서 에이전트 설정을 읽는다.
  현재 런타임이 사용자 에이전트 선택을 지원하지 않으면 메인 세션이 같은 스킬로 수행한다.
  에이전트 파일 작성/구문 검사와 런타임 에이전트 호출 성공은 구분한다.
- 모델과 실행 권한은 상위 세션을 상속한다. 별도 API 키나 상시 서버는 필요하지 않다.
- 자동 24시간 감시나 예약 실행은 구성하지 않았다. 요청을 받으면 기록을 이어서 작업한다.

## 로그인 연결

`tam_browser`는 Playwright MCP 0.0.81을 사용한다. 기존 브라우저 프로필 점유 문제를
피하도록 전용 프로필을 `C:/Users/BNK-1/.codex/browser/tam-cafe24`에 보관한다.
출력도 Git 밖의 `tam-cafe24-output`에 둔다. 다른 PC에서는 TOML의 두 경로를 바꾼다.
Node/npm, Chrome, Python Playwright가 필요하며 현재 PC에서 확인한다.

2026-09-17 전용 프로필로 MCP 초기화, 탭 조회, 공개 공식몰 접속을 headless로 시험했고
성공했다(`browser-setup-check.json`). 관리자 로그인이나 인증 유지까지 검증한 것은 아니다.
이 PC에는 같은 스킬을 `C:/Users/BNK-1/.codex/skills/tam-cafe24`에도 설치했다.

관리자 로그인 화면을 연 다음 사용자가 직접 로그인/2차 인증한다. 비밀번호를 채팅이나
저장소에 남기지 않는다. 로그인 후 몰/스킨/권한 확인, 원본 백업·복사, 앱과 정책 조회는
작업자가 진행한다. 디자인·상품·게시판·프로모션/쿠폰·배송·관련 앱 접근 및 검수에 필요한
주문 확인 권한이 필요하다. 본인인증, 별도 서비스 로그인, 외부 계약은 사용자 참여가
필요할 수 있다. 로그인 지속 여부는 서비스의 세션 정책에 따른다.

스킨 복사는 쿠폰·배송·상품 설정을 격리하지 않는다. 기존 상업 조건을 읽고 보존하며,
고객 일괄 알림이나 실제 결제는 단순 화면 검수에 포함하지 않는다.

## 반복 점검

```powershell
python -X utf8 ops/cafe24/smoke.py
python -X utf8 ops/cafe24/smoke.py --base-url https://tambeauty.kr/skin-skinXX/
```

두 번째 URL은 형식 예시이며 실제 관리자에서 확인한 미리보기 경로로 대체한다.
기본 출력 `runs/public-smoke.json`은 Git에서 제외된다. 결과는 HTTP/화면 넘침/보이는
이미지/네이티브 옵션 선택 후 금액 변화/로그인 필드 등 공개 화면 검증이다.
실패는 재현 후 판단하며 곧바로 운영몰 코드를 바꾸지 않는다. 스크립트는 로그인,
장바구니 추가, 쿠폰 발급, 주문 제출을 하지 않는다. 모바일 검사는 좁은 화면 에뮬레이션이며
실물 기기 또는 모바일 전용 스킨 검수를 대체하지 않는다.

쿠폰 적용, 배송 경계값, 옵션별 재고, 후기 작성, 결제 완료와 반환은 별도 인증 검증이
필요하다. 단순 버튼 노출을 이 항목들의 성공으로 기록하지 않는다.

## 참고

- [Codex 사용자 에이전트 공식 문서](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Cafe24 구현 범위와 공식 모듈 근거](../../CAFE24-IMPLEMENTATION-PLAN.md)
