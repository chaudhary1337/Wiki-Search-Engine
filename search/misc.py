import time

# a logger function, keeps a track of the total running time
def log(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        print(f'Running: "{func.__name__}" ...')
        func(*args, **kwargs)
        end_time = time.time()
        print(f"Done.\nTaken {round(end_time-start_time, 4)}s")

    return inner


# encodes the int value to a hex to save space
def enc(s):
    return str(hex(s))[2:]


# decodes the hex value to an integer for tf-idf and all
# later on
def dec(hax):
    return int("0x" + hax, 16)


# some custom stopwords
CUSTOM_STOPWORDS = [
    "https",
    "http",
    "infobox",
    "wikidata",
    "wikipedia",
    "redirect",
]

# IMPORTANT config
# prints every specified pages, that yes, these many pages have been parsed
PRINT_LIMIT = 10000
# dumps every specified pages to avoid the information in inverted
# index blowing up
DUMP_LIMIT = 50000

# all the supported fields
FIELDS = ["t", "i", "b", "c", "l", "r"]

# for later if I want to use multiprocessing
NUM_PROCESSES = 5
