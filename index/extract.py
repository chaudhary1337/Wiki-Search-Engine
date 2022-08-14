from misc import CUSTOM_STOPWORDS

from nltk.corpus import stopwords
import Stemmer

import re


class Extract:
    def __init__(self):
        self.nltk_stopwords = stopwords.words("english")
        self.custom_stopwords = CUSTOM_STOPWORDS
        self.stopwords = set(self.nltk_stopwords + self.custom_stopwords)

        self.stem_words = Stemmer.Stemmer("english").stemWords

    def clean(self, text):
        text = re.sub("http[s]?://\S+", "", text)
        text = re.sub("&lt|&gt|&amp|&quot|&apos|&nbsp", " ", text)
        text = re.sub("[^a-z0-9 ]", " ", text)

        tokens = text.split()
        tokens_nonstop = [token for token in tokens if token not in self.stopwords]
        tokens_stemmed = self.stem_words(tokens_nonstop)

        return tokens_stemmed

    def get_title(self, title):
        title = " ".join(title)
        title = title.lower()
        return title

    def get_infobox(self, text):
        n = len(text)
        infoboxes = []

        for ib in re.finditer("{{infobox", text):
            brackets = 0
            for i in range(ib.start(), n):
                if text[i] == "{":
                    brackets += 1
                elif text[i] == "}":
                    brackets -= 1

                if brackets == 0:
                    break

            infoboxes.append(text[ib.start() : i])

        return " ".join(infoboxes)

    def get_links(self, text):
        return re.findall(r"\[http.*?\]", text)

    def get_categories(self, text):
        return re.findall(r"\[\[category:(.*?)\]\]", text)

    def get_references(self, text):
        return re.findall(r"\{\{(.*?)\}\}", text)[1:]

    def get_text(self, text):
        text = " ".join(text)
        text = text.lower()

        breaker = re.split("==see also==", text)

        body = breaker[0]
        infoboxes = self.get_infobox(breaker[0])
        links = self.get_links(breaker[-1])
        categories = self.get_categories(breaker[-1])
        references = self.get_references(breaker[-1])

        return body, infoboxes, categories, links, references

    # def get_heading(self, line):
    #     i = 1
    #     n = len(line)

    #     while i < n and line[i] == "=":
    #         i += 1

    #     if i == 1:
    #         return ""

    #     heading = []
    #     while i < n and line[i] != "=":
    #         heading.append(line[i])
    #         i += 1

    #     return "".join(heading)

    # def handle_buffer(self, heading, buffer):
    #     print(heading, self.clean("".join(buffer)))

    # def get_text(self, text):
    #     text = " ".join(text)
    #     text = text.lower()

    #     print(text)

    #     buffer = []
    #     prev_heading = ""

    #     for line in text.split("\n"):
    #         if len(line) == 1:
    #             continue

    #         heading = self.get_heading(line)

    #         if heading:
    #             self.handle_buffer(prev_heading, buffer)
    #             buffer = []
    #             prev_heading = heading
    #         else:
    #             buffer.append(line)

    #     self.handle_buffer(prev_heading, buffer)


# test
# extract = Extract()
# print(extract.stopwords)
# print(extract.clean("text http://wow-nice cycling fast speeding"))
