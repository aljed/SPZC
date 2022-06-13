import re
from string import Template


def tag_html(html: str) -> str:
    text = html
    vuln_tag = r'(button|textarea|textbox|checkbox|input|select|option|optgroup|fieldset|label|datalist|form)'
    pattern_temp = Template(r'<' + vuln_tag + r'(.*)$tag="(.*?)"(.*)>')
    replacement_temp = Template(r'<\1\2$tag="_RaNmE_\3"\4>')

    for tag in ['id', 'for', 'name']:
        sub = {'tag': tag}
        text = re.sub(
            pattern_temp.substitute(sub),
            replacement_temp.substitute(sub),
            text,
        )
    return text
