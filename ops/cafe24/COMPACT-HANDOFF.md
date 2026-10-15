# TAM 하이라이터 — 현재 인계 / 2026-10-15

## 최신 사용자 지시와 현재 변경

- 사용자는 “이미지만 바꾸라고 했는데 이상한 것까지 바꿨다”고 범위를 바로잡았다. 이전의 전체 페이지 개편 해석은 잘못이었다.
- 이후 “응해봐..피부 위에 빛나는 펄. 여기만 바꾸는 건가?”라고 이미지 교체 진행을 지시했다. 실제 변경은 **ON SKIN 두 칸의 원본 미디어와 포스터만**이다. 나머지는 검토 후 유지했다.
- 기준은 복구본 `049728c`(디자인 내용 `678f30c`/`e5f525c`). 새 소스 커밋 `171894c`.
- 왼쪽: 원본 수진 하이라이터 영상의 세 가지 팔 발색 정지 장면.
- 오른쪽: 같은 원본에서 제품이 빠진 뒤의 손바닥 발색 세 구간. 총 약3.3초. 대기 포스터는 핑크 발색.
- 작은 설명만 실제 부위에 맞게 `손등에 바른 제형` → `손바닥에 바른 제형`. alt/aria도 실제 촬영 내용에 맞춤. **그 밖의 문안/제목/섹션 순서/규격/여백/CSS/JS 모두 유지.**
- 후보이며 사용자 최종 디자인 승인은 받지 않았다. 공개 확인 상태는 `state.json`의 `highlighter_image_only_20261015` 참고.
- 확인 링크: https://gimyedalm-collab.github.io/tam-mall-draft/highlighter-r33/?v=171894c#h33-on-skin

## 작업 위치와 배포

- 활성 체크아웃 `C:/Users/BNK-1/Desktop/tam-vegan-detail-publish`, 브랜치 `vegan-detail-261002`.
- 승인된 GitHub 미리보기 반영: `git push origin HEAD:main`. force push 금지. ChatGPT Sites 금지. Cafe24 운영몰은 변경하지 않음.
- `Desktop/tam-mall-draft-backup`에는 별도 사용자 변경이 있음. 전체 reset/restore 금지. 해당 state 키와 인계만 동기화.
- 소스 `highlighter-r33/detail.template.html`, `detail.css`, `detail.js`. 빌더 `ops/cafe24/build_highlighter_r33.py`. 산출물 standalone index와 preview product24. 옛 R32 빌더 실행 금지.
- CSS `e113a095618e`, JS `c0bd291a1d34` 그대로.

## 유지할 결정

- Milky Cheek V12/product102는 승인되어 잠김. 수정 금지. Lip Liner product118도 이번 변경 없음.
- 기존 립라이너·치크와 이미지 규격/배치/여백/브랜드 분위기 유지. 같은 크기라고 사진의 결까지 같다고 단정하지 말 것.
- `세 가지 펄 컬러.`와 `화이트 · 핑크 · 골드, / 내게 어울리는 펄 컬러.` 유지. 거절된 질문형 문안 및 펄/첫 사용량 FAQ 복귀 금지.
- 손끝에 소량을 덜어 두드리고 스펀지는 경계 스머징용. 직접 얼굴에 문지르는 권장 문구/밀림 없음 주장 금지. 기존 4인 영상은 이번 범위에서 그대로 두었다.
- `7a62cae`는 거절됨: 제품 앞배치, 회색 배경 새 모델 사진, 제형 섹션 삭제, 사용 영상의 제품 누끼 대체를 재적용하지 말 것. 세 얼굴 반복 확대 `348556f`도 거절됨.
- AI 허용은 과거에 있었으나 이번에는 사용하지 않음. 실제 발색을 생성하거나 피부/펄 색을 보정하지 않음.

## 검토와 근거

- 상세 기록 `ops/cafe24/highlighter-r33-image-only-20261015.json`. 소스 해시, 정확한 시간/크롭, 웹 파일 해시 포함.
- 원본: `Desktop/_탐뷰티/PROSTER_젤리라인_SNS소스_260916/04_Seeding_Clean_Videos/creator_highlighter_수진/수진님 하이라이터 컷편집본.mp4`. 같은 폴더의 `컷편집 완료.mp4`는 치크 영상이므로 하이라이터 근거로 사용 금지.
- 편집은 구간 선택/크롭/비례 축소/인코딩만. 색상명·도포 횟수·효능 추정 없음. 손바닥의 농축된 펄이 얼굴에 얇게 바른 결과와 같다고 주장하지 말 것.
- 로컬7폭 검사 통과. 390px 섹션 전후390×475, 전체 높이5681 동일. 템플릿/두산출물 ON SKIN 밖 DOM이 LF 정규화 후 동일. CSS/JS/빌더/치크/립라이너도 동일.
- Claude에 이전/후보/승인치크/영상 프레임을 함께 제공해 독립 검토. `claude -p ... --no-session-persistence --output-format text --tools Read`. 기존 손등 컷을 얼굴로 오인하고 스펀지로 단정한 부분은 채택하지 않음. 밝은 화이트 포스터가 두껍게 보인다는 관찰은 채택해 같은 영상의 핑크 프레임으로 변경.
- 기능 검사/Claude 의견은 사용자 시각적 승인이나 구매 전환 근거가 아님.
- 캡처/원본검토/Claude 원문: `C:/Users/BNK-1/AppData/Local/Temp/tam-image-only/`. 이전 롤백 근거 `ops/cafe24/highlighter-r33-rollback-crosscheck-20261015.json`.

## 다음 작업

사용자 피드백에 따라 이미지 범위 안에서 판단한다. 이미지 교체를 이유로 페이지 구성이나 문안을 또 바꾸지 않는다. Claude는 비대화형·로컬 세션 미저장 옵션 필수. 사용자 다른 세션/인증은 보존한다. PowerShell에서 한국어 Python 파이프는 UTF-8 OutputEncoding을 사용한다.
