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

    def clean(self, text):
        # removes the links
        text = re.sub("http[^\s]*", " ", text)
        # removes the junk
        text = re.sub("&lt|&gt|&amp|&quot|&apos|&nbsp", " ", text)
        # filers out the non-alphanumeric characters
        text = re.sub("[^0-9a-z ]", " ", text)

        tokens = text.split()

        return tokens

    def extract(self, page):
        title = "".join(page["title"]).lower()
        text = " ".join(page["text"]).lower()

        # cleans up all the individual respective fields
        cleaned_page = list(
            map(
                self.clean,
                [
                    title,
                    "",
                    text,
                    "",
                    "",
                    "",
                ],
            )
        )

        return {field: field_data for field, field_data in zip(FIELDS, cleaned_page)}
