"""상품 상세 미리보기의 고객 리뷰 영역 (v3, 2026-09-21).

실제 쇼핑몰 리뷰 모듈 구조: 평점 요약 -> 포토 후기 모음 -> [전체 / 포토] 탭 + 정렬 -> 목록 -> 페이지 번호.
발췌가 아니라 그 상품의 공개 후기 전부를 데이터 파일로 넣고 assets/reviews.js 가 그린다.

입력: 바탕화면/_탐뷰티/리뷰_전체수집_260921/reviews_all.json (리포 밖, 커밋하지 않음)
출력: storefront-v2/preview/assets/reviews-data/p{상품번호}.js  (window.TAM_REVIEWS)
      storefront-v2/preview/product-*.html 의 Discover more 앞에 섹션 뼈대 + 따라다니는 리뷰 버튼(표식 사이를 다시 씀)
사진: 리포에 복사하지 않는다. 공식몰이 쓰는 스냅 서버(cdn.snapfit.co.kr)의 medium_ 이미지를 그대로 불러온다.
사용: python -X utf8 ops/cafe24/build_product_reviews.py
"""
import html, io, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREVIEW = ROOT / "storefront-v2/preview"
DATA = Path.home() / "Desktop/_탐뷰티/리뷰_전체수집_260921"
PRODUCTS = [18, 23, 24, 25, 101, 102, 109, 110, 111, 112, 114, 115, 118, 121]
SNAPSHOT = "2026.09.21"
ASSET_V = "7"
START = "<!-- customer-reviews:start (ops/cafe24/build_product_reviews.py) -->"
END = "<!-- customer-reviews:end -->"
ANCHOR = re.compile(r'<section\b[^>]*class="shop-section container"[^>]*>\s*<div class="section-heading">\s*<h2>Discover more', re.S)
NPAY_TAIL = re.compile(r"\(\s*\d{4}-\d{2}-\d{2}[-\s\d:]*에 등록된 네이버 페이 구매평\s*\)")


def clean(t):
    t = NPAY_TAIL.sub("", t or "").replace("\r", "")
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def medium(url):
    head, name = url.rsplit("/", 1)
    return head + "/medium_" + name


def section(no, title, n, avg):
    name = html.escape(title)
    return (START + "\n"
            f'      <section class="review-section container" id="review" aria-label="{name} 고객 리뷰" data-reviews>\n'
            '        <div class="section-heading">\n'
            "          <h2>Review</h2>\n"
            "        </div>\n"
            '        <div data-reviews-body></div>\n'
            "        <noscript><p>후기 목록은 자바스크립트를 켜야 보입니다.</p></noscript>\n"
            "      </section>\n"
            f'      <a class="review-jump" href="#review" data-review-jump hidden><span class="review-jump-score"><span class="rv-star" aria-hidden="true">★</span> {avg:.1f} · </span>리뷰 {n:,} <span data-arrow aria-hidden="true">↓</span></a>\n      '
            + END + "\n      ")


def main():
    data = json.loads((DATA / "reviews_all.json").read_text(encoding="utf-8"))
    out_dir = PREVIEW / "assets/reviews-data"
    out_dir.mkdir(parents=True, exist_ok=True)
    old = PREVIEW / "assets/reviews"
    if old.is_dir():
        shutil.rmtree(old)  # v2에서 복사해 뒀던 고객 사진은 더 이상 쓰지 않음
    report = []
    for no in PRODUCTS:
        reviews = [r for r in data["reviews"] if no in r["products"]]
        title = data["products"][str(no)]
        n = len(reviews)
        avg = sum(r["score"] for r in reviews) / n
        items = [{"i": r["id"], "s": r["score"], "t": clean(r["text"]), "u": (r["user"] or "").strip(), "d": r["date"],
                  "r": r.get("recommend") or 0, "p": [medium(p["url"]) for p in r["photos"] if p.get("url")]} for r in reviews]
        payload = {"product": no, "title": title, "asof": SNAPSHOT, "count": n, "avg": round(avg, 2),
                   "dist": {str(k): sum(1 for r in reviews if r["score"] == k) for k in (5, 4, 3, 2, 1)}, "items": items}
        js = "window.TAM_REVIEWS = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"
        (out_dir / f"p{no}.js").write_bytes(js.encode("utf-8"))

        path = PREVIEW / f"product-{no}.html"
        s = path.read_text(encoding="utf-8")
        if START in s:
            s = s[:s.index(START)] + s[s.index(END) + len(END):].lstrip()
        m = list(ANCHOR.finditer(s))
        assert m, f"{path.name}: Discover more 위치를 못 찾음"
        s = s[:m[-1].start()] + section(no, title, n, avg) + s[m[-1].start():]
        s = re.sub(r'\s*<link rel="stylesheet" href="assets/reviews\.css[^"]*" />', "", s)
        s = re.sub(r'\s*<script defer src="assets/reviews(?:-data/p\d+)?\.js[^"]*"></script>', "", s)
        links = list(re.finditer(r"<link\b[^>]*stylesheet[^>]*>", s))
        tags = ('\n    <link rel="stylesheet" href="assets/reviews.css?v=' + ASSET_V + '" />'
                f'\n    <script defer src="assets/reviews-data/p{no}.js?v={ASSET_V}"></script>'
                '\n    <script defer src="assets/reviews.js?v=' + ASSET_V + '"></script>')
        s = s[:links[-1].end()] + tags + s[links[-1].end():]
        page = s.encode("utf-8")
        path.write_bytes(page)
        photos = sum(1 for it in items if it["p"])
        report.append(f"{no:>4} {title[:22]:<22} 후기 {n:>4} | 포토 {photos:>3} | 평균 {avg:.2f} | 데이터 {len(js.encode('utf-8')) // 1024}KB")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
