from search.extract import Extract
from help import DUMP_LIMIT, FIELD_WEIGHTS, dec

from collections import Counter


class Search:
    def __init__(self, path_to_inverted_index):
        self.extract = Extract()
        self.path_to_inverted_index = path_to_inverted_index

    def search_token(self, token, field):
        mini_token = token[:3]
        n = len(token)
        data = None

        with open(f"{self.path_to_inverted_index}/merged_{mini_token}.txt", "r") as f:
            while line := f.readline():
                if line[:n] == token:
                    token, data = line.split()
                    break

        field_data = data.split(";")[field]
        if not field_data:
            return {}

        pages = field_data.split(",")
        if not pages:
            return {}

        token_counter = Counter()
        for page in pages:
            page_id, freq = map(dec, page.split(":"))
            token_counter[page_id] += freq * FIELD_WEIGHTS[field]

        return token_counter

    def search(self, query, k=10):
        # extracted_query = self.extract.extract(query)

        query_counter = Counter()
        for token in query.split():
            query_counter += self.search_token(token, 2)

        topk = query_counter.most_common(k)

        for page_id, tf in topk:
            save_counter, line_number = divmod(page_id, DUMP_LIMIT)

            with open(
                f"{self.path_to_inverted_index}/title{save_counter}.txt", "r"
            ) as f:
                lines = f.readlines()
                print(lines[line_number].strip())
