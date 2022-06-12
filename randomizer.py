import re
import base64
from urllib.parse import unquote
from Crypto.Util.Padding import pad, unpad
BLOCK_SIZE = 32


from Crypto.Cipher import AES

rtagged_id_pattern = re.compile(r'"_RaNmE_(.*?)"')
rtagged_data_pattern = re.compile(r'_RaNmE_(.*?)=([^=]*?)(&|$)')


def randomize(file: str, ck: bytes):
    cipher = AES.new(ck, AES.MODE_ECB)

    matched = set(rtagged_id_pattern.findall(file))
    encrypted_map = {m: cipher.encrypt(pad(m.encode(), BLOCK_SIZE)) for m in matched}

    def convert_case(match_obj):
        return '"_RaNmE_' + base64.b64encode(encrypted_map[match_obj.group(1)]).decode() + '"'

    text = rtagged_id_pattern.sub(convert_case, file)
    return text


def derandomize(content_data: bytes, ck: bytes):
    cipher = AES.new(ck, AES.MODE_ECB)

    matched = rtagged_data_pattern.findall(content_data.decode())
    decrypted_map = {m[0]: unpad(cipher.decrypt(base64.b64decode(unquote(m[0]).encode())), BLOCK_SIZE) for m in matched}

    def convert_case(match_obj):
        return '{decryped_id}={value}{opt}'.format(
            decryped_id=decrypted_map[match_obj.group(1)].decode(),
            value=match_obj.group(2),
            opt=match_obj.group(3),
        )

    text = rtagged_data_pattern.sub(convert_case, content_data.decode())
    return text.encode()
