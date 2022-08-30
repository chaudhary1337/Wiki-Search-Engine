from collections import Counter, defaultdict
from os.path import exists
from math import log
from time import time

from search.extract import Extract
from search.parse import Parse

from help import FIELD_WEIGHTS, TOTAL, dec


class Search:
    def __init__(self, path_to_inverted_index, in_file, out_file):
        self.path_to_inverted_index = path_to_inverted_index
        self.in_file = in_file
        self.out_file = out_file

        self.extract = Extract()
        self.parse = Parse(path_to_inverted_index)

    def search_token(self, token, field):
        field_matches = defaultdict(int)

        pages = self.parse.get_token_pages(token)

        # idf is the number of pages this token appears in
        idf = len(pages)
        # if the number of pages is 0, then this token is not
        # in the data dump
        if idf == 0:
            return field_matches

        for page in pages:
            if not page:
                continue

            page_id, field_data = page.split(":")

            i = -1
            while (i := i + 1) < len(field_data):
                # reads the characters while a field is not seen
                # gets the appropriate bonus for a field
                # if matching, we give BONUS, else BONUS_DEFAULT
                i, tf, bonus = self.parse.get_tf_bonus(field_data, i, field)

                # calculates the current score of the token
                # in the specified field
                score = log(1 + tf) * log(TOTAL / idf) * bonus * FIELD_WEIGHTS[field]

                # for this page_id, increase its ranking by score
                field_matches[dec(page_id)] += score

        return field_matches

    def search_query(self, query, k=10):
        start_time = time()

        extracted_query = self.extract.extract(query)

        query_counter = Counter()
        # has one more key, the "" other than FIELDS
        for field in extracted_query.keys():
            for token in extracted_query[field]:
                query_counter.update(self.search_token(token, field))

        topk = query_counter.most_common(k)
        titles = self.parse.get_titles(topk)

        for score, title in sorted(titles, reverse=True):
            self.out_file.write(title + "\n")

        self.out_file.write(f"{round(time() - start_time)}\n\n")

    def search(self):
        queries = self.in_file.readlines()
        for query in queries:
            self.search_query(query)
        return
