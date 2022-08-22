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

    def save_page(self, page_id, page):
        """
        adds information to the inverted_index
        """
        extracted_page = self.extract.extract(page)

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
            for field in FIELDS:
                # if this combination is unseen, create a new list
                if field not in self.inverted_index[word]:
                    self.inverted_index[word][field] = []

                self.inverted_index[word][field].append(
                    # for a given word
                    # in a given field
                    # here is the page id and the term freq
                    enc(page_id)
                    + ":"
                    + enc(frequency[field][word])
                )

        # if the number of pages parsed crosses the dump limit
        # then self trigger the dump
        if page_id and page_id % DUMP_LIMIT == 0:
            self.save_pages()

    @log
    def save_pages(self):
        """
        dumps the inverted_index

        format:

        word field1;field2;field3;field4;field5;field6

        where field1 is
        page_id1:term_freq1,page_id2:term_freq2

        NOTE:
        can later add something like word overall_freq field1;...
        basically, add the overall term frequency
        """

        word_data = []
        # goes over all the words in sorted ordering
        for word in sorted(self.inverted_index):
            field_data = []

            for field in FIELDS:
                page_data = self.inverted_index[word][field]
                field_data.append(",".join(page_data))

            # joins all the field_data for each field by a semicolon
            word_data.append(word + " " + ";".join(field_data))

        with open(
            f"{self.path_to_inverted_index}/index{self.save_counter}.txt", "w"
        ) as f:
            f.write("\n".join(word_data))

        # resetting the inverted index
        self.inverted_index = defaultdict(defaultdict)
        self.save_counter += 1
