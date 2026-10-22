"""Regression checks for Cafe24 layouts with an imported head."""
import unittest
from integrate_skin import patch_layout


class ImportedHeadTests(unittest.TestCase):
    def setUp(self):
        self.source = '''<!doctype html><html lang="ko">
<!--@import(/theme/layout/head.html)-->
<body id="main"><!--@import(/theme/popup.html)-->
<!--@import(/theme/layout/header.html)-->
<main><!--@contents--></main>
<!--@import(/theme/layout/footer.html)-->
<script src="/existing-app.js"></script></body></html>'''

    def test_imported_head_keeps_native_hooks(self):
        output, report = patch_layout(self.source)
        self.assertEqual(report['status'], 'candidate')
        for hook in ['<!--@import(/theme/layout/head.html)-->',
                     '<!--@import(/theme/popup.html)-->',
                     '<!--@contents-->',
                     '<script src="/existing-app.js"></script>']:
            self.assertIn(hook, output)
        self.assertIn('id="main" class="tam-native"', output)
        self.assertIn('<!--@import(/tam/partials/header.html)-->', output)
        self.assertIn('<!--@import(/tam/partials/footer.html)-->', output)
        self.assertEqual(output.count('TAM-INTEGRATION-V2'), 1)
        self.assertLess(output.index('TAM-INTEGRATION-V2'), output.index('<body'))
        self.assertEqual(patch_layout(output)[0], output)

    def test_ambiguous_head_is_unchanged(self):
        source = '<!--@import(/other/head.html)-->' + self.source
        output, report = patch_layout(source)
        self.assertEqual(report['status'], 'manual')
        self.assertEqual(output, source)

    def test_missing_head_is_unchanged(self):
        source = self.source.replace('<!--@import(/theme/layout/head.html)-->', '')
        output, report = patch_layout(source)
        self.assertEqual(report['status'], 'manual')
        self.assertEqual(output, source)

    def test_checkout_keeps_original_chrome(self):
        output, report = patch_layout(self.source, checkout=True)
        self.assertEqual(report['status'], 'candidate')
        self.assertIn('class="tam-checkout"', output)
        self.assertIn('<!--@import(/theme/layout/header.html)-->', output)
        self.assertIn('<!--@import(/theme/layout/footer.html)-->', output)
        self.assertNotIn('/tam/assets/chrome', output)

    def test_inline_head_still_works(self):
        source = self.source.replace('<!--@import(/theme/layout/head.html)-->',
                                    '<head><script src="/app.js"></script></head>')
        output, report = patch_layout(source)
        self.assertEqual(report['status'], 'candidate')
        self.assertIn('<script src="/app.js"></script>', output)
        self.assertLess(output.index('TAM-INTEGRATION-V2'), output.index('</head>'))


if __name__ == '__main__':
    unittest.main()
