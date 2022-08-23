from search.extract import Extract
from help import DUMP_LIMIT, FIELD_WEIGHTS, FIELDS, RFIELDS, dec

from collections import Counter, defaultdict


class Search:
    def __init__(self, path_to_inverted_index):
        self.extract = Extract()
        self.path_to_inverted_index = path_to_inverted_index

    def search_token(self, token, field):
        field_id = FIELDS[field]

        mini_token = token[:3]
        n = len(token)
        data = None

        with open(f"{self.path_to_inverted_index}/merged_{mini_token}.txt", "r") as f:
            while line := f.readline():
                if line[:n] == token:
                    token, data = line.split()
                    break

        pages = data.split(";")

        if len(pages) == 0:
            return {}

        field_matches = defaultdict(int)
        for page in pages:
            page_id, field_data = page.split(":")

            i = 0
            buffer = []
            while i < len(field_data):
                while i < len(field_data) and field_data[i] not in RFIELDS:
                    buffer.append(field_data[i])
                    i += 1

                # if the current buffer is useful, store it
                # since the current field is matching
                if field_data[i] == field_id:
                    field_matches[dec(page_id) - 1] += (
                        dec("".join(buffer)) * FIELD_WEIGHTS[field]
                    )

                # by default, reset the buffer
                # and increase the counter
                buffer = []
                i += 1

        return field_matches

    def search(self, query, k=10):
        # extracted_query = self.extract.extract(query)

        query_counter = Counter()
        for token in query.split():
            query_counter += self.search_token(token, "b")

        topk = query_counter.most_common(k)

        for page_id, tf in topk:
            save_counter, line_number = divmod(page_id, DUMP_LIMIT)

            with open(
                f"{self.path_to_inverted_index}/title{save_counter}.txt", "r"
            ) as f:
                lines = f.readlines()
                print(lines[line_number].strip())
