import time


def log(func):
    def inner():
        start_time = time.time()
        print(f'Running: "{func.__name__}" ...')
        func()
        end_time = time.time()
        print(f"Done.\nTaken {round(end_time-start_time, 4)}s")

    return inner


CUSTOM_STOPWORDS = [
    "https",
    "http",
]
