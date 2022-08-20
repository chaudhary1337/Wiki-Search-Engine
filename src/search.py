from misc import log
from extract import Extract

import sys


@log
def main():
    path_to_inverted_index = sys.argv[1]
    query = sys.argv[2]

    extract = Extract()
    extracted_query = extract.extract(query)
    print("Hehe Boihhh")


if __name__ == "__main__":
    main()
