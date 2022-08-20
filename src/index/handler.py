from index.extract import Extract
from misc import FIELDS, PRINT_LIMIT, DUMP_LIMIT, log, enc

from collections import Counter, defaultdict
from xml import sax as sx

# handles information of ONE specific page
class PageHandler:
    def __init__(self):
        self.extract = Extract()

    def handle(self, page):
        """extracts all the relevant fields from the page"""
        title = page["title"]
        body = page["body"]

        title = self.extract.extract_title(title)
        body, infoboxes, categories, links, references = self.extract.extract_text(body)

        return {
            "t": title,
            "b": body,
            "i": infoboxes,
            "c": categories,
            "l": links,
            "r": references,
        }


class ContentHandler(sx.ContentHandler):
    """
    handles the entire content handling system

    reads individual pages
    extracts information from them using page handler
    and then dumps the information to a file every specified
    duration (as per the misc.py file)
    """

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

        # global setup
        self.total_tokens = 0
        self.total_tokens_inverted_index = 0

    @log
    def dump_pages(self):
        self.total_tokens_inverted_index += len(self.inverted_index)

        # storing the inverted index
        lines = []
        # for word in sorted(self.inverted_index):
        for word in sorted(self.inverted_index):
            word_data = " ".join(self.inverted_index[word])
            lines.append(f"{word};{word_data}\n")

        with open(
            f"{self.path_to_inverted_index}/index{self.page_count//DUMP_LIMIT}.txt", "w"
        ) as f:
            f.write("".join(lines))

        # pages cleanup
        self.inverted_index = defaultdict(list)
        return

    def dump_page(self, extracted_page):
        # add the page's information to the inverted index
        words_set = set()
        counted_index = defaultdict(list)
        for field in FIELDS:
            counted_index[field] = Counter(extracted_page[field])
            words_set.update(counted_index[field].keys())

        for word in words_set:
            encoded = enc(self.page_count)
            for field in FIELDS:
                if word in counted_index[field]:
                    encoded += field + enc(counted_index[field][word])
            self.inverted_index[word].append(encoded)

        # if the page count is a multiple of the DUMP_LIMIT
        # then we do write the values
        if self.page_count and self.page_count % DUMP_LIMIT == 0:
            self.dump_pages()

        return

    def cleanup(self):
        if self.inverted_index:
            self.dump_pages()
        return

    def get_total_token_count(self, extracted_page):
        return (
            len(extracted_page["t"])
            + len(extracted_page["b"])
            + len(extracted_page["c"])
            + len(extracted_page["l"])
            + len(extracted_page["r"])
        )

    def startElement(self, name, _):
        # keep a track of the current tag being seen
        self.curr_tag = name
        return

    def endElement(self, name):
        # if the end element is mediawiki, then we have completed our
        # indexing
        if name == "mediawiki":
            self.cleanup()
            return

        # if page not ending, we keep on using the
        # characters(content) method to add details
        if name != "page":
            return

        # the current page is sent to being handled
        # and then dumped into the inverted index
        extracted_page = self.page_handler.handle(self.page)
        self.dump_page(extracted_page)

        self.total_tokens += self.get_total_token_count(extracted_page)

        # page ends, so fresh start
        self.page = defaultdict(list)
        self.page_count += 1

        # log
        if self.page_count % PRINT_LIMIT == 0:
            print(f"Parsed {self.page_count} pages.")
        return

    def characters(self, content):
        # adds content to a page depending upon which tag is active
        if self.curr_tag == "title":
            self.page["title"].append(content)
        elif self.curr_tag == "text":
            self.page["body"].append(content)
        else:
            pass
