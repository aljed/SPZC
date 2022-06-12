import re
import randomizer as r


def tag_file(file):
    text = file.decode('latin-1')
    tag = r'(button|textarea|textbox|checkbox|input|select|option|optgroup|fieldset|label|datalist|form)'

    pattern = r'<' + tag + r' (.*) id="(.*?)"(.*)>'
    replacement = r'<\1 \2 id="_RaNmE_\3"\4>'
    text = re.sub(pattern, replacement, text)
    pattern = r'<' + tag + r'(.*) for="(.*?)"(.*)>'
    replacement = r'<\1 \2 for="_RaNmE_\3"\4>'
    text = re.sub(pattern, replacement, text)
    pattern = r'<' + tag + r'(.*) name="(.*?)"(.*)>'
    replacement = r'<\1 \2 name="_RaNmE_\3"\4>'
    text = re.sub(pattern, replacement, text)

    return text
