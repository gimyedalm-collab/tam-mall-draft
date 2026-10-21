"""Reproduce the frozen physical GIF edit with installed FFmpeg; no generation."""
from pathlib import Path
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'cloud-blush-v11'
m=json.loads((O/'motion-provenance.json').read_text(encoding='utf-8'))
args=['ffmpeg','-v','error','-y']
for item in m['sources']:
    src=Path(item['path']);src=src if src.is_absolute() else ROOT/src
    assert hashlib.sha256(src.read_bytes()).hexdigest()==item['sha256']
    args.extend(['-i',str(src)])
out=O/m['file']
args.extend(['-filter_complex',m['filter'],'-loop',str(m['loop_repeats']),str(out)])
subprocess.run(args,check=True)
assert out.stat().st_size<4_900_000
assert hashlib.sha256(out.read_bytes()).hexdigest()==m['sha256']
print('Frozen V11 motion edit reproduced exactly.')
