import unittest

from tagger import tag_html


class TestTagger(unittest.TestCase):
    def test_tag_html(self):
        test_html = '<form id="username">'
        res = tag_html(test_html)
        self.assertEqual(res, '<form id="_RaNmE_username">')

        test_html = '<button name="username">'
        res = tag_html(test_html)
        self.assertEqual(res, '<button name="_RaNmE_username">')

        test_html = '<input for="username">'
        res = tag_html(test_html)
        self.assertEqual(res, '<input for="_RaNmE_username">')


if __name__ == '__main__':
    unittest.main()
