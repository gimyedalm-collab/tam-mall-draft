"""Set a verified local V11 package as current delivery. No store writes."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[2];SOURCE=ROOT/'cloud-blush-v11';S=SOURCE/'cafe24';D=ROOT/'cafe24-delivery-20261019/cloud-blush'
qa=json.loads((SOURCE/'qa.json').read_text(encoding='utf-8'));assert qa['status']=='candidate_package_qa_pass'
m=json.loads((S/'manifest.json').read_text(encoding='utf-8'))
assert qa['bytes']==sum(i['bytes'] for i in m['files'])
for it in m['files']:assert hashlib.sha256((S/it['file']).read_bytes()).hexdigest()==it['sha256']
previous=json.loads((D/'manifest.json').read_text(encoding='utf-8'));active={i['file'] for i in m['files']}
for it in previous['files']:
    if it['file'] not in active:
        old=(D/it['file']).resolve();assert old.parent==(D/'images').resolve();old.unlink(missing_ok=True)
shutil.copytree(S,D,dirs_exist_ok=True)
shutil.copy2(SOURCE/'cloud-blush-cafe24.zip',D.parent/'cloud-blush-cafe24.zip')
print('Verified Cloud V11 package is now the local current delivery; Cafe24 upload remains deferred.')
