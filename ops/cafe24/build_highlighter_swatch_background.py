"""Clean only the original swatch backdrop; preserve source skin and pearl.

The still uses a native SVG clip over the byte-identical source JPEG. The film
uses a per-frame silhouette matte with an untouched, opaque foreground. No
colour, exposure, skin, pearl or speed filters are applied. Old assets remain.
"""
from pathlib import Path
import base64
import json
import shutil
import subprocess
import tempfile

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'highlighter-r33/assets'
BACKGROUND = '#faf8f6'


def ffmpeg_path():
    installed = shutil.which('ffmpeg')
    if installed:
        return installed
    return str(next((Path.home() / 'AppData/Local/Microsoft/WinGet/Packages').glob(
        'Gyan.FFmpeg_*/ffmpeg-*/bin/ffmpeg.exe')))


def silhouette(frame, palm=False):
    blue, green, red = cv2.split(frame.astype(np.int16))
    skin = (red > 110) & (red - blue > 19) & (red - green > 8)
    if palm:
        yy, xx = np.mgrid[:frame.shape[0], :frame.shape[1]]
        # Retain the deep skin fold at the thumb/wrist, not the tabletop shadow.
        skin |= ((xx < 320) & (yy > 300) & (yy < 750)
                 & (red - green > 25) & (red - blue > 40))
    mask = skin.astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    mask[:] = 0
    cv2.drawContours(mask, [contour], -1, 255, -1)
    return mask, contour


def main():
    ffmpeg = ffmpeg_path()
    def run(args):
        subprocess.run([ffmpeg, '-v', 'error', '-y', *args], check=True)

    source_photo = ASSETS / 'arm-three-pearls-261015.jpg'
    frame = cv2.imread(str(source_photo))
    _, contour = silhouette(frame)
    polygon = cv2.approxPolyDP(contour, 1.1, True).reshape(-1, 2)
    points = ' '.join(f'{x},{y}' for x, y in polygon)
    encoded_original = base64.b64encode(source_photo.read_bytes()).decode()
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1250" '
        'viewBox="0 0 1000 1250"><defs><clipPath id="arm">'
        f'<polygon points="{points}"/></clipPath></defs>'
        f'<path fill="{BACKGROUND}" d="M0 0h1000v1250H0z"/>'
        '<image width="1000" height="1250" clip-path="url(#arm)" '
        f'href="data:image/jpeg;base64,{encoded_original}"/></svg>\n'
    )
    (ASSETS / 'arm-three-pearls-clean-261015.svg').write_text(svg, encoding='utf-8')
    assert base64.b64decode(encoded_original) == source_photo.read_bytes()

    source_video = ASSETS / 'palm-pearl-result-261015.mp4'
    target_video = ASSETS / 'palm-pearl-clean-261015.mp4'
    capture = cv2.VideoCapture(str(source_video))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)
    assert (width, height, fps) == (720, 900, 24)
    count = 0
    with tempfile.TemporaryDirectory(prefix='tam-swatch-matte-') as tmp:
        matte = Path(tmp) / 'matte.mkv'
        encoder = subprocess.Popen([
            ffmpeg, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray',
            '-s', '720x900', '-r', '24', '-i', 'pipe:0', '-c:v', 'ffv1', str(matte)
        ], stdin=subprocess.PIPE)
        try:
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                mask, _ = silhouette(frame, palm=True)
                mask = cv2.GaussianBlur(mask, (7, 7), 1.2)
                # This common region stays inside the moving hand in all 79 frames.
                assert np.all(mask[320:620, 300:540] == 255), 'Pearl region must stay opaque'
                encoder.stdin.write(mask.tobytes())
                count += 1
        finally:
            capture.release()
            encoder.stdin.close()
            encoder.wait()
        assert encoder.returncode == 0
        run([
            '-i', str(source_video), '-i', str(matte), '-f', 'lavfi', '-i',
            'color=c=0xfaf8f6:s=720x900:r=24', '-filter_complex',
            '[0:v][1:v]alphamerge[fg];[2:v][fg]overlay=shortest=1:format=rgb,'
            'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]',
            '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
            '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
            '-movflags', '+faststart', str(target_video)
        ])
    run(['-ss', '1.65', '-i', str(target_video), '-frames:v', '1', '-q:v', '2',
         str(ASSETS / 'palm-pearl-clean-poster-261015.jpg')])
    # Only compression rounding may differ within the protected source region.
    before = cv2.VideoCapture(str(source_video))
    after = cv2.VideoCapture(str(target_video))
    errors = []
    while True:
        ok, a = before.read()
        other_ok, b = after.read()
        assert ok == other_ok, 'Frame count changed'
        if not ok:
            break
        a = a[320:620, 300:540].astype(np.float32)
        b = b[320:620, 300:540].astype(np.float32)
        errors.append(float(np.abs(a - b).mean()))
    before.release()
    after.release()
    assert max(errors) < 3, errors
    print(json.dumps({'frames': count, 'embedded_photo_bytes_identical': True,
                      'pearl_roi_encoding_mae_mean': float(np.mean(errors)),
                      'pearl_roi_encoding_mae_max': max(errors)}, indent=2))


if __name__ == '__main__':
    main()
