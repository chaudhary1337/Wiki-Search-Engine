from search.handle import Search

import sys

if __name__ == "__main__":
    path_to_inverted_index = sys.argv[1]
    in_file = open(sys.argv[2], "r")
    out_file = open("queries_op.txt", "w+")

    searcher = Search(path_to_inverted_index, in_file, out_file)
    searcher.search()
