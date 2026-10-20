"""Bounded nonpersistent local Claude consultation; UTF-8 stdin avoids Windows quote truncation."""
from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cloud-blush-v7'
exe=Path.home()/'AppData/Roaming/npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe'
prompt='''Read only. Do not edit or invoke agents. Review this complete plan and actual rendered candidate. Previous attempt had Windows argument truncation; it was not a valid completed review. This prompt is supplied through stdin in full. Owner wants the already chosen Freshian section order and image roles, TAM colours and cream-to-powder USP. Do not invent claims or reorder the page. Cafe24 upload is deferred. Review up to 5 concrete issues: source-only first-revision cheeks, palette/face role, copy evidence, mobile readability, duplicate assets, Cafe24 package limits. Distinguish code review from physical colour validation and owner approval. You may only Read the following image files for visual review:
cloud-blush-v7/review-palette-430.png
cloud-blush-v7/review-faces-430.png
cloud-blush-v7/review-texture-430.png
cloud-blush-v7/review-vegan-430.png
cloud-blush-v7/review-delivery-390.jpg
Give a concise Korean verdict with material blockers and optional refinements. Do not demand fabricated proof. Full plan follows:\n'''+(OUT/'plan.json').read_text(encoding='utf-8')+'\nACTUAL QA:\n'+(OUT/'qa.json').read_text(encoding='utf-8')+'\nACTUAL COPY/STRUCTURE:\n'+(OUT/'detail.template.html').read_text(encoding='utf-8').split('<div data-tam-product-info')[0]
(OUT/'claude-review-input.txt').write_text(prompt,encoding='utf-8')
result=subprocess.run([str(exe),'-p','--no-session-persistence','--output-format','text','--tools','Read','--allowedTools','Read','--strict-mcp-config','--permission-mode','dontAsk'],input=prompt,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
(OUT/'claude-review.txt').write_text(result.stdout or result.stderr,encoding='utf-8')
print(result.stdout or result.stderr)
raise SystemExit(result.returncode)
