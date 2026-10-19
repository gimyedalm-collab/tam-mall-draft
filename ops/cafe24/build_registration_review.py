from pathlib import Path
from PIL import Image
import json,re,shutil,html,zipfile
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cafe24-delivery-20261019'
qa=json.loads((OUT/'qa.json').read_text(encoding='utf-8'))
rows=[];compare=[]
for q in qa:
    key=q['product'];m=json.loads((OUT/key/'manifest.json').read_text(encoding='utf-8'))
    native=' + 정보 HTML' if m.get('product_information') else ''
    rows.append(f'<tr><th>{m["product"]}</th><td>{q["files"]}개 / GIF {q["gifs"]}개{native}</td><td>{q["total_bytes"]/1e6:.1f}MB</td><td><a href="{key}/index.html">미리보기</a> · <a href="{key}-cafe24.zip" download>등록 파일</a></td></tr>')
    for i,item in enumerate(m['files']):
        if item['kind']!='gif':continue
        source='../'+item['source'];after=key+'/'+item['file']
        if Path(source).suffix.lower()=='.mp4':before=f'<video controls muted playsinline preload="metadata" src="{source}"></video>'
        else:before=f'<img loading="lazy" src="{source}" alt="변환 전 원본">'
        compare.append(f'<section><h2>{m["product"]} · 움직이는 소재 {i+1:02}</h2><p class="small">{item["duration_seconds"]:.1f}초 · {item["width"]}px · {item["fps_target"]}fps · {item["bytes"]/1e6:.2f}MB · 3회 재생 후 정지</p><div class="pair"><figure><figcaption>원본 · 비교용</figcaption>{before}</figure><figure><figcaption>카페24용 GIF</figcaption><img loading="lazy" src="{after}" alt="카페24용 변환본"></figure></div></section>')

# External MP4 integration kit: production host is intentionally unconfigured.
ext=OUT/'highlighter-external';(ext/'video').mkdir(parents=True,exist_ok=True);(ext/'posters').mkdir(exist_ok=True)
base=(OUT/'highlighter/detail.cafe24.html').read_text(encoding='utf-8')
m=json.loads((OUT/'highlighter/manifest.json').read_text(encoding='utf-8'))
external=[]
for item in m['files']:
    if item['kind']!='gif' or not item['source'].endswith('.mp4'):continue
    src=ROOT/item['source'];shutil.copy2(src,ext/'video'/src.name)
    poster=src.stem+'.jpg';im=Image.open(OUT/'highlighter'/item['file']);im.convert('RGB').save(ext/'posters'/poster,quality=95)
    oldpath='/web/upload/tam-detail-20261019/highlighter/'+Path(item['file']).name
    old=re.search(r'<img[^>]+src="'+re.escape(oldpath)+r'"[^>]*>',base).group()
    full='real-glow' in src.name
    video=f'<div style="position:relative;width:100%;aspect-ratio:{item["width"]}/{item["height"]};background:#fff;"><video controls muted playsinline loop preload="none" poster="/web/upload/tam-detail-20261019/highlighter/{poster}" style="position:absolute;left:{0 if full else 5.6}%;top:0;width:{100 if full else 88.8}%;height:100%;object-fit:contain;" aria-label="{html.escape(item["alt"],quote=True)}"><source src="{{{{VIDEO_BASE_URL}}}}/{src.name}" type="video/mp4"></video></div>'
    base=base.replace(old,video)
    external.append({'file':src.name,'source_sha256':item['source_sha256']})
(ext/'detail.external.template.html').write_text(base,encoding='utf-8')
(ext/'README.txt').write_text('하이라이터 외부 영상 삽입안 — 호스팅 연결 전\n\n펄 표현 보존을 위해 MP4 원본 2개를 그대로 보관했습니다.\nvideo 폴더는 카페24 쇼핑몰 FTP 업로드용이 아닙니다. HTTPS 영상 호스팅에 올리고 {{VIDEO_BASE_URL}}을 실제 주소로 치환해야 합니다.\n기본 하이라이터 images와 posters 파일은 /web/upload/tam-detail-20261019/highlighter/에 업로드합니다.\n별도 JS 없이 기본 재생 컨트롤을 사용하며 자동 재생을 전제로 하지 않습니다.\n실제 카페24 저장 후 PC/모바일 재생, 응답 형식, 탐색, 실패 시 포스터를 확인하기 전 적용 완료로 보고하지 않습니다.\n',encoding='utf-8')
(ext/'status.json').write_text(json.dumps({'status':'prepared; video hosting and Cafe24 playback unverified','files':external},indent=2),encoding='utf-8')
with zipfile.ZipFile(OUT/'highlighter-external-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in ext.rglob('*'):
        if f.is_file():z.write(f,f.relative_to(ext))

page='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>TAM · 카페24 등록본과 영상 변환 비교</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f2f5;color:#29232c;font:16px/1.8 system-ui,sans-serif;word-break:keep-all}main{max-width:1040px;margin:auto;padding:32px 24px 70px}h1{font-size:clamp(28px,4vw,40px);line-height:1.3}h2{font-size:23px}a{color:#654c6a;text-underline-offset:4px}table{width:100%;border-collapse:collapse;background:#fff}td,th{text-align:left;padding:14px 12px;border-bottom:1px solid #ddd}section{margin-top:36px;padding-top:20px;border-top:1px solid #ddd}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}figure{margin:0;background:white;padding:12px}figcaption{margin-bottom:12px}img,video{display:block;max-width:100%;width:100%;max-height:560px;object-fit:contain}.small{font-size:13px;color:#756b79}.callout{background:#eae2ee;padding:20px}.table-wrap{overflow-x:auto}@media(max-width:650px){main{padding:24px 16px}.pair{grid-template-columns:1fr}td,th{padding:10px 7px;font-size:13px}}</style></head><body><main><p class="small">2026.10.19 · CAFE24 등록 기준 · 운영몰 반영 전 검토</p><p><a href="cloud-rebalance-review/index.html">클라우드 블러 · 발색 복원과 정보 크기 수정 비교</a> · <a href="claude-cloud-review.html">이전 독립 검토 기록</a></p><h1>등록 파일과 미리보기를<br>같은 구성으로.</h1><p>기본 상세는 JPG·PNG·GIF로 구성했습니다. 클라우드 하단 제품정보·전성분은 일반 HTML 텍스트로 포함했습니다. 별도 스크립트, 웹폰트, 영상 장면 선택 버튼 없이 표시됩니다. 기존 디자인은 모바일 430px 화면을 기준으로 출력했고, 립라이너는 현재 연결된 R34 파일을 사용했습니다.</p><div class="table-wrap"><table><thead><tr><th>제품</th><th>등록 이미지</th><th>전체 용량</th><th>확인 / 다운로드</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table></div><p class="small">각 파일 4.9MB 미만. 아래쪽 파일은 지연 로딩합니다. GIF는 3회 재생 후 멈춥니다. 표의 용량은 상품별 모든 이미지를 합한 값입니다.</p><div class="callout"><strong>하이라이터: 원본 영상 삽입안을 우선 검토</strong><p>GIF의 색상 수와 프레임 제한 때문에 미세한 펄과 피부 질감에는 차이가 남습니다. 원본 MP4를 별도 HTTPS 영상 호스팅에 연결하는 등록 템플릿도 준비했습니다. 현재 호스팅 연결과 실제 카페24 재생 확인은 미완료입니다.</p><a href="highlighter-external-kit.zip" download>외부 영상 연결용 파일</a></div><p>클라우드는 원본의 세 장면에서 4.4초를 선택했습니다. 밀키치크·하이라이터·립라이너는 원본 구간을 유지했습니다. 원본 사진과 영상 파일에는 색 보정이나 재생성을 하지 않았습니다.</p><p class="small">등록 HTML은 예정 경로 /web/upload/tam-detail-20261019/를 사용합니다. 카페24에 파일을 올리기 전에는 작동하는 주소가 아닙니다. 브라우저 확인과 운영몰 적용 완료를 구분합니다.</p>'''+''.join(compare)+'''<section><h2>확인 범위</h2><p>320·390·860px에서 자바스크립트를 끄고 파일 표시, 가로 넘침, 이미지 사이 틈을 확인했습니다. GIF 전체 프레임 디코딩과 ZIP 파일 검사를 통과했습니다. 카페24 관리자 저장, 모바일 상품 상세 반영 및 실제 기기 확인은 다음 적용 단계입니다.</p><p><a href="qa.json">확인 기록</a> · <a href="https://support.cafe24.com/hc/ko/articles/17460428614041">카페24 MP4·이미지 등록 공식 안내</a></p></section></main></body></html>'''
(OUT/'index.html').write_text(page,encoding='utf-8')
print('Review and external-host integration kit prepared')
