"""Rebuild only the palm clip from original footage with a stable, soft matte.

Never run the older background builder to regenerate the current arm image.
The three original time ranges, crop, skin/pearl colour and page geometry stay.
"""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np

from build_highlighter_swatch_background import ASSETS, ffmpeg_path, silhouette

SEGMENTS = [(8.35, 1.3), (11.95, .8), (14.5, 1.2)]
WIDTH, HEIGHT, FPS = 720, 900, 30


def geometry(frame):
    mask, _ = silhouette(frame, palm=True)
    # Regularize colour-threshold stair steps before feathering, not the image.
    field = cv2.GaussianBlur(mask, (0, 0), 5)
    return (field > 145).astype(np.float32)


def align_mask(reference, neighbor, neighbor_mask):
    small = lambda f: cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (360, 450))
    flow = cv2.calcOpticalFlowFarneback(
        small(reference), small(neighbor), None, .5, 3, 25, 3, 5, 1.2, 0)
    flow = cv2.resize(flow, (WIDTH, HEIGHT)) * 2
    y, x = np.mgrid[:HEIGHT, :WIDTH].astype(np.float32)
    return cv2.remap(neighbor_mask, x + flow[:, :, 0], y + flow[:, :, 1],
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--review-dir', type=Path, required=True)
    args = parser.parse_args()
    args.review_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg = ffmpeg_path()
    target = ASSETS / 'palm-pearl-smooth-261015.mp4'
    encoder = subprocess.Popen([
        ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', f'{WIDTH}x{HEIGHT}', '-r', str(FPS), '-i', 'pipe:0', '-an',
        '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
        '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
        '-movflags', '+faststart', str(target)], stdin=subprocess.PIPE)
    counts = []
    protected_errors = []
    try:
        for segment, (start, duration) in enumerate(SEGMENTS):
            raw = subprocess.check_output([
                ffmpeg, '-v', 'error', '-ss', str(start), '-i', str(args.source),
                '-t', str(duration), '-vf', 'crop=1080:1350:0:280,scale=720:900:flags=lanczos,fps=30',
                '-f', 'rawvideo', '-pix_fmt', 'bgr24', 'pipe:1'])
            frames = np.frombuffer(raw, np.uint8).reshape(-1, HEIGHT, WIDTH, 3)
            masks = [geometry(f) for f in frames]
            counts.append(len(frames))
            # Track only within each shot; never average different shades/cuts.
            for i, frame in enumerate(frames):
                total = masks[i] * 2
                weight = 2
                for j in (i - 1, i + 1):
                    if 0 <= j < len(frames):
                        total = total + align_mask(frame, frames[j], masks[j])
                        weight += 1
                alpha = cv2.GaussianBlur((total / weight > .5).astype(np.float32), (0, 0), 2)
                assert np.all(alpha[320:620, 300:540] > .99999)
                output = np.rint(frame * alpha[:, :, None] +
                                 np.array([246, 248, 250]) * (1 - alpha[:, :, None])).astype(np.uint8)
                protected_errors.append(int(np.abs(output[320:620, 300:540].astype(int) -
                                                    frame[320:620, 300:540].astype(int)).max()))
                encoder.stdin.write(output.tobytes())
                if i in (0, len(frames)//2, len(frames)-1):
                    cv2.imwrite(str(args.review_dir / f'segment-{segment}-frame-{i}.jpg'), output)
            print(f'Segment {segment + 1}: {len(frames)} frames', flush=True)
    finally:
        encoder.stdin.close()
        encoder.wait()
    assert encoder.returncode == 0
    assert max(protected_errors) == 0
    subprocess.run([ffmpeg, '-v', 'error', '-y', '-ss', '1.65', '-i', str(target),
                    '-frames:v', '1', '-q:v', '2',
                    str(ASSETS / 'palm-pearl-smooth-poster-261015.jpg')], check=True)
    report = dict(segments=SEGMENTS, segment_frames=counts, fps=FPS,
                  frames=sum(counts), dimensions=[WIDTH, HEIGHT],
                  protected_roi_max_error_before_encoding=max(protected_errors),
                  processing='Original source; one final encode. Spatial matte regularization, motion-aligned adjacent matte smoothing within each cut, 2px feather. No foreground colour/exposure filter.')
    (args.review_dir / 'render.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
