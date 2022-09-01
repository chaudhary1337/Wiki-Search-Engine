import re
from string import ascii_lowercase, digits
from nltk.corpus import stopwords
import Stemmer

from help import CUSTOM_STOPWORDS, FIELDS, STEM_CACHE


class Extract:
    def __init__(self):
        self.stopwords = set(stopwords.words("english") + CUSTOM_STOPWORDS)
        self.stemmer = Stemmer.Stemmer("english")
        self.stemmer.maxCacheSize = STEM_CACHE
        self.stemwords = self.stemmer.stemWords

        # regex compiled for *speed*
        self.re_links = re.compile("http[^ ]*")
        self.re_nonalpha = re.compile("[^0-9a-z ]")
        self.re_refs = re.compile(r"\< ref \>(.*?)\< \/ref \>")

        # this is the page information that will be used directly
        # outside of this class
        # NOTE: needs to be flushed for another page.
        self.extracted_page = {field: [] for field in FIELDS}

    def is_valid(self, token):
        return not (
            not 2 <= len(token) <= 13
            or token in self.stopwords
            or (token[0] in digits and len(token) > 4)
            or (
                any(c in ascii_lowercase for c in token)
                and any(c in digits for c in token)
            )
        )

    def tokenize(self, text):
        text = self.re_links.sub(" ", text)
        text = self.re_nonalpha.sub(" ", text)

        tokens = text.split()
        tokens = [token for token in tokens if self.is_valid(token)]
        tokens = self.stemwords(tokens)

        return tokens

    def extract_title(self, title):
        title = " ".join(title).lower()
        self.extracted_page["t"].append(title)

    def is_infobox(self, lines, i):
        return lines[i].startswith("{{infobox") or lines[i].startswith("{{ infobox")

    def get_infobox(self, lines, i):
        brackets = 0
        completed = False

        while i < len(lines):
            line = lines[i]
            self.extracted_page["i"].append(line)

            # handles the logic to end the infobox
            for c in line:
                if c in "{}":
                    brackets += 1 if c == "{" else -1

                if brackets == 0:
                    completed = True

            if completed:
                break

            i += 1

        return i

    def get_body(self, lines, i):
        self.extracted_page["b"].append(lines[i])
        return i

    def get_category(self, lines):
        cat = "[[category:"

        for line in lines.split("\n"):
            if line.startswith(cat):
                self.extracted_page["c"].append(line[len(cat) : -2])

    def get_link(self, lines):
        split_lines = lines.split("==external links==")

        if len(split_lines) == 2:
            self.extracted_page["l"].append(split_lines[1])

        return

    def get_reference(self, lines):
        self.extracted_page["r"].append(lines.split("==", maxsplit=1)[0])
        return

    def get_other_references(self, text):
        references = self.re_refs.findall(text)

        for reference in references:
            self.extracted_page["r"].append(reference)
        return

    def extract_text(self, text):
        lines = "\n".join(line.lower() for line in text)

        lines = lines.replace("== ", "==")
        lines = lines.replace(" ==", "==")

        split_lines = lines.split("==references==")

        if len(split_lines) == 2:
            self.get_category(split_lines[1])
            self.get_reference(split_lines[1])
            self.get_link(split_lines[1])

        i = 0
        upper = split_lines[0].split("\n")
        while i < len(upper):
            if self.is_infobox(upper, i):
                i = self.get_infobox(upper, i)
            else:
                i = self.get_body(upper, i)

            i += 1

        self.get_other_references(lines)

    def extract(self, page):
        self.extract_title(page["title"])
        self.extract_text(page["text"])

        # tokenizing all the field informations
        for field in FIELDS:
            self.extracted_page[field] = self.tokenize(
                " ".join(self.extracted_page[field])
            )

    def flush(self):
        self.extracted_page = {field: [] for field in FIELDS}
