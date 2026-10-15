# TAM 하이라이터 — 현재 작업 인계 / 2026-10-15

## 가장 최근 사용자 지시와 현재 상태

- 사용자: 최신 수정본이 최악이며 산으로 간다고 강하게 거절. **전 버전으로 복구 → 교차검증 → 컴팩 작업**을 지시했다.
- 복구·교차검증까지 수행했다. **이 턴에서 추가 디자인 수정은 하지 않는다.** 다음 디자인 변경은 새로운 사용자 지시를 따른다.
- 실제 복구 기준은 직전 버전 `678f30c`(페이지 내용 커밋 `e5f525c`). 공개 복구 커밋 `e49eeb2`.
- 확인 링크: https://gimyedalm-collab.github.io/tam-mall-draft/highlighter-r33/?v=e49eeb2
- 거절된 최신 디자인 `7a62cae`를 다시 적용하지 않는다. 회색 배경 모델 사진, 제품 앞배치, 사용법 정지 제품컷 교체를 되돌렸다.
- **복구본도 승인된 최종 디자인이 아니다.** 팔 컷이 어둡고 노랗게 보이며 손등 영상은 바르는 동작만 보여준다는 기존 불만이 남아 있다. 사용자의 롤백 지시 때문에 그대로 복원했다.

## 작업 위치

- 활성 체크아웃: `C:/Users/BNK-1/Desktop/tam-vegan-detail-publish`
- 브랜치: `vegan-detail-261002`; 원격: `gimyedalm-collab/tam-mall-draft`
- 승인된 GitHub 미리보기 반영 방식: `git push origin HEAD:main`. force push 금지.
- `Desktop/tam-mall-draft-backup`에는 별도 사용자 변경이 있다. 전체 복원/리셋 금지. 재개용 state 키만 갱신했다.
- Cafe24 운영몰은 변경하지 않았다. GitHub의 product-24는 구매 기능 완성이 아닌 미리보기다.
- ChatGPT Sites 사용 금지. GitHub/GitHub Pages만 사용한다.

## 현재 페이지와 원본

- 소스: `highlighter-r33/detail.template.html`, `detail.css`, `detail.js`.
- 빌더: `ops/cafe24/build_highlighter_r33.py`. 결과: `highlighter-r33/index.html` 및 `storefront-v2/preview/product-24.html`의 scoped detail.
- 활성 순서: hero/glow → 3색 비교 → 팔/손등 ON SKIN → 제형/펄 확대 → 4인 사용 영상과 사용법 → 성분 → 제품 마무리 → 제품정보.
- CSS 버전 `e113a095618e`, JS 버전 `c0bd291a1d34`.
- 새 디자인에서 추가했던 `original-product-still.jpg`, `original-finished-look.jpg`, `original-stick-sponge.webp`는 활성 트리에서 제거했다. Git의 거절된 커밋에 기록은 남아 있다.
- 원본 자료: `Desktop/_탐뷰티/PROSTER_젤리라인_SNS소스_260916/05_Product_Cuts/01_Beam_Highlighter`.
- 원본 영상 경로 목록: `Desktop/_탐뷰티/하이라이터_WOW_R32_261002/source-map.json`.
- 추가 생성 AI는 이번 복구 작업에 사용하지 않았다. 원본 색상/피부톤을 보정해서 발색을 만들어내지 않는다.

## 유지해야 할 사용자 결정

- Milky Cheek V12/product102는 최종 승인되어 잠겨 있다. 수정 금지.
- 기존 립라이너·치크와 이미지 규격, 배치, 여백, 브랜드 분위기를 맞추라는 요구가 기본이다.
- 색상 제목 `세 가지 펄 컬러.` 유지. 거절된 질문형 제목과 펄/첫 사용량 FAQ 복귀 금지.
- 마무리 문안 `화이트 · 핑크 · 골드, / 내게 어울리는 펄 컬러.` 유지.
- 손끝에 소량을 덜어 두드리고 스펀지는 경계 스머징에 사용. 얼굴에 직접 문지르면 밀린다는 사용자 설명을 무시하지 않는다.
- 세 얼굴 사진을 크게 반복한 `348556f`도 거절됐다. 사진을 추가해 길이만 늘리지 않는다.
- 기존 소스를 먼저 활용하고 없으면 AI를 쓸 수 있다는 허용은 있었지만, 실제 발색 근거와 생성 연출을 혼동하지 않는다.
- Claude는 반드시 비대화형 `claude -p ... --no-session-persistence --output-format text`. 사용자 다른 세션/인증을 건드리지 않는다.

## 검증 완료 사실

- template/CSS/index/JS/builder/regression/product24의 7개 파일을 `678f30c`와 LF 정규화 후 비교해 일치 확인.
- 로컬 320/390/600/720/800/860/1440px 검사 통과: 넘침, 원본 미디어, commerce DOM, 제품정보, 동작/정지 및 reduced motion.
- 공개 320/390/860px에서 단독/상품 미리보기 확인. 공개 HTML/CSS/팔 사진/손등 영상·포스터가 로컬과 일치.
- `check_highlighter_r33_story.py`의 기존 제목/FAQ 제거/색상·구매영역 링크 검사 통과.
- 위 검사는 **복구 정확성과 기능 검증**이다. 구매 소구력이나 사용자 승인을 증명하지 않는다.

## 교차검증 — 반복하면 안 되는 실패

1. 규격/글자/재생 체크를 디자인 만족도 검증처럼 보고했다. 승인된 치크와 실제 촬영 분위기를 함께 비교하지 못했다.
2. 개별 이미지 문제에서 시작해 제품 앞배치, 새 얼굴 사진, 제형 섹션 삭제, 사용 영상 삭제까지 변경폭을 키웠다. 기준 화면과 변경 범위를 고정하지 않았다.
3. 부적절한 도포 영상을 정지 제품 컷으로 바꿔 모순은 없앴지만, 올바른 사용법이나 완성 발색을 더 잘 보여주는 증거를 확보하지 못했다.
4. 이전 Claude 요청은 새 수정안의 장점을 설명하며 새 화면만 보여줬다. 이번에는 복구본 A / 거절본 B / 승인 치크 C를 같은 모바일 폭으로 비교시켰다.
5. Claude도 틀릴 수 있다. 이번 답변 중 손등 영상의 접촉 끝을 스펀지로 단정한 부분, ON SKIN 영상이 두 개라는 부분, A/B 사용법이 같다는 부분은 실제 자료와 맞지 않거나 불확실해 채택하지 않았다.
6. 채택한 결론: A의 불일치는 여전히 남아 있고, B는 제거와 대체 과정에서 필요한 시각 근거를 줄였다. 최종 미감은 미승인이다.

다음 작업 시 페이지 전체를 또 재편하지 말 것. 정확한 기준 화면을 고정하고, 후보 소스가 **완성 발색/컬러 차이/권장 사용법 중 무엇을 실제로 보여주는지** 확인한 뒤 변경 부분만 같은 조건으로 비교한다. 미확인 색상명·도포 횟수·효능은 붙이지 않는다.

## 상세 기록과 재개

- 현재 상태: `ops/cafe24/state.json`의 `highlighter_rollback_20261015`.
- 교차검증: `ops/cafe24/highlighter-r33-rollback-crosscheck-20261015.json`.
- 비교 캡처/Claude 원문: `C:/Users/BNK-1/AppData/Local/Temp/tam-rollback-review/`.
- 공개 검증 스크립트: Temp의 `tam_verify_source_reuse.py`; 복구 커밋 인수 `e49eeb2`.
- 셸에서 한국어 Python을 파이프로 전달할 때 `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)` 설정. ASCII 물음표 손상 주의.
- **컴팩 상태:** 재개용 핵심 기록을 이 파일로 압축했다. 현재 세션에 대화 컨텍스트 강제 압축을 실행하는 호출 도구는 없다. 실제 대화 압축 명령을 실행했다고 주장하지 않는다.
