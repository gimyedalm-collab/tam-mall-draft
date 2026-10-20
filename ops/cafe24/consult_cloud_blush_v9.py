from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'cloud-blush-v9'
exe=Path.home()/'AppData/Roaming/npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe'
prompt='''Read only; do not edit or delegate. Owner now explicitly says to REMOVE excessive fonts/ornament from V8, preserving reference section order, original photos and layout. V9 switches large Bodoni/italic headings to TAM Korean Pretendard and small Manrope labels, removes halos, chips, oval, duplicate English colour names and duplicate formula copy. Do not recommend adding reference ornament back. Check actual rendered images:
cloud-blush-v9/review-hero-430.png
cloud-blush-v9/review-palette-430.png
cloud-blush-v9/review-faces-430.png
cloud-blush-v9/review-howto-430.png
cloud-blush-v9/review-formula-430.png
Assess ONLY clipping, mobile hierarchy, excess duplication, or any claim changed by this revision. State maximum 3 actionable issues, in Korean; distinguish blocker from optional. Existing photos and colour unchanged and physically unverified; do not demand colour correction. Cafe24 upload is explicitly deferred. Package is flat JPG/GIF plus native12px INCI. Supporting text effective >=12px at320 verified. Owner acceptance pending.'''
(O/'claude-review-input.txt').write_text(prompt,encoding='utf-8')
r=subprocess.run([str(exe),'-p','--no-session-persistence','--output-format','text','--tools','Read','--allowedTools','Read','--strict-mcp-config','--permission-mode','dontAsk'],input=prompt,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
(O/'claude-review.txt').write_text(r.stdout or r.stderr,encoding='utf-8')
print(r.stdout or r.stderr)
