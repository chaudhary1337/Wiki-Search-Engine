import time


def log(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        print(f'Running: "{func.__name__}" ...')
        func(*args, **kwargs)
        end_time = time.time()
        print(f"Done.\nTaken {round(end_time-start_time, 4)}s")

    return inner


def enc(s):
    return str(hex(s))[2:]


def dec(hax):
    return int("0x" + hax, 16)


CUSTOM_STOPWORDS = [
    "https",
    "http",
    "infobox",
    "wikidata",
    "wikipedia",
    "redirect",
]

PRINT_LIMIT = 10000
DUMP_LIMIT = 50000

FIELDS = ["t", "i", "b", "c", "l", "r"]
