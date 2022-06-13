import re
import base64
from urllib.parse import unquote

from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 32

rtagged_id_pattern = re.compile(r'"_RaNmE_(.*?)"')
rtagged_content_data_pattern = re.compile(r'_RaNmE_(.*?)=([^=]*?)(&|$)')


def _encrypt(cipher, input: bytes) -> bytes:
    return cipher.encrypt(pad(input, BLOCK_SIZE))


def _decrypt(cipher, input: bytes) -> bytes:
    return unpad(cipher.decrypt(input), BLOCK_SIZE)


def _decode_content_data(id: str) -> bytes:
    return base64.b64decode(unquote(id).encode())


def randomize(html: str, ck: bytes) -> str:
    cipher = AES.new(ck, AES.MODE_ECB)

    matched = set(rtagged_id_pattern.findall(html))
    encrypted_map = {m: _encrypt(cipher, m.encode()) for m in matched}

    def convert_case(match_obj):
        return '"_RaNmE_' + base64.b64encode(encrypted_map[match_obj.group(1)]).decode() + '"'

    return rtagged_id_pattern.sub(convert_case, html)


def derandomize(content_data: bytes, ck: bytes) -> bytes:
    cipher = AES.new(ck, AES.MODE_ECB)

    matched = rtagged_content_data_pattern.findall(content_data.decode())
    matched_ids = list(map(lambda x: x[0], matched))
    decrypted_map = {m: _decrypt(cipher, _decode_content_data(m)) for m in matched_ids}

    def convert_case(match_obj):
        return '{decryped_id}={value}{opt}'.format(
            decryped_id=decrypted_map[match_obj.group(1)].decode(),
            value=match_obj.group(2),
            opt=match_obj.group(3),
        )

    text = rtagged_content_data_pattern.sub(convert_case, content_data.decode())
    return text.encode()
