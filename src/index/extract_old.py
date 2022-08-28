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

        self.extracted_page = {field: None for field in FIELDS}

    def process(self, text):
        # removes the junk
        text = re.sub("&lt|&gt|&amp|&quot|&apos|&nbsp", "", text)
        # removes the links
        text = re.sub("http[^ ]*", " ", text)
        # remove the comments
        text = re.sub("<!--.*-->", " ", text)
        # converting all useful characters to a space
        # so that it is preserved
        text = re.sub("\n|:", " ", text)
        # filers out the non-alphanumeric characters
        text = re.sub("[^0-9a-z\s]", "", text)

        return text

    def tokenize(self, text):
        tokens = text.split()
        tokens = [token for token in tokens if token not in self.stopwords]
        tokens = [token for token in tokens if 2 <= len(token) < 15]
        tokens = self.stemwords(tokens)
        return tokens

    def extract_title(self, title):
        self.extracted_page["t"] = self.tokenize(self.process(title))

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

        self.extracted_page["i"] = self.tokenize(self.process(" ".join(infoboxes)))

    def extract_body(self, text):
        self.extracted_page["b"] = self.tokenize(self.process(text))

    def extract_category(self, text):
        categories = " ".join(re.findall("\[\[category:(.*)\]\]", text))
        categories = re.sub("[^0-9a-z ]", " ", categories)

        self.extracted_page["c"] = self.tokenize("".join(categories))

    def extract_link(self, text):
        ending = re.split("==\ *external links\ *==", text)

        # if no links present, sad
        if len(ending) == 1:
            return []

        links = []

        for line in ending[1].split("\n"):
            # if starts with a star, is a reference
            if line and line[0] == "*":
                links.append(line)
            # belongs to another sub-heading: {{DEFAULTSORT:...}}
            elif len(line) > 2 and line[0] == line[1] == "{" and line[2] == "D":
                break
            # belongs to another sub-heading: [[Category:...]]
            elif len(line) > 2 and line[0] == line[1] == "[" and line[2] == "C":
                break
            else:
                continue

        self.extracted_page["l"] = self.tokenize(self.process("".join(links)))

    def extract_reference(self, text):
        ending = re.split("==\ *references\ *==", text)

        # if no ref present, sad
        if len(ending) == 1:
            return []

        references = []

        for line in ending[1].split("\n"):
            # if starts with a star, is a reference
            if line and line[0] == "*":
                references.append(line)
            # if heading is ===ASDF===, then is allowed
            # if heading is ==WOW== then its not, since it
            # belongs to another sub-heading
            elif len(line) > 2 and line[0] == line[1] == "=" and line[2] != "=":
                break
            else:
                continue

        self.extracted_page["r"] = self.tokenize(self.process("".join(references)))

    def extract(self, page):
        title = "".join(page["title"]).lower()
        self.extract_title(title)

        text = "".join(page["text"]).lower()
        if "#REDIRECT" == text[: len("#REDIRECT")]:
            return

        functions = [
            self.extract_infobox,
            self.extract_body,
            self.extract_category,
            self.extract_link,
            self.extract_reference,
        ]

        # just run those functions one by one
        for function in functions:
            function(text)

        # THIS KIND OF MULTPROCESSING TAKES TOO LONG
        # DO NOT DO IT
        # processes = []
        # for function in functions:
        #     process = Process(target=function, args=[text])
        #     process.start()
        #     processes.append(process)

        # for process in processes:
        #     process.join()
