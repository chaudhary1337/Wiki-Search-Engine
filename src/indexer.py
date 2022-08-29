"""
the primary file which handles the indexing part

1. indexing
2. merging
"""

import sys
from xml import sax as sx

from help import log
from index.merge import Merge
from index.handle import ContentHandler


@log()
def index():
    # creates a parser for the content
    parser = sx.make_parser()

    # creates a content handler object to handle all the
    # content from the xml file
    content_handler = ContentHandler(path_to_inverted_index)
    parser.setContentHandler(content_handler)
    parser.parse(path_to_wiki_dump)

    print(f"> Parsed total of {content_handler.page_count} pages.")
    print(f"> Saved pages a total of {content_handler.pages.save_counter} times.")
    return


@log()
def merge():
    merge = Merge(path_to_inverted_index)
    merge.merge()
    merge.clean_index()


if __name__ == "__main__":
    # extracts the arguments provided
    path_to_wiki_dump = sys.argv[1]
    path_to_inverted_index = sys.argv[2]

    index()
    merge()
