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

        return infoboxes

    def get_links(self, text):
        return re.findall(r"\[(http.*?)\]", text)

    def get_categories(self, text):
        return re.findall(r"\[\[category:(.*?)\]\]", text)

    def get_references(self, text):
        return re.findall(r"\{\{(.*?)\}\}", text)

    def get_text(self, text):
        text = " ".join(text)
        text = text.lower()

        breaker = re.split("==references==", text)
        if len(breaker) < 2:
            breaker.append("")

        body = breaker[0]
        infoboxes = self.get_infobox(breaker[0])
        links = self.get_links(breaker[1])
        categories = self.get_categories(breaker[1])
        references = self.get_references(breaker[1])

        return list(
            map(
                self.clean,
                [
                    body,
                    " ".join(infoboxes),
                    " ".join(links),
                    " ".join(categories),
                    " ".join(references),
                ],
            )
        )
