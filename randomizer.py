import re
from Crypto.Cipher import AES

NONCE = b'aa'


def randomize(file, ck, nonce=NONCE):
    cipher = AES.new(ck, AES.MODE_EAX, nonce=nonce)

    def convert_case(match_obj):
        return r'"_RaNmE_' + encrypted_map[match_obj.group(1)].decode('latin-1') + '"'

    pattern = r'"_RaNmE_(.*?)"'
    all = set(re.findall(pattern, file))
    encrypted_map = {word: cipher.encrypt(word.encode('latin-1')) for word in all}

    text = re.sub(pattern, convert_case, file)
    return text


def derandomize(file, ck, nonce=NONCE):
    cipher = AES.new(ck, AES.MODE_EAX, nonce=nonce)

    def convert_case(match_obj):
        return encrypted_map[match_obj.group(1)].decode('latin-1') + match_obj.group(2) + match_obj.group(3)

    pattern = r'_RaNmE_(.*?)=(.*?)(&|$)'
    all = re.findall(pattern, file)
    encrypted_map = {word[0]: cipher.decrypt(word[0].encode('latin-1')) for word in all}

    text = re.sub(pattern, convert_case, file)
    return text.encode('latin-1')
