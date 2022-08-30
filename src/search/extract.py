from collections import defaultdict

from nltk.corpus import stopwords
import Stemmer

from help import CUSTOM_STOPWORDS, FIELDS


class Extract:
    def __init__(self):
        self.nltk_stopwords = stopwords.words("english")
        self.custom_stopwords = CUSTOM_STOPWORDS
        self.stopwords = set(self.nltk_stopwords + self.custom_stopwords)
        self.stemwords = Stemmer.Stemmer("english").stemWords

    def clean(self, text):
        tokens = text.split()
        tokens_nonstop = [token for token in tokens if token not in self.stopwords]
        tokens_stemmed = self.stemwords(tokens_nonstop)

        return tokens_stemmed

    def is_field_query(self, i, query):
        if i + 1 < len(query) and query[i] in FIELDS and query[i + 1] == ":":
            return query[i]
        else:
            return ""

    def get_buffers_while(self, i, query):
        buffer = []
        while i < len(query) and not self.is_field_query(i, query):
            buffer.append(query[i])
            i += 1
        return i, "".join(buffer).strip()

    def extract(self, query):
        """
        extracts all the information of a query
        requires the vanilla keywords to be present at the start

        returns a dictionary of {
            field: list(list(stemmed keywords))
        }

        the field for vanilla keywords is ""
        for the rest is the first word of the supported fields
        """
        query = query.lower()

        i = 0
        extracted = defaultdict(list)

        while i < len(query):
            # get the current field if exists, else ""
            field = self.is_field_query(i, query)

            # skipping the "X:" part, where X is the field
            if field:
                i += 2

            # gets the new i and the buffer
            i, buffer = self.get_buffers_while(i, query)

            # clean the buffer and add it
            extracted[field].append(buffer)

        for field in FIELDS:
            extracted[field] = self.clean(" ".join(extracted[field]))
        return extracted
