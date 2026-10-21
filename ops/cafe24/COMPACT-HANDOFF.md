## ACTIVE: main storefront sync, 2026-10-21

Owner requested all completed work applied to GitHub main except shading duo.
Current worktree: Desktop/tam-main-sync-261021. Six routes110,111,25,118,102,24
now embed their existing Cafe24 registration compositions; product109 unchanged.
Cloud V13 and Powder Balm V5 had been published standalone but were absent from
main product details. Lip Oil V9 is a01-03 component within product25, preserving
00 gloss, all existing options and original common series panels. Other latest
compositions are R34 liner, V12 cheek, R33 highlighter. Main film V16 was already
connected. Run sync_storefront_details.py after package or old-builder changes.
See main-sync-20261021.json for verification; live Cafe24 upload remains deferred.

---

# TAM 하이라이터 — 현재 인계 / 2026-10-15

## 현재 기준: 사용자 확인 후 일단 마감 · 2026-10-15

- 사용자: “그래 하이라이터는 일단 이렇게 포지션 마무리하자고”. 현재 하이라이터 포지션/상세 버전을 마감하고 기준본으로 유지.
- 기준 소스 `a0d8129`: 공식 팔 발색 + 제품·제형 두 사진, PC 폰트 마무리, 기존 모바일/문안/섹션 구성 포함.
- 새 요청 전까지 추가 디자인 변경을 진행하지 않음. 이전 성분 구간 의견은 미완료 개편 과제로 자동 재개하지 말 것.
- state `highlighter_owner_close_20261015`. 아래의 승인 대기 문구는 마감 전 이력이며 이번 사용자 확인이 우선함.
- Cafe24 운영몰 적용 완료를 의미하지 않음. 이번 마감은 GitHub 미리보기의 하이라이터 버전에 해당.

## LATEST: PC typography finish, 2026-10-15

- Owner requested PC font-size review and completion. Published source `a0d8129`: https://gimyedalm-collab.github.io/tam-mall-draft/highlighter-r33/?v=a0d8129
- Added font-size-only override for detail containers>=760px: hero64px, section headings48px, intro26px, body24px, swatch captions20px, footnotes16px. Heading weight, wording, layout rules, original media and JS stay unchanged.
- CSS revision `88f24509d2f8`. Template unchanged; generated HTML changes only the CSS cache revision. Narrow containers/mobile/tablet below760px retain prior typography.
-7width regression passed. Additional integrated desktop1280/1440/1920 checked;390/720 entire text metrics and page heights identical before/after. Public390/1440/1920 on both routes verified, including computed font sizes and exact files. Brief CDN delay resolved before completion.
- Report `highlighter-r33-pc-typography-20261015.json`; state `highlighter_pc_typography_20261015`; review captures in Temp/tam-pc-type-final. Requested work complete; owner visual acceptance remains separate.
- Keep the official two-photo pair below. Formula content/image was reviewed previously but not redesigned; this turn changes its PC font sizes only. Cafe24 production untouched.

## LATEST: official arm / texture photograph pair, 2026-10-15

- Source commit `af017df`: https://gimyedalm-collab.github.io/tam-mall-draft/highlighter-r33/?v=af017df#h33-on-skin
- Owner authorized trying candidate1 arm swatches left + candidate3 product/texture right in the existing ON SKIN frames. Candidate2 palm video rejected for visible skin creases.
- Current `official-arm-three-shades-261015.jpg` and `official-three-pearl-textures-261015.jpg` are byte-identical official SNS originals. Original shade labels retained. No AI-generated swatches published.
- ON SKIN video/button/data-motion removed; right caption and alt now describe the texture photograph. All other HTML, headings, geometry, CSS/JS unchanged.390px page height5681px unchanged.
- Formula section was reviewed but not changed. Do not infer authorization for a broader redesign.
-7localwidths and3publicwidths/2routes passed. Public/source files verified. Owner visual acceptance pending.
- Report: `highlighter-r33-official-pair-20261015.json`. State: `highlighter_official_pair_20261015`. Source/AI review evidence: Temp/tam-source-search-261015; public checks: Temp/tam-official-pair.

## 최신 진행: 영상 테두리 깨짐 수정

- 사용자 지적: 배경 정리 후 영상이 조금 깨져 보임. 확인된 문제는 손 윤곽의 톱니 모양 잘림과 회색 테두리.
- 공개 소스 `8503f92`: https://gimyedalm-collab.github.io/tam-mall-draft/highlighter-r33/?v=8503f92#h33-on-skin
- **오른쪽 손바닥 영상과 포스터만 교체**. 왼쪽 팔 이미지, 문안, CSS/JS, 규격, 배치, 기타 미디어 그대로.
- 현재 `palm-pearl-smooth-261015.mp4` / `palm-pearl-smooth-poster-261015.jpg`. 원본의 동일 세 구간을30fps/99프레임/3.3초로 재출력. 경계 정리·인접 프레임 마스크 추적·부드러운 가장자리 처리. 밝은 배경 유지. 발색 중앙 영역은 인코딩 전 원본 픽셀과 동일.
- 재생성은 `build_highlighter_palm_edge_fix.py --source <original> --review-dir <temp>` 사용. 이전 배경 빌더로 현재 파일 덮어쓰지 말 것.
-7폭 로컬 검사, 공개3폭/2경로 재생·정지·모션 감소·가로 넘침 및 파일 일치 확인. 전체99프레임 디코딩 정상. 이 결과가 사용자 시각적 승인은 아님.
- 상세 `highlighter-r33-video-edge-fix-20261015.json`, state `highlighter_video_edge_fix_20261015`. 이번 수정에 새 Claude 검토 완료를 주장하지 않음.

## 직전 진행: 배경 정리

- 공개 소스 커밋 `75c4620`: https://gimyedalm-collab.github.io/tam-mall-draft/highlighter-r33/?v=75c4620#h33-on-skin
- 이번 배경 편집의 추가 Claude 검토는300초시간초과로 완료되지 않음. 완료/승인으로 보고 금지. 자체 소스·발색보존·레이아웃·브라우저 검증은 완료.

- 사용자가 두 소스 방향은 “좋은데”라고 했지만 배경이 어두워 더러운 느낌이라고 지적. 다른 소스 검토 및 편집을 지시했다.
- 추가 편집 영상20개를 확인. 따뜻한 피부톤/자막이 있는 다른 팔 컷 및 얼굴 도포 컷들보다 현재의 세 가지 팔 발색과 완성 손바닥 소스를 유지하고 배경만 정리하는 쪽을 선택.
- `arm-three-pearls-clean-261015.svg`: 원본 JPEG 바이트를 그대로 포함하고 피부 바깥만 밝은 아이보리로 가리는 native SVG. 펄과 피부를 재생성하지 않음.
- `palm-pearl-clean-261015.mp4` 및 포스터: 원본79프레임의 구도/속도 유지, 피부 경계를 따라 배경과 드리운 그림자만 정리. 색/노출 필터 없음.
- 이미지 생성 도구의 배경 편집본은 펄 미세질감도 달라져 **채택하지 않음**. 지나친 확대 크롭도 제외.
- 제목/본문/작은 설명/CSS/JS/배치/여백/기타 이미지 모두 그대로.
- 상세/검증: `ops/cafe24/highlighter-r33-background-cleanup-20261015.json`. 공개 링크와 완료 상태는 state의 `highlighter_background_cleanup_20261015` 확인. 사용자 최종 시각 승인은 대기.
- 재생성 스크립트 `ops/cafe24/build_highlighter_swatch_background.py`. 검토 임시자료 `Temp/tam-clean-background/`.

## 직전 이미지 교체 내역

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
