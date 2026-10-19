import unittest

from tools.add_public_seo import first_paragraph, shorten, upsert_meta


class AddPublicSeoTests(unittest.TestCase):
    def test_first_paragraph_strips_markup_and_overview_prefix(self):
        source = "<html><body><p><strong>Überblick.</strong> Das ist <em>sichtbar</em> und hilfreich.</p></body></html>"
        self.assertEqual(first_paragraph(source), "Das ist sichtbar und hilfreich.")

    def test_shorten_keeps_words_and_adds_ellipsis(self):
        text = "eins zwei drei vier fünf sechs"
        result = shorten(text, 15)
        self.assertEqual(result, "eins zwei drei…")

    def test_upsert_meta_is_idempotent(self):
        source = "<html><head><title>Titel</title></head><body></body></html>"
        once = upsert_meta(source, "robots", "index, follow")
        twice = upsert_meta(once, "robots", "index, follow")
        self.assertEqual(once, twice)
        self.assertEqual(once.count('name="robots"'), 1)


if __name__ == "__main__":
    unittest.main()
