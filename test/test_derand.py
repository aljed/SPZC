import unittest

import randomizer as r
from tagger import tag_file


class Derand(unittest.TestCase):
    def test_derand(self):
        form_str = """
        <form action="./search.php" method="get" id="search">
        <fieldset>
            <input name="keywords" id="keywords" type="search" maxlength="128" title="Search for keywords" class="inputbox search tiny" size="20" value="" placeholder="Search…" />
            <button class="button button-search" type="submit" title="Search">
                <i class="icon fa-search fa-fw" aria-hidden="true"></i><span class="sr-only">Search</span>
            </button>
            <a href="./search.php" class="button button-search-end" title="Advanced search">
                <i class="icon fa-cog fa-fw" aria-hidden="true"></i><span class="sr-only">Advanced search</span>
            </a>
            
        </fieldset>
        </form>
        """
        ck = b"1111222233334444"
        tagged = tag_file(form_str)
        enc = r.randomize(tagged, ck)
        dec = r.derandomize(enc, ck)
        self.assertNotEqual(form_str, enc)
        self.assertEqual(form_str, dec)

    def test_no_id_critical_tag(self):
        no_id_html_str = """
        <form action="./search.php" method="get" id="search">
        <fieldset>
            <input name="keywords" type="search" maxlength="128" title="Search for keywords" class="inputbox search tiny" size="20" value="" placeholder="Search…" />
            <button class="button button-search" type="submit" title="Search">
                <i class="icon fa-search fa-fw" aria-hidden="true"></i><span class="sr-only">Search</span>
            </button>
            <a href="./search.php" class="button button-search-end" title="Advanced search">
                <i class="icon fa-cog fa-fw" aria-hidden="true"></i><span class="sr-only">Advanced search</span>
            </a>
            
        </fieldset>
        </form>
        """
        ck = b"1111222233334444"
        tagged = tag_file(no_id_html_str)
        self.assertEqual(no_id_html_str, tagged)
        enc = r.randomize(tagged, ck)
        self.assertEqual(no_id_html_str, enc)
        dec = r.derandomize(enc, ck)
        self.assertEqual(no_id_html_str, dec)


if __name__ == '__main__':
    unittest.main()
