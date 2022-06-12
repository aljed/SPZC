import re
import base64

from Crypto.Cipher import AES

NONCE = b'aa'

rtagged_id_pattern = re.compile(r'"_RaNmE_(.*?)"')
rtagged_data_pattern = re.compile(r'_RaNmE_(.*?)=([^=]*?)(&|$)')


def randomize(file: str, ck: bytes, nonce=NONCE):
    cipher = AES.new(ck, AES.MODE_EAX, nonce=nonce)

    matched = set(rtagged_id_pattern.findall(file))
    encrypted_map = {m: cipher.encrypt(m.encode()) for m in matched}

    def convert_case(match_obj):
        return '_RaNmE_' + base64.b64encode(encrypted_map[match_obj.group(1)]).decode()

    text = rtagged_id_pattern.sub(convert_case, file)
    return text


def derandomize(content_data: bytes, ck: bytes, nonce=NONCE):
    cipher = AES.new(ck, AES.MODE_EAX, nonce=nonce)

    matched = rtagged_data_pattern.findall(content_data.decode())
    decrypted_map = {m[0]: cipher.decrypt(base64.b64decode(m[0].encode())) for m in matched}
    print(f'{decrypted_map=}')

    def convert_case(match_obj):
        return '{decryped_id}={value}{opt}'.format(
            decryped_id=decrypted_map[match_obj.group(1)].decode(),
            value=match_obj.group(2),
            opt=match_obj.group(3),
        )

    text = rtagged_data_pattern.sub(convert_case, content_data.decode())
    return text
