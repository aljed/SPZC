import unittest
import base64

from Crypto.Cipher import AES

import randomizer as r


class TestRandomizer(unittest.TestCase):
    ck = b'-495877618964777'

    def test_randomize(self):
        test_html = '<button id="_RaNmE_username">'
        encrypted_id = r._encrypt(AES.new(self.ck, AES.MODE_ECB), b'username')
        b64enc = base64.b64encode(encrypted_id).decode()
        expected = f'<button id="_RaNmE_{b64enc}">'
        print(expected)
        self.assertEqual(r.randomize(test_html, self.ck), expected)

    def test_derandomize(self):
        content_data = b'_RaNmE_rZygNXKblBAxDIyPEurLbVuBw4A0DjruZmtzRQACJpI%3D=1'
        self.assertEqual(r.derandomize(content_data, self.ck), b'username=1')


if __name__ == '__main__':
    unittest.main()
