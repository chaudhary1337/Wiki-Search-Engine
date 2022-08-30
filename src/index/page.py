from collections import defaultdict
from collections import Counter

from index.extract import Extract
from help import DUMP_LIMIT, FIELDS, enc, log


class Pages:
    def __init__(self, path_to_inverted_index):
        self.path_to_inverted_index = path_to_inverted_index

        # stores the number of times pages are saved
        self.save_counter = 0

        self.pages = []
        # an index of word: field: page_id + ":" term_freq
        self.inverted_index = defaultdict(defaultdict)
        self.extract = Extract()

        # handling titles
        self.titles = []

    def save_page(self, page_id, page):
        """
        adds information to the inverted_index

        NOTE: can later convert all tf="1" values to tf="" to save space
        """
        # title added directly, since that is required for searching
        self.titles.append("".join(page["title"]).lower().strip())

        # page handing
        self.extract.extract(page)
        extracted_page = self.extract.extracted_page
        self.extract.flush()

        # keeps a track of all the words encountered currently
        words = set()
        # frequency[field][word] = term frequency
        # basically, for this word in this field, how many times
        # does it occur?
        frequency = defaultdict(Counter)

        for field in FIELDS:
            field_words = extracted_page[field]
            # creating a counter of the field words
            frequency[field] = Counter(field_words)
            # adding the keys of the counter (words) to the words set
            words.update(frequency[field].keys())

        # storing all the information
        for word in words:
            # for this word
            # and for this page id
            self.inverted_index[word][page_id] = []

            for field in FIELDS:
                # if the frequency of the word in a field is 0
                # skip
                if frequency[field][word] == 0:
                    continue

                # getting the encoded tf
                # 1x is saved as x only. search needs to handle such cases.
                tf = enc(frequency[field][word]) if frequency[field][word] > 1 else ""
                # getting the field_id and NOT the field itself
                field_id = FIELDS[field]

                # appending in list
                self.inverted_index[word][page_id].append(tf + field_id)

        # if the number of pages parsed crosses the dump limit
        # then self trigger the dump
        if page_id and page_id % DUMP_LIMIT == 0:
            self.save_pages()

    @log(end="")
    def save_pages(self):
        """
        dumps the inverted_index

        format:

        word page_id:tf1fid1tf2fid2;page_id:...

        where fid1 and tf1 represent the field id and the term frequency


        NOTE:
        can later add something like word overall_freq page_id:...
        basically, add the overall term frequency
        """

        # goes over all the words in sorted ordering
        full_data = []
        for word in sorted(self.inverted_index):
            word_data = []
            for page_id in self.inverted_index[word]:
                # concatenate the data for a given word, for a given page_id
                word_data.append(
                    "".join(
                        [enc(page_id), ":", "".join(self.inverted_index[word][page_id])]
                    )
                )

            # have a ; between information of each page
            full_data.append("".join([word, " ", ";".join(word_data)]))

        with open(
            f"{self.path_to_inverted_index}/index{self.save_counter}.txt", "w"
        ) as f:
            f.write("\n".join(full_data))

        with open(
            f"{self.path_to_inverted_index}/title{self.save_counter}.txt", "w"
        ) as f:
            f.write("\n".join(self.titles))

        # resetting everything
        self.inverted_index = defaultdict(defaultdict)
        self.save_counter += 1
        self.titles = []
