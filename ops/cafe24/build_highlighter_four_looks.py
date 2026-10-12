"""Compose four supplied actual-use clips without retouch or colour grading."""
from pathlib import Path
import json, subprocess
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = next((Path.home() / 'Desktop').glob('*/*WOW_R32_261002'))
SOURCES = json.loads((SOURCE_DIR / 'source-map.json').read_text(encoding='utf-8'))
FFMPEG = next((Path.home() / 'AppData/Local/Microsoft/WinGet/Packages').glob('Gyan.FFmpeg_*/**/ffmpeg.exe'))
TEMP = ROOT / 'ops/cafe24/runs/highlighter-four-looks'
TEMP.mkdir(parents=True, exist_ok=True)
ASSETS = ROOT / 'highlighter-r32/assets'
clips = [
    {'index': 1, 'start': 12.0, 'crop': [0, 150, 1080, 1320]},
    {'index': 2, 'start': 152.0, 'crop': [0, 40, 1080, 1320]},
    {'index': 4, 'start': 21.3, 'crop': [0, 0, 1080, 1320]},
    {'index': 6, 'start': 24.0, 'crop': [0, 0, 1080, 1320]},
]

def run(args):
    subprocess.run([str(FFMPEG), '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

def prepare(item):
    x, y, w, h = item['crop']
    target = TEMP / f"clip-{item['index']}.mp4"
    run(['-ss', str(item['start']), '-i', SOURCES[item['index']], '-t', '2.8',
         '-vf', f'crop={w}:{h}:{x}:{y},scale=366:448:flags=lanczos,fps=24,setsar=1',
         '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', str(target)])
    return target

with ThreadPoolExecutor(max_workers=4) as pool:
    inputs = list(pool.map(prepare, clips))
video = ASSETS / 'howto-four-looks-261012.mp4'
poster = ASSETS / 'howto-four-looks-poster-261012.jpg'
args = []
for source in inputs:
    args += ['-i', str(source)]
run([*args, '-filter_complex', '[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|382_0|0_464|382_464:fill=white[v]',
     '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium',
     '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)])
run(['-ss', '0.8', '-i', str(video), '-frames:v', '1', '-q:v', '2', str(poster)])
evidence = {
    'source_kind': 'User-supplied highlighter clean/seeding videos',
    'clips': [{**item, 'source_filename': Path(SOURCES[item['index']]).name} for item in clips],
    'duration_requested_seconds': 2.8,
    'layout': '2x2, four distinct source people; 366x448 tiles with 16px white gaps',
    'output': str(video.relative_to(ROOT)).replace('\\', '/'),
    'processing': 'Trim, crop, proportional resize, grid composition and compression. No colour adjustment, retouch, AI generation, speed change or audio.',
    'claims': 'Actual-use montage; no purchase, review, popularity, satisfaction or efficacy statistics implied.',
    'production_cafe24_changed': False,
}
(ROOT / 'ops/cafe24/highlighter-four-looks-20261012.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
print(video.name, video.stat().st_size, 'bytes')
