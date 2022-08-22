from misc import log

from heapq import heapify, heappush, heappop
import os


class FileHandler:
    def __init__(self, f, num):
        self.f = f
        self.num = num
        self.move_next()

    def __lt__(self, other):
        return (
            self.num < other.num
            if self.token == other.token
            else self.token < other.token
        )

    def move_next(self):
        line = self.f.readline()
        if line:
            self.token, self.data = line.split(";")

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

            # get the file name, open it
            # then create a file handler to be used in the heap
            file_name = path.name
            f = open(f"{self.path_to_inverted_index}/{file_name}", "r")
            files.append(FileHandler(f, file_name[len("index") :]))
        return files

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
            f = open(f"{self.path_to_inverted_index}/merged_{mini_token}.txt", "w+")

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

            f.write(token + ";" + " ".join(all_data))
            f.close()
