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

    print(f"Completed indexing of {content_handler.page_count} pages.")

    with open("invertedindex_stat.txt", "w") as f:
        f.write(
            content_handler.total_tokens
            + "\n"
            + content_handler.total_tokens_inverted_index
            + "\n"
        )


if __name__ == "__main__":
    main()
