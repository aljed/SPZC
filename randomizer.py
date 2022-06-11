import re
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

client_key = get_random_bytes(16)

def randomize(file, ck):

    cipher = AES.new(client_key, AES.MODE_EAX)
    nonce = cipher.nonce

    def convert_case(match_obj):
        return r'"_RaNmE_' + encrypted_map[match_obj.group(1)].decode('latin-1') + '"'

    pattern = r'"_RaNmE_(.*?)"'
    all = set(re.findall(pattern, file))
    encrypted_map = {word: cipher.encrypt(word.encode('latin-1')) for word in all}
    cipher = AES.new(client_key, AES.MODE_EAX, nonce=nonce)

    decrypted = {word: cipher.decrypt(word) for word in encrypted_map.values()}

    text = re.sub(pattern, convert_case, file)
    return text, nonce


def derandomize(file, ck, nonce):
    cipher = AES.new(client_key, AES.MODE_EAX, nonce=nonce)

    def convert_case(match_obj):
        return r'"' + encrypted_map[match_obj.group(1)].decode('latin-1') + '"'

    pattern = r'"_RaNmE_(.*?)"'
    all = re.findall(pattern, file)
    encrypted_map = {word: cipher.decrypt(word.encode('latin-1')) for word in all}

    text = re.sub(pattern, convert_case, file)
    return text