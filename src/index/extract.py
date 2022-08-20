from misc import CUSTOM_STOPWORDS

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

    def clean(self, text):
        # removes the links
        text = re.sub(r"http[s]?://\S+", " ", text)
        # removes the jumnk
        text = re.sub("&lt|&gt|&amp|&quot|&apos|&nbsp", " ", text)
        # filers out the non-alphanumeric characters
        text = re.sub("[^0-9a-z ]", " ", text)

        tokens = text.split()
        tokens_nonstop = [token for token in tokens if token not in self.stopwords]
        tokens_stemmed = self.stemwords(tokens_nonstop)

        return tokens_stemmed

    def clean_body(self, text):
        text = re.sub("{{.*?}}", "", text)
        text = re.sub("[[.*?]]", "", text)
        return text

    def extract_title(self, title):
        title = " ".join(title)
        title = title.lower()
        return self.clean(title)

    def extract_infobox(self, text):
        n = len(text)
        infoboxes = []

        for ib in re.finditer("{{infobox", text):
            brackets = 0
            for i in range(ib.start(), n):
                # if a bracket
                # do a +1 or -1 if { or } respectively
                if text[i] in "{}":
                    brackets += 1 if text[i] == "{" else -1

                # if we have used up all the brackets
                # we are at the end of the infobox
                if brackets == 0:
                    break

            # string splicing, might consider
            # speeding this up later
            infoboxes.append(text[ib.start() : i])

        return infoboxes

    def extract_links(self, text):
        return re.findall(r"\[(http.*?)\]", text)

    def extract_categories(self, text):
        return re.findall(r"\[\[category:(.*?)\]\]", text)

    def extract_references(self, text):
        return re.findall(r"\{\{(.*?)\}\}", text)

    def extract_text(self, text):
        text = " ".join(text)
        text = text.lower()

        # breaking the text into two parts,
        # so that the body + infobox area is split from the
        # references, categories and links
        breaker = re.split("==references==", text)
        if len(breaker) < 2:
            breaker.append("")

        body = self.clean_body(str(breaker[0]))
        infoboxes = " ".join(self.extract_infobox(breaker[0]))
        links = " ".join(self.extract_links(breaker[1]))
        categories = " ".join(self.extract_categories(breaker[1]))
        references = " ".join(self.extract_references(breaker[1]))

        # cleans up all the individual respective fields
        return list(
            map(
                self.clean,
                [
                    body,
                    infoboxes,
                    links,
                    categories,
                    references,
                ],
            )
        )
