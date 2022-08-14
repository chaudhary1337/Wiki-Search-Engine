from extract import Extract

from collections import defaultdict
from xml import sax as sx


class PageHandler:
    def __init__(self):
        self.extract = Extract()

    def handle(self, page):
        """extracts all the relevant fields from the page"""
        title = page["title"]
        body = page["body"]

        title = self.extract.get_title(title)
        body, infoboxes, categories, links, references = self.extract.get_text(body)


class ContentHandler(sx.ContentHandler):
    def __init__(self, path_to_inverted_index):
        # necessary setup
        self.path_to_inverted_index = path_to_inverted_index

        # keep a track of the current tag for a page
        self.curr_tag = ""

        # page setup
        self.page = defaultdict(list)
        self.page_handler = PageHandler()
        self.page_count = 0

    def startElement(self, name, _):
        # keep a track of the current tag being seen
        self.curr_tag = name

    def endElement(self, name):
        # if page not ending, we keep on using the
        # characters(content) method to add details
        if name != "page":
            return

        # the current page is sent to being handled
        self.page_handler.handle(self.page)

        # page ends, so fresh start
        self.page = defaultdict(list)
        self.page_count += 1

        # if count exceeds a certain amount, dump it
        if self.page_count > 7:
            exit()
        else:
            print("*" * 80)

    def characters(self, content):
        # adds content to a page depending upon which tag is active
        if self.curr_tag == "title":
            self.page["title"].append(content)
        elif self.curr_tag == "text":
            self.page["body"].append(content)
        else:
            pass
