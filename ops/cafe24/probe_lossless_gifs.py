"""Measure lossless GIF optimization without changing delivery masters."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image


def frames(path):
    with Image.open(path) as image:
        metadata = {'size': image.size, 'loop': image.info.get('loop'),
                    'icc': hashlib.sha256(image.info.get('icc_profile', b'')).hexdigest()}
        timeline = []
        for frame in range(image.n_frames):
            image.seek(frame)
            rgba=hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()
            duration=image.info.get('duration',0)
            if timeline and timeline[-1]['rgba']==rgba:
                timeline[-1]['duration']+=duration
            else:
                timeline.append({'duration':duration,'rgba':rgba})
        return metadata, timeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gifsicle', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.output.resolve() != args.source.resolve()
    args.output.mkdir(parents=True, exist_ok=True)
    results = []
    for source in sorted(args.source.glob('*.gif')):
        target = args.output / source.name
        subprocess.run([str(args.gifsicle), '-O3', str(source), '-o', str(target)], check=True)
        identical = frames(source) == frames(target)
        row = {'file': source.name, 'before': source.stat().st_size,
               'after': target.stat().st_size, 'decoded_timeline_loop_icc_equal': identical,
               'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
        row['saving_percent'] = round((1-row['after']/row['before'])*100, 2)
        results.append(row)
        print(json.dumps(row), flush=True)
    (args.output/'lossless-report.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    assert all(row['decoded_timeline_loop_icc_equal'] for row in results)


if __name__ == '__main__':
    main()
