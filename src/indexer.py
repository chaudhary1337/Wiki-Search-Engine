from index.handler import ContentHandler
from index.merger import Merge
from misc import log

import sys
from xml import sax as sx


@log
def main():
    # extracts the arguments provided
    path_to_wiki_dump = sys.argv[1]
    path_to_inverted_index = sys.argv[2]

    # creates a parser for the content
    parser = sx.make_parser()
    # creates a content handler object to handle all the
    # content from the xml file
    content_handler = ContentHandler(path_to_inverted_index)
    parser.setContentHandler(content_handler)

    # parsing the wiki data dump
    parser.parse(path_to_wiki_dump)

    # final message
    print(f"Completed indexing of {content_handler.page_count} pages.")

    # prints the required stats
    with open("invertedindex_stat.txt", "w") as f:
        f.write(
            str(content_handler.total_tokens)
            + "\n"
            + str(content_handler.total_tokens_inverted_index)
            + "\n"
        )

    # merge
    merge = Merge(path_to_inverted_index)
    merge.merge()


if __name__ == "__main__":
    main()
