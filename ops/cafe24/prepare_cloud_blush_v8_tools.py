"""Create V8-specific exporters from established V7 contracts; V7 remains archived."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OPS=ROOT/'ops/cafe24'
s=(OPS/'export_cloud_blush_v7.py').read_text(encoding='utf-8').replace('V7','V8').replace('cloud-blush-v7','cloud-blush-v8')
s=s.replace('import hashlib, html, json, shutil, zipfile','import hashlib, html, json, shutil, zipfile, subprocess, math')
start=s.index('        if motion:');end=s.index('        else:',s.index('        elif n==1:',start))
s=s[:start]+'''        if motion:
            src=(SOURCE/loc.get_attribute('data-gif')).resolve();file=f'images/{n:02}-motion.gif'
            img=loc.locator('img');alt=img.get_attribute('alt');kind='gif'
            if 'inset' not in (loc.get_attribute('class') or ''):
                shutil.copy2(src,DEST/file)
            else:
                # Preserve the reference's side margins in the actual GIF canvas.
                rect=loc.bounding_box();ir=img.bounding_box();w=round(ir['width']*2);h=round(ir['height']*2)
                x=round((ir['x']-rect['x'])*2);y=round((ir['y']-rect['y'])*2);ch=math.ceil(rect['height']*2)
                filt=f'scale={w}:{h}:flags=lanczos,pad=860:{ch}:{x}:{y}:color=0xf1e8ee,drawbox=x={x}:y={y}:w={w}:h={h}:color=0x665760:t=2,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=sierra2_4a'
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-filter_complex',filt,'-loop','2',str(DEST/file)],check=True)
''' + s[end:]
s=s.replace('Two source GIFs each play 3 cycles and stop; no colour grading','Two source GIFs each play 3 cycles and stop; second GIF padded to reference inset; no creative colour grading')
(OPS/'export_cloud_blush_v8.py').write_text(s,encoding='utf-8')
s=(OPS/'verify_cloud_blush_v7.py').read_text(encoding='utf-8').replace('cloud-blush-v7','cloud-blush-v8')
s=s.replace("assert (D/'images/01-detail.jpg').read_bytes()==(OUT/'assets/hero-preserved.jpg').read_bytes()", "# Hero intentionally rebuilt from original product cutouts under the latest owner instruction.")
s=s.replace("p.locator('.wrist-grid figcaption,.face-row .tone,.note')", "p.locator('.wrist-grid figcaption,.face-row .tone,.face-row h3,.texture-grid p,.texture-grid small,.note')")
s=s.replace("[('#palette','palette'),('#faces','faces'),('#texture','texture'),('#vegan','vegan')]", "[('#hero','hero'),('#palette','palette'),('#faces','faces'),('#texture','texture'),('#howto','howto'),('#vegan','vegan'),('#formula','formula')]")
(OPS/'verify_cloud_blush_v8.py').write_text(s,encoding='utf-8')
s=(OPS/'promote_cloud_blush_v7.py').read_text(encoding='utf-8').replace('V7','V8').replace('cloud-blush-v7','cloud-blush-v8');(OPS/'promote_cloud_blush_v8.py').write_text(s,encoding='utf-8')
print('V8 scoped tools prepared.')
