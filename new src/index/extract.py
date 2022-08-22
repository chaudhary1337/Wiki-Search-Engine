from help import CUSTOM_STOPWORDS

from nltk.corpus import stopwords
import Stemmer


class Extract:
    def __init__(self):
        self.nltk_stopwords = stopwords.words("english")
        self.stopwords = set(self.nltk_stopwords + CUSTOM_STOPWORDS)
        self.stem = Stemmer.Stemmer("english").stemWords

    def extract(self, page):
        """
        returns the extracted page of the form:
        {
            field: list of words
        }
        """
        title = "".join(page["title"]).lower()
        body = "".join(page["body"]).lower()

        return {
            "t": title.split(),
            "i": [],
            "b": body.split(),
            "c": [],
            "l": [],
            "r": [],
        }
