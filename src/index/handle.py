from collections import defaultdict
from time import time
from xml import sax as sx

from help import PRINT_LIMIT
from index.page import Pages


class ContentHandler(sx.ContentHandler):
    def __init__(self, path_to_inverted_index):
        # setup
        self.path_to_inverted_index = path_to_inverted_index

        # keeping a track of the current stuff
        self.curr_tag = ""
        self.time = time()

        # handles all the page related stuff
        # page count is the same as the page id
        self.page_count = 0
        self.page = defaultdict(list)
        self.pages = Pages(path_to_inverted_index)
        return

    def startElement(self, name, _):
        self.curr_tag = name
        return

    def endElement(self, name):
        # if reached the end, force dump everything
        if name == "mediawiki":
            self.pages.save_pages()

        # if the current tag is not a page, we do not do anything
        if name != "page":
            return

        # logging
        if self.page_count and self.page_count % PRINT_LIMIT == 0:
            curr_time = time()
            print(
                f"Parsed {self.page_count} pages. Taken {round(curr_time - self.time, 4)}"
            )
            self.time = curr_time

        # save the page
        self.pages.save_page(self.page_count, self.page)

        # prepare for the next page
        self.page_count += 1
        self.page = defaultdict(list)

    def characters(self, content):
        if self.curr_tag not in ["title", "text"]:
            return

        self.page[self.curr_tag].append(content)
        return
