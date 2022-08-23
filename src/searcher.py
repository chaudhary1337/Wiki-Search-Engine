from search.handle import Search

import sys

if __name__ == "__main__":
    path_to_inverted_index = sys.argv[1]
    query = sys.argv[2]

    searcher = Search(path_to_inverted_index)
    searcher.search(query)
