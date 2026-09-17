"""Read-only public Cafe24 regression checks. Never submits cart/order/login forms."""
import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from playwright.async_api import async_playwright


async def check_page(context, base, route, kind):
    page = await context.new_page()
    result = {"route": route, "kind": kind, "checks": [], "page_error_count": 0}
    # Count errors without retaining third-party payloads or customer data.
    def page_error(_):
        result["page_error_count"] += 1
    page.on("pageerror", page_error)

    def check(name, passed):
        result["checks"].append({"name": name, "passed": bool(passed)})

    try:
        response = await page.goto(urljoin(base, route), wait_until="domcontentloaded", timeout=45000)
        await page.wait_for_timeout(2500)
        check("HTTP success", response is not None and response.ok)
        check("nonempty body", len(await page.locator("body").inner_text()) > 30)
        check("no horizontal overflow", await page.evaluate(
            "document.documentElement.scrollWidth <= innerWidth + 2"))
        result["broken_visible_images"] = await page.locator("img").evaluate_all("""es =>
            es.filter(e => {const r=e.getBoundingClientRect(); return e.complete &&
              !e.naturalWidth && r.width>0 && r.height>0 && r.top<innerHeight &&
              r.bottom>0 && getComputedStyle(e).visibility !== 'hidden';}).length""")
        check("visible images loaded", result["broken_visible_images"] == 0)
        if kind == "product":
            option = page.locator("#product_option_id1")
            check("native option selector exists", await option.count() == 1)
            check("native total area exists", await page.locator("#totalPrice").count() > 0)
            result["integrations"] = await page.evaluate("""() => ({
                snap: [...document.scripts].some(s => /snapfit|snapreview|sfre-srcs/.test(s.src)),
                naver: !!document.querySelector('#NaverChk_Button'),
                kakao: [...document.scripts].some(s => /kakao.*checkout|checkout.*kakao/.test(s.src))
            })""")
            if await option.count():
                values = await option.locator("option").evaluate_all(
                    "es=>es.filter(e=>!e.disabled && e.value && !['*','**'].includes(e.value)).map(e=>e.value)")
                result["selectable_options"] = len(values)
                check("at least one selectable option", len(values) > 0)
                if values:
                    if await option.is_visible():
                        await option.select_option(values[0], timeout=7000)
                    else:
                        # TAM cushion's custom list drives hidden native options.
                        # Other skins may expose Cafe24's standard radio labels.
                        custom = page.locator('.custom-opt__item').first
                        label = page.locator('ul[ec-dev-id="product_option_id1"] li[option_value] label').first
                        if await custom.is_visible():
                            await custom.click(timeout=7000)
                        else:
                            await label.click(timeout=7000)
                    try:
                        await page.wait_for_function("""() => {
                          const el=document.querySelector('#totalPrice');
                          return el && Number(el.innerText.replace(/[^0-9]/g,''))>0;
                        }""", timeout=7000)
                        check("option selection updates total", True)
                    except Exception:
                        check("option selection updates total", False)
        elif kind == "login":
            check("password field exists", await page.locator('input[type="password"]').count() > 0)
        result["status"] = "pass" if all(c["passed"] for c in result["checks"]) else "needs_review"
    except Exception as exc:
        result["status"] = "error"
        result["error_type"] = type(exc).__name__
    finally:
        await page.close()
    return result


async def run(args):
    base = args.base_url.rstrip("/") + "/"
    parsed = urlsplit(base)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("Use a HTTP(S) base URL without query or fragment; skin preview path prefixes are supported.")
    routes = [("", "home"), ("product/detail.html?product_no=23", "product"),
              ("product/detail.html?product_no=112", "product"),
              ("member/login.html", "login"), ("order/basket.html", "basket")]
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "base_url": base,
              "scope": "Unauthenticated structure and option selection only; no orders, cart additions, login, or coupon issuance.",
              "results": []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for width in (1440, 390):
            context = await browser.new_context(viewport={"width": width, "height": 900},
                                                is_mobile=width == 390, has_touch=width == 390)
            for route, kind in routes:
                result = await check_page(context, base, route, kind)
                result["viewport_width"] = width
                report["results"].append(result)
                print(f"{width} {kind} {route or '/'}: {result['status']}", flush=True)
            await context.close()
        await browser.close()
    report["passed"] = all(r["status"] == "pass" for r in report["results"])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Report: {output}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://tambeauty.kr/")
    parser.add_argument("--output", default="ops/cafe24/runs/public-smoke.json")
    raise SystemExit(asyncio.run(run(parser.parse_args())))
