from w3lib.html import remove_tags

def clean(tag):
    content = remove_tags(tag)
    return content.replace('\n', '').replace('\t', '').strip()
