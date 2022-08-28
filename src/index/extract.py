from string import ascii_lowercase, digits
from help import CUSTOM_STOPWORDS, FIELDS

from nltk.corpus import stopwords
import Stemmer

import re


class Extract:
    def __init__(self):
        # setting up the 2 required stuffs
        # 1. stopwords
        # 2. stemmer
        self.nltk_stopwords = stopwords.words("english")
        self.custom_stopwords = CUSTOM_STOPWORDS
        self.stopwords = set(self.nltk_stopwords + self.custom_stopwords)
        self.stemwords = Stemmer.Stemmer("english").stemWords

        # a mapping from words to their stemmed versions
        # saves on time, since stemming is the heaviest operation
        self.stemword_d = {}

        # this is the page information that will be used directly
        # outside of this class
        # NOTE: needs to be flushed for another page.
        self.extracted_page = {field: [] for field in FIELDS}

    def clean(self, text):
        return re.sub("[^0-9a-z ]", "", text)

    def fix(self, text, c=" "):
        return c.join(text).lower() if type(text) == list else text

    def stem(self, tokens):
        tokens_stemmed = []
        for token in tokens:
            if token not in self.stemword_d:
                self.stemword_d[token] = self.stemwords([token])[0]
            tokens_stemmed.append(self.stemword_d[token])

        return tokens_stemmed

    def tokenize(self, text):
        tokens = text.split()
        tokens = [token for token in tokens if token not in self.stopwords]
        tokens = [token for token in tokens if 2 <= len(token) < 15]
        # tokens = self.stem(tokens)
        return tokens

    def extract_title(self, title):
        title = self.fix(title)
        title = self.clean(title)
        title = self.tokenize(title)
        self.extracted_page["t"] = title
        return

    def get_infobox(self, lines, i):
        infobox = []

        brackets = 0
        completed = False

        while i < len(lines):
            line = lines[i]

            for c in line:
                if c in "{}":
                    brackets += 1 if c == "{" else -1

                if brackets == 0:
                    completed = True

            infobox.extend(self.tokenize(self.clean(line.strip())))
            if completed:
                break
            i += 1

        self.extracted_page["i"].extend(infobox)
        return i

    def get_body(self, lines, i):
        self.extracted_page["b"].extend(self.tokenize(self.clean(lines[i].strip())))
        return i

    def extract_text(self, text):
        text = self.fix(text)
        lines = text.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("{{infobox") or line.startswith("{{ infobox"):
                i = self.get_infobox(lines, i)
            else:
                i = self.get_body(lines, i)

            i += 1

    def extract(self, page):
        self.extract_title(page["title"])
        self.extract_text(page["text"])

    def flush(self):
        self.extracted_page = {field: [] for field in FIELDS}
