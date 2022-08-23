from collections import Counter, defaultdict
from os.path import exists
from math import log

from search.extract import Extract
from help import (
    BONUS,
    DUMP_LIMIT,
    FIELD_WEIGHTS,
    BONUS_DEFAULT,
    RFIELDS,
    FIELDS,
    TOTAL,
    dec,
)


class Search:
    def __init__(self, path_to_inverted_index):
        self.extract = Extract()
        self.path_to_inverted_index = path_to_inverted_index

    def get_token_pages(self, token):
        """
        does a linear search on the appropriate merged file
        using the mini_token (first 3 characters)

        returns a list of page info of the form
        ["page_id:tf1fid1tf2fid2", "page_id2:tffid"]
        which has been split by a ;
        """
        data = ""

        mini_token = token[:3]
        path = f"{self.path_to_inverted_index}/merged_{mini_token}.txt"

        if not exists(path):
            return []

        with open(path, "r") as f:
            while line := f.readline():
                if line[: len(token)] != token:
                    continue
                token, data = line.split()
                break

        return data.split(";")

    def get_tf(self, field_data, i):
        """
        returns the final index i
        and the decoded buffer, which is the tf

        NOTE: here we use RFIELDS since we want to look at the actual data
        (the dump format)
        """
        buffer = []
        while i < len(field_data) and field_data[i] not in RFIELDS:
            buffer.append(field_data[i])
            i += 1
        return i, dec("".join(buffer))

    def get_bonus(self, field_data, i, field):
        """
        NOTE: here we use FIELDS since we want to look at human readable format

        """
        if field == "":
            return BONUS_DEFAULT

        matching = field_data[i] == FIELDS[field]
        return BONUS_DEFAULT if not matching else BONUS

    def search_token(self, token, field):
        pages = self.get_token_pages(token)

        # idf is the number of pages this token appears in
        idf = len(pages)
        # if the number of pages is 0, then this token is not
        # in the data dump
        if idf == 0:
            return {}

        field_matches = defaultdict(int)
        for page in pages:
            if not page:
                continue

            page_id, field_data = page.split(":")

            i = -1
            while (i := i + 1) < len(field_data):
                # reads the characters while a field is not seen
                i, tf = self.get_tf(field_data, i)

                # gets the appropriate bonus for a field
                # if matching, we give BONUS, else BONUS_DEFAULT
                bonus = self.get_bonus(field_data, i, field)

                # calculates the current score of the token
                # in the specified field
                score = log(1 + tf) * log(TOTAL / idf) * bonus * FIELD_WEIGHTS[field]

                # for this page_id, increase its ranking by score
                # NOTE: THIS REMAINS THE ONLY MAJOR BUG/ISSUE IN MY CODE
                field_matches[dec(page_id) - 1] += score

        return field_matches

    def search(self, query, k=10):
        query_counter = Counter()

        extracted_query = self.extract.extract(query)
        print(extracted_query)

        # has one more key, the "" other than FIELDS
        for field in extracted_query.keys():
            for token in extracted_query[field]:
                query_counter += self.search_token(token, field)

        topk = query_counter.most_common(k)

        for page_id, score in topk:
            save_counter, line_number = divmod(page_id, DUMP_LIMIT)

            # try opening the file if possible
            path = f"{self.path_to_inverted_index}/title{save_counter}.txt"
            if not exists(path):
                continue

            # open the file and read the specified line number
            with open(path, "r") as f:
                lines = f.readlines()
                title = lines[line_number].strip()
                print(f"[{round(score, 2)}] {title}")
