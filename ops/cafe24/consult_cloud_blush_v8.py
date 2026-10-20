from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'cloud-blush-v8';exe=Path.home()/'AppData/Roaming/npm/node_modules/@anthropic-ai/claude-code/bin/claude.exe'
prompt='''Read only. No edits, no other agents. Owner explicitly rejected V7 interpretation and now instructs closer Freshian DESIGN substitution, not just section order: big serif headings, hero product cutout composition, three-column texture cards, shallow 50/50 cheek rows, oval how-to title, muted TAM backgrounds. Do not invoke older one-grid or unchanged-hero requirements; this latest direction supersedes them. Provided first-revision cheeks, wrist assets and transparent texture assets stay unchanged except crop/resize. Physical shade accuracy unverified; Cafe24 upload deferred. Review the following reference/candidate images with Read:
cloud-blush-v8/review/ref-hero.jpg and cloud-blush-v8/review-hero-430.png
cloud-blush-v8/review/ref-faces.jpg and cloud-blush-v8/review-faces-430.png
cloud-blush-v8/review-palette-430.png
cloud-blush-v8/review-howto-430.png
cloud-blush-v8/review-formula-430.png
Judge design fidelity, mobile hierarchy, misleading crop/claims, and specific remaining issues. Give at most 4 practical issues in Korean. Distinguish owner approval from technical verification. Actual delivery is flattened JPG/GIF + native information, NOT the editable authoring HTML.
PLAN:\n'''+(O/'plan.json').read_text(encoding='utf-8')+'\nQA:\n'+(O/'qa.json').read_text(encoding='utf-8')
(O/'claude-review-input.txt').write_text(prompt,encoding='utf-8')
r=subprocess.run([str(exe),'-p','--no-session-persistence','--output-format','text','--tools','Read','--allowedTools','Read','--strict-mcp-config','--permission-mode','dontAsk'],input=prompt,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
(O/'claude-review.txt').write_text(r.stdout or r.stderr,encoding='utf-8');print(r.stdout or r.stderr)
