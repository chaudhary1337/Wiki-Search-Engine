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
        self.file_names = self.get_files()

    def get_files(self):
        file_names = []
        for path in os.scandir(self.path_to_inverted_index):
            # if a dir, skip
            if not path.is_file():
                continue

            # get the file name from the path
            file_name = path.name
            if not file_name.startswith("index"):
                continue

            file_names.append(f"{self.path_to_inverted_index}/{file_name}")

        return file_names

    def get_file_handlers(self):
        files = []
        for file_name in self.file_names:
            f = open(file_name, "r")
            files.append(FileHandler(f, file_name[len("index") :]))
        return files

    # REMOVES all the index files
    # since they are not needed after the merge
    def clean_index(self):
        for file_name in self.file_names:
            os.remove(file_name)

    def merge(self):
        files = self.get_file_handlers()
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

            f.write(token + " " + ";".join(all_data) + "\n")
            f.close()
