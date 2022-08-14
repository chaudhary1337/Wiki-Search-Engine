from extract import Extract
from misc import FIELDS, PRINT_LIMIT, DUMP_LIMIT, log

from collections import Counter, defaultdict
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

        return {
            "t": title,
            "b": body,
            "i": infoboxes,
            "c": categories,
            "l": links,
            "r": references,
        }


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

        # pages setup
        self.inverted_index = defaultdict(list)

    @log
    def dump_pages(self):
        # storing the inverted index
        with open(
            f"{self.path_to_inverted_index}/index{self.page_count//DUMP_LIMIT}.txt", "w"
        ) as f:
            for word in sorted(self.inverted_index):
                line = word + ";" + " ".join(self.inverted_index[word]) + "\n"
                f.write(line)

        # pages cleanup
        self.inverted_index = defaultdict(list)

    def dump_page(self, extracted_page):
        # add the page's information to the inverted index
        words_set = set()
        counted_index = defaultdict(list)
        for field in FIELDS:
            counted_index[field] = Counter(extracted_page[field])
            words_set.update(counted_index[field].keys())

        for word in words_set:
            encoded = str(self.page_count)
            for field in FIELDS:
                if word in counted_index[field]:
                    encoded += field + str(counted_index[field][word])
            self.inverted_index[word].append(encoded)

        # if the page count is a multiple of the DUMP_LIMIT
        # then we do write the values
        if self.page_count and self.page_count % DUMP_LIMIT == 0:
            self.dump_pages()

        return

    def startElement(self, name, _):
        # keep a track of the current tag being seen
        self.curr_tag = name

    def endElement(self, name):
        # if page not ending, we keep on using the
        # characters(content) method to add details
        if name != "page":
            return

        # the current page is sent to being handled
        # and then dumped into the inverted index
        extracted_page = self.page_handler.handle(self.page)
        self.dump_page(extracted_page)

        # page ends, so fresh start
        self.page = defaultdict(list)
        self.page_count += 1

        # log
        if self.page_count % PRINT_LIMIT == 0:
            print(f"Parsed {self.page_count} pages.")

    def characters(self, content):
        # adds content to a page depending upon which tag is active
        if self.curr_tag == "title":
            self.page["title"].append(content)
        elif self.curr_tag == "text":
            self.page["body"].append(content)
        else:
            pass
