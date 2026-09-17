# 쿠션 상세페이지 최종본 적용

사용자가 `GELLY-SKIN-cushion_0908`을 쿠션 최종 파일로 지정했다.
실제 파일은 다운로드 폴더의 `jelly-skin-cushion_0908.zip` 및 같은 이름의 해제 폴더다.
누끼컷 교체 자료가 아니라 상세페이지 10개 구간의 이미지·움직이는 WebP 패키지임을 확인했다.

- 상세 원본 10개를 원본 HTML 순서로 적용. JPG 7개와 애니메이션 WebP 3개.
- 기존 원격 상세 이미지 3개를 교체하고, 접힌 details 대신 펼쳐진 제품 상세 영역으로 표시.
- 원본 860px 폭을 초과해 확대하지 않으며 모바일에서는 화면 폭에 맞춤. 구간 사이 간격 없음.
- 색 보정·재인코딩 없음. 원본/미리보기/Cafe24 패키지 SHA-256 일치.
- WebP는 253/288/65프레임 유지. 원본 총 43,778,675바이트; 아래쪽 구간은 지연 로딩.
- 원본 HTML의 `.JPG` 대문자 참조와 실제 `.jpg` 파일명의 차이를 수정하여 Linux/Pages 경로 오류 방지.
- 별도 MP4는 원본 HTML에 사용되지 않아 불필요하게 추가하지 않음.

## 적용 위치

- 미리보기: `storefront-v2/preview/product-23.html#product-detail`
- 이미지: `storefront-v2/preview/assets/jelly-skin-cushion-0908/`
- Cafe24 이미지 업로드 대상: `/tam/assets/jelly-skin-cushion-0908/`
- Cafe24 상품 23 상세설명용 HTML: `storefront-v2/cafe24/tam/sections/cushion-detail-0908.html`
- 파일 순서·크기·프레임·해시 기록: `cushion-detail-0908.json`

관리자 접속 후 상품 23의 기존 상세설명을 백업하고 해당 상품 설명에만 적용한다.
전 상품 공통 스킨 영역에 삽입하지 않는다. 실제 운영몰 상세설명은 아직 변경하지 않았다.

## 재실행

```powershell
python -X utf8 ops/cafe24/import_cushion_detail.py
python -X utf8 ops/cafe24/check_cushion_detail.py
```

두 번째 명령은 PC 1440px·모바일 390/320px에서 전 구간 이미지 로드, 순서·크기,
구간 사이 틈, 가로 넘침, 404·콘솔 오류를 검사하고 로컬 화면 증거를 저장한다.
