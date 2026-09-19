import unittest

from render_public_markdown import render_markdown


class EditorialRenderingTests(unittest.TestCase):
    def test_preserves_structured_content_without_literal_markdown(self):
        page = render_markdown("""### Hilfe zu `!rank`

Erster Absatz über
zwei Quellzeilen.

1. [Konto öffnen](https://example.org/account)
2. `!connect` benutzen

| Befehl | Bedeutung |
| --- | --- |
| `!rank` | Rang |

#### Grenzen

Keine Garantie.
""", title="Befehle")
        self.assertIn('<h2>Hilfe zu <code>!rank</code></h2>', page)
        self.assertRegex(page, r'<h3>\s*Grenzen</h3>')
        self.assertIn('<ol>', page)
        self.assertIn('<table>', page)
        self.assertIn('<a href="https://example.org/account">', page)
        self.assertIn('Erster Absatz über\nzwei Quellzeilen.</p>', page)
        self.assertNotIn('`', page)

    def test_duplicate_headings_have_distinct_stable_anchors(self):
        page = render_markdown('## Hilfe\n\nA\n\n## Hilfe\n\nB', title='Test')
        self.assertIn('id="hilfe"', page)
        self.assertIn('id="hilfe-2"', page)

    def test_source_markup_is_not_executable_and_date_is_not_audit(self):
        page = render_markdown('<script>alert(1)</script>', title='Test')
        self.assertNotIn('<script>', page)
        self.assertIn('fachlich ungeprüft', page)


if __name__ == '__main__':
    unittest.main()
