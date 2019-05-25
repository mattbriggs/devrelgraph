import re

def get_text_from_file(path):
    '''Return text from a text filename path'''
    textout = ""
    fh = open(path, "r")
    for line in fh:
        textout += line
    fh.close()
    return textout

def get_links_regex(inpath, bodytext):
    '''With the body as a string, extract via RegEx the altltext, link, and linktype'''

    link_types = {"http" : "hyperlink", "media/" : "meda", ".md" : "internal"}
    doc_links = [["doc", "alttext", "link", "type"]]
    match = re.findall("\[.*?\]\(.*?\)", bodytext)
    for m in match:
        parts = m.split("](")
        alttext = parts[0][1:]
        link = parts[1][:-1]
        link_type = ""
        for key, value in link_types.items():
            if re.match(key, link):
                link_type = value
        doc_links.append([inpath, alttext, link, link_type])
    return doc_links


def main():
    '''Main parsing'''
    path = r"" # add path to file

    body_raw = get_text_from_file(path)
    body_links = get_links_regex(path, body_raw)
    print(body_links)


if __name__ == "__main__":
    main()