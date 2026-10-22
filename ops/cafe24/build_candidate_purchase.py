"""Patch private captured native sources; publish only our overrides and builder."""
from pathlib import Path
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--original',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
def write(path,text):
    dest=args.output/'templates'/path
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(text,encoding='utf-8')
detail=(args.original/'detail-template.html').read_text(encoding='utf-8')
marker='<script defer src="https://awiz.cafe24.com/tam-detail-20261022/candidate-detail-261022-v2.js"></script>'
assert detail.count(marker)==1 and 'candidate-purchase-' not in detail
detail=detail.replace(marker,marker+'\n<link rel="stylesheet" href="https://awiz.cafe24.com/tam-detail-20261022/candidate-purchase-261022-v4.css">\n<script defer src="https://awiz.cafe24.com/tam-detail-20261022/candidate-purchase-261022-v3.js"></script>')
write('moa/import/product_detail/detail.html',detail)
common=(args.original/'common.js').read_text(encoding='utf-8')
marker='function scrollHeaderFixed() {'
assert common.count(marker)==1
guard="\n    // New candidate navigation has no legacy header-bottom element.\n    if (!$('.header__bottom').length) return;"
write('moa/js/common.js',common.replace(marker,marker+guard))
pdp=(args.original/'detail.js').read_text(encoding='utf-8')
assert pdp.count("$('.header__bottom').outerHeight()")>=2
pdp=pdp.replace("$('.header__bottom').outerHeight()","($('.tam-nav-header').outerHeight() || $('.header__bottom').outerHeight() || 0)")
write('moa/js/product/detail.js',pdp)
print('Prepared3native patches; commerce and media nodes retained.')
