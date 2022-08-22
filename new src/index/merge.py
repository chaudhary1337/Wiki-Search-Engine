from help import FIELDS, log

from heapq import heapify, heappush, heappop
import os


class FileHandler:
    def __init__(self, f, num):
        self.f = f
        self.num = num
        self.move_next()

    # adding a comparison for the heap
    # token first because we want to keep it sorted by the word
    # then we look at the page numbers,
    # to ensure the sorted ordering again
    def __lt__(self, other):
        return (
            self.num < other.num
            if self.token == other.token
            else self.token < other.token
        )

    # move to the next line, read if possible
    # else return False
    def move_next(self):
        line = self.f.readline()
        if line:
            self.token, self.data = line.split()

        return bool(line)


class Merge:
    def __init__(self, path_to_inverted_index):
        self.path_to_inverted_index = path_to_inverted_index

    def get_files(self):
        files = []
        for path in os.scandir(self.path_to_inverted_index):
            # if a dir, skip
            if not path.is_file():
                continue

            # get the file name from the path
            file_name = path.name
            if file_name[: len("index")] != "index":
                continue

            # then create a file handler to be used in the heap
            f = open(f"{self.path_to_inverted_index}/{file_name}", "r")
            files.append(FileHandler(f, file_name[len("index") :]))

        return files

    def get_merged_data(self, all_data):
        # merging all the field specific data
        # that is, get ALL the possible titles for a word
        # from all the files
        merged_data = [[] for _ in range(len(FIELDS))]

        # going over all the individual lines from different files
        # for a single word

        for data in all_data:
            for i, field_data in enumerate(data.split(";")):
                if not field_data:
                    continue

                merged_data[i].append(field_data)

        # merging all the same field data from all the diff files
        for i in range(len(FIELDS)):
            merged_data[i] = ",".join(merged_data[i])

        # formatting in the same format as used for index saving
        return ";".join(merged_data)

    @log
    def merge(self):
        files = self.get_files()
        heapify(files)

        while files:
            # pop out the smalles value
            smallest_file = heappop(files)
            token, data = smallest_file.token, smallest_file.data

            # mini token is the first 3 chars
            mini_token = token[:3]
            # opening the file of the mini token
            f = open(f"{self.path_to_inverted_index}/merged_{mini_token}.txt", "a+")

            # store all the data for the current token
            all_data = [data]

            # move the file pointer to the next line
            if smallest_file.move_next():
                heappush(files, smallest_file)

            # adding all the document information for a token
            while files and files[0].token == token:
                smallest_file = heappop(files)
                all_data.append(smallest_file.data)

                if smallest_file.move_next():
                    heappush(files, smallest_file)

            f.write(token + " " + self.get_merged_data(all_data) + "\n")
            f.close()
