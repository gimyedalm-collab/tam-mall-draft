"""Verify current Cafe24 image deliveries without modifying their media."""
import hashlib
import json
import re
import zipfile
from pathlib import Path

from PIL import Image
from sync_storefront_details import PACKAGES, ROOT


def main():
    products = []
    for product, (folder, release) in PACKAGES.items():
        directory = ROOT / folder
        manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
        files = manifest.get('files') or manifest.get('media') or manifest['images']
        media = []
        for item in files:
            path = directory / item['file']
            data = path.read_bytes()
            with Image.open(path) as im:
                width, height = im.size
                fmt = im.format
            digest = hashlib.sha256(data).hexdigest()
            assert digest == item['sha256'], path
            assert fmt in ('JPEG', 'PNG', 'GIF'), path
            assert len(data) <= 10_000_000, path
            # Extra compatibility check for Edibot, not a universal FTP rule.
            assert height < 25600, path
            assert not (width >= 1600 and height >= 6400), path
            assert not (height >= 1600 and width >= 6400), path
            media.append(dict(file=item['file'], bytes=len(data), width=width,
                              height=height, format=fmt, sha256=digest))
        fragment = directory / ('cafe24-detail.html' if product == 109 else 'detail.cafe24.html')
        source = fragment.read_text(encoding='utf-8')
        assert not re.search(r'<(?:script|iframe|video)|@font-face', source, re.I), fragment
        image_urls = re.findall(r'<img\b[^>]*src="([^"]+)"', source)
        assert len(image_urls) == len(media), fragment
        assert all(url.startswith('/web/upload/') for url in image_urls), fragment
        archives = list(directory.glob('*.zip'))
        if product != 109:
            archives.append(directory.parent / (directory.name + '-cafe24.zip'))
        zip_checks = []
        for archive_path in archives:
            assert archive_path.is_file(), archive_path
            with zipfile.ZipFile(archive_path) as archive:
                assert archive.testzip() is None, archive_path
                names = archive.namelist()
                for item in media:
                    matches = [name for name in names if name == item['file'] or name.endswith('/' + item['file'])]
                    assert len(matches) == 1, (archive_path, item['file'])
                    assert hashlib.sha256(archive.read(matches[0])).hexdigest() == item['sha256']
            zip_checks.append(dict(file=archive_path.relative_to(ROOT).as_posix(), crc_and_media_hashes=True))
        products.append(dict(product_no=product, release=release, folder=folder, media=media,
                             upload_fragment=fragment.relative_to(ROOT).as_posix(),
                             upload_image_urls=image_urls, archives=zip_checks))
    report = dict(date='2026-10-21', products=products,
                  media_count=sum(len(p['media']) for p in products),
                  uploader_limits='Authenticated Cafe24 UI: <=10MB/file, <=100 files/batch, <=1000 files/folder',
                  extra_dimension_check='Edibot compatibility only',
                  actual_cafe24_upload_verified=False)
    output = ROOT / 'ops/cafe24/rollout-20261021/package-audit.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(products=len(products), media=report['media_count'], passed=True)))


if __name__ == '__main__':
    main()
