"""Preserve the approved series distinction while connecting oil V9 to native25."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
preview=BeautifulSoup((ROOT/'storefront-v2/preview/product-25.html').read_text(encoding='utf-8'),'html.parser')
intro=preview.select_one('#product-detail > div')
intro.select_one('a')['href']='/skin-skin21/product/detail.html?product_no=18#prdDetail'
oil=(ROOT/'ops/cafe24/native-preparation-20261022/delivery/product-25.html').read_text(encoding='utf-8')
result='<div style="width:100%;max-width:860px;margin:auto">'+str(intro)+oil+'</div>\n'
(args.output/'product-25-series-v9.html').write_text(result,encoding='utf-8')
print('Series intro, native gloss18 link, seven approved oil panels; original SKUs untouched.')
