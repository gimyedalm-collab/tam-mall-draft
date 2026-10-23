"""Patch only review section/image attributes; native templates stay private."""
import argparse
import re
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
BASE='https://awiz.cafe24.com/tam-detail-20261022/'


def build(source,output):
    assert not output.resolve().is_relative_to(ROOT)
    text=source.read_text(encoding='utf-8')
    without_review=re.sub(r'<section\b[^>]*class="tam-home-reviews"[\s\S]*?</section>','',text)
    count=0
    def patch(match):
        nonlocal count
        raw=match[0]
        if 'srcset=' not in raw or 'perf261023-' not in raw:return raw
        tag=BeautifulSoup(raw,'html.parser').img
        filename=tag['src'].split('/')[-1]
        original=re.sub(r'-\d+(?=\.[^.]+$)','',filename.replace('perf261023-',''))
        with Image.open(ROOT/'storefront-v2/preview/assets'/original) as im:width=im.width
        entries=tag['srcset'].split(', ')
        if original.startswith('lookbook-'):
            entries.append(BASE+'inner-'+Path(original).stem+'-1600.jpg 1600w')
            sizes='(max-width:760px) 50vw, (max-width:1500px) 48vw, 760px'
        elif original in ('retouched-111-v1.png','retouched-112-v1.png'):
            sizes='(max-width:760px) 90vw, (max-width:1023px) 48vw, 640px'
        else:
            sizes='(max-width:760px) 52vw, 340px'
        entries.append(BASE+'home-'+original+f' {width}w')
        raw=re.sub(r'srcset="[^"]*"','srcset="'+', '.join(entries)+'"',raw)
        raw=re.sub(r'sizes="[^"]*"','sizes="'+sizes+'"',raw)
        count+=1
        return raw
    result=re.sub(r'<img\b[^>]*>',patch,without_review)
    assert count==6,count
    strip=lambda s:re.sub(r'<img\b[^>]*>','<img>',s)
    assert strip(result)==strip(without_review)
    assert 'tam-home-reviews' not in result
    output.write_text(result,encoding='utf-8')
    print('Removed homepage review section and corrected six responsive image selections; other source unchanged.')


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--source',type=Path,required=True)
    a.add_argument('--output',type=Path,required=True)
    v=a.parse_args();build(v.source,v.output)
