"""Compare public Cafe24 media with preserved local originals, including pixels.

The platform can losslessly rewrite PNG bytes. A byte mismatch is therefore
checked against every decoded frame, frame duration, loop count and ICC profile.
Never use this tool for authenticated administrator exports.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import urllib.request

from PIL import Image, ImageSequence


def visual_signature(data):
    with Image.open(io.BytesIO(data)) as im:
        info = {'size': im.size,
                'icc_sha256': hashlib.sha256(im.info.get('icc_profile', b'')).hexdigest(),
                'loop': im.info.get('loop'), 'frames': []}
        for frame in ImageSequence.Iterator(im):
            info['frames'].append({
                'duration': frame.info.get('duration'),
                'rgba_sha256': hashlib.sha256(frame.convert('RGBA').tobytes()).hexdigest()})
        return info


def verify(item, source_root):
    result = {k: item[k] for k in ('product_no', 'source', 'file', 'url')}
    try:
        original = (source_root / item['source']).read_bytes()
        original_hash = hashlib.sha256(original).hexdigest()
        if original_hash != item['sha256']:
            raise ValueError('Original differs from approved manifest')
        request = urllib.request.Request(item['url'], headers={'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=45) as response:
            remote = response.read()
            result.update(http_status=response.status, content_type=response.headers.get('Content-Type'))
        remote_hash = hashlib.sha256(remote).hexdigest()
        byte_match = original_hash == remote_hash
        result.update(original_bytes=len(original), remote_bytes=len(remote),
                      original_sha256=original_hash, remote_sha256=remote_hash,
                      byte_match=byte_match)
        result['visual_match'] = byte_match or visual_signature(original) == visual_signature(remote)
        result['pass'] = result['http_status'] == 200 and result['visual_match']
    except Exception as error:
        result.update(pass_=False, error=str(error))
        result['pass'] = False
        result.pop('pass_', None)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    media = json.loads(args.manifest.read_text(encoding='utf-8'))['media']
    with ThreadPoolExecutor(max_workers=4) as pool:
        checks = list(pool.map(lambda item: verify(item, args.source_root), media))
    result = {'total': len(checks), 'passed': sum(x['pass'] for x in checks),
              'byte_matches': sum(x.get('byte_match', False) for x in checks),
              'checks': checks}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}))
    for item in checks:
        if not item['pass']:
            print(json.dumps(item, ensure_ascii=False))
    raise SystemExit(0 if result['passed'] == result['total'] else 1)


if __name__ == '__main__':
    main()
