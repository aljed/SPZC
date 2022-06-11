import re
import randomizer as r

def tag_file(file):

    text = file
    tag = r'(button|textarea|textbox|checkbox|input|select|option|optgroup|fieldset|label|datalist)'

    pattern = r'<' + tag + r' (.*) id="(.*?)"(.*)>'
    replacement = r'<\1 \2 id="_RaNmE_\3"\4>'
    text = re.sub(pattern, replacement, text)
    pattern = r'<' + tag + r'(.*) for="(.*?)"(.*)>'
    replacement = r'<\1 \2 for="_RaNmE_\3"\4>'
    text = re.sub(pattern, replacement, text)

    return text


f = open('test.html', 'r', encoding='latin-1')
enc = tag_file(f.read())
g = open('output.html', 'w', encoding='latin-1')
u, nonce = r.randomize(enc, "1111222233334444")
g.write(r.derandomize(u, "243", nonce))