import time

# a logger function, keeps a track of the total running time
def log(end="\n", show_text=True):
    def logger(func):
        def inner(*args, **kwargs):
            start_time = time.time()
            if show_text:
                print(f'Running: "{func.__name__}" ... ', end=end)
            func(*args, **kwargs)
            end_time = time.time()
            if show_text:
                print(f"Done: '{func.__name__}'. ", end="")
            print(f"Taken {round(end_time-start_time, 4)}s")

        return inner

    return logger


# encodes the int value to a hex to save space
def enc(s):
    return str(hex(s))[2:]


# decodes the hex value to an integer for tf-idf and all
# later on
def dec(hax):
    return int("0x" + hax, 16)


# IMPORTANT config
# prints every specified pages, that yes, these many pages have been parsed
PRINT_LIMIT = 10000
# dumps every specified pages to avoid the information in inverted
# index blowing up
DUMP_LIMIT = 50000
# the total number of documents
TOTAL = 476811
# cache for pystemmer
STEM_CACHE = 10000000
# number of "threads" for multi-processing in python
NUM_PROCESSES = 4

# mapping from human readable field to dumpable field
FIELDS = {
    "t": "p",
    "i": "q",
    "b": "r",
    "c": "s",
    "l": "t",
    "r": "u",
}

# config to tune while searching
# NOTE: empty string represents the vanilla field
# that is, user has not specified anything
FIELD_WEIGHTS = {
    "": 1,
    "t": 10,
    "i": 4,
    "b": 3,
    "c": 2,
    "l": 1,
    "r": 1,
}

# multiplied by this amount if a match happens for a query
BONUS_DEFAULT = 1
BONUS_MISMATCH = 0
BONUS = 1.5

# reverse mapping of the fields dumped to be used during searching
RFIELDS = {
    "p": "t",
    "q": "i",
    "r": "b",
    "s": "c",
    "t": "l",
    "u": "r",
}

# custom stemmed stopwords
CUSTOM_STOPWORDS = [
    "www",
    "https",
    "http",
    "com",
    "ref",
    "reflist",
    "jpg",
    "description",
    "redirect",
    "category",
    "name",
    "refer",
    "title",
    "date",
    "image",
    "author",
    "url",
    "use",
    "infobox",
    "site",
    "web",
    "also",
    "defaultsort",
    "use",
    "list",
    "org",
    "publish",
    "cite",
    "website",
    "caption",
    "link",
]
