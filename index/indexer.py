from handler import ContentHandler
from misc import log

import sys
from xml import sax as sx


@log
def main():
    path_to_wiki_dump = sys.argv[1]
    path_to_inverted_index = sys.argv[2]

    parser = sx.make_parser()
    content_handler = ContentHandler(path_to_inverted_index)
    parser.setContentHandler(content_handler)
    parser.parse(path_to_wiki_dump)

    print(content_handler.page_count)


if __name__ == "__main__":
    main()
