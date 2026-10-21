"""Bounded read-only, nonpersistent independent critique."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'cloud-blush-v12'
prompt='''Read-only Korean design/copy critique; do not edit or invoke other agents. Review only these local files: cloud-blush-v12/plan.json, detail.css, review-faces-430.png, review-hero-430.png, review-formula-430.png, review-vegan-430.png, review-texture-430.png, and cloud-blush-v11/review-faces-430.png, review-vegan-430.png.
Owner request: 살구 쉐이크 / 살구 베이지 naming is lazy; vegan section should have just a vegan mark without product image; many fonts are too large and inconsistent; oil image must return (previous feedback disliked oil/product composite, not oil itself).
V12 now: hero28 source px, all section titles24; six helpful two-line shade descriptions; original shade photos not recoloured; same V11 5.51sec real application GIF; old oil illustration restored alone; compact vegan botanical VEGAN FORMULA brand graphic, explicitly not third-party certification. No current certification evidence found for Cloud product, so no official certification logo or claim. Main canvas430, actual Cafe24 output scales to390/320; native INCI12px unchanged. Latest owner's smaller headings supersedes prior V10 larger hero instruction. No request to change overall section order or swatch geometry.
Check actual images, report only concrete relevant problems. Especially unsupported shade adjectives, readability, hierarchy, oil/vegan section balance. Separate must-fix from optional. Do not invent certification or mandatory approval. Under 600 Korean words. Note limits of actual screen vs image review.'''
(OUT/'claude-review-input.txt').write_text(prompt,encoding='utf-8')
exe=Path.home()/'AppData/Roaming/npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe'
p=subprocess.run([str(exe),'-p','--no-session-persistence','--output-format','text','--tools','Read','--allowedTools','Read','--strict-mcp-config','--permission-mode','dontAsk'],input=prompt,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
(OUT/'claude-review.txt').write_text(p.stdout,encoding='utf-8')
print(p.stdout);print('exit',p.returncode)
if p.returncode:print(p.stderr[-1500:])
