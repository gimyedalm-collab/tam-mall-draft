"""Connect approved oil V9 without the owner-rejected series explanation.

Product25 and all four native options remain unchanged. This is display content,
not a product, inventory or order migration.
"""
from pathlib import Path
import argparse

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
oil=(ROOT/'ops/cafe24/native-preparation-20261022/delivery/product-25.html').read_text(encoding='utf-8')
result=oil
(args.output/'product-25-series-v9.html').write_text(result,encoding='utf-8')
print('Seven approved oil panels only; original product and all four native SKUs untouched.')
