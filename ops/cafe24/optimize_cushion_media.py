"""Derive web video from original animation frames; originals remain untouched."""
from pathlib import Path
from PIL import Image
import subprocess,json,tempfile
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'storefront-v2/preview/assets'
OUT=ASSETS/'ux-261013';OUT.mkdir(exist_ok=True)
report=[]
for name in ['02','05','07']:
 source=ASSETS/f'jelly-skin-cushion-0908/{name}.webp'
 im=Image.open(source);durations=[]
 with tempfile.TemporaryDirectory(prefix='tam-cushion-') as folder:
  tmp=Path(folder);lines=['ffconcat version 1.0']
  for i in range(im.n_frames):
   im.seek(i);im.load();duration=im.info.get('duration',100);durations.append(duration)
   frame=tmp/f'{i:04d}.png';im.convert('RGB').save(frame)
   if i==0: im.convert('RGB').save(OUT/f'cushion-{name}-poster.jpg',quality=95)
   lines.extend([f"file '{frame.as_posix()}'",f'duration {duration/1000:.6f}'])
  lines.append(f"file '{frame.as_posix()}'")
  manifest=tmp/'frames.txt';manifest.write_text('\n'.join(lines))
  target=OUT/f'cushion-{name}.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-t',str(sum(durations)/1000),'-fps_mode','vfr','-an','-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],check=True)
  report.append({'source':str(source.relative_to(ROOT)),'output':str(target.relative_to(ROOT)),'source_frames':im.n_frames,'source_duration_seconds':sum(durations)/1000,'source_bytes':source.stat().st_size,'output_bytes':target.stat().st_size,'size':list(im.size)})
  print(name,report[-1],flush=True)
(ROOT/'ops/cafe24/ux-media-20261013.json').write_text(json.dumps(report,indent=2)+'\n')
