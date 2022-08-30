from os.path import exists

from help import (
    BONUS,
    BONUS_DEFAULT,
    BONUS_MISMATCH,
    RFIELDS,
    FIELDS,
    DUMP_LIMIT,
    dec,
)


class Parse:
    # aka Majdoori
    def __init__(self, path_to_inverted_index):
        self.path_to_inverted_index = path_to_inverted_index

    def get_token_pages(self, token):
        """
        does a linear search on the appropriate merged file
        using the mini_token (first 3 characters)

        returns a list of page info of the form
        ["page_id:tf1fid1tf2fid2", "page_id2:tffid"]
        which has been split by a ;
        """
        data = ""

        mini_token = token[:3]
        path = f"{self.path_to_inverted_index}/merged_{mini_token}.txt"

        if not exists(path):
            return []

        with open(path, "r") as f:
            while line := f.readline():
                if not line.startswith(token):
                    continue
                token, data = line.split()
                break

        return data.split(";")

    def get_tf(self, field_data, i):
        """
        returns the final index i
        and the decoded buffer, which is the tf

        NOTE: here we use RFIELDS since we want to look at the actual data
        (the dump format)
        """
        buffer = []
        while i < len(field_data) and field_data[i] not in RFIELDS:
            buffer.append(field_data[i])
            i += 1

        # if the buffer is empty, then assume value 1
        return i, dec("".join(buffer)) if buffer else 1

    def get_bonus(self, field_data, i, field):
        """
        NOTE: here we use FIELDS since we want to look at human readable format
        """
        if field == "":
            return BONUS_DEFAULT
        elif field_data[i] != FIELDS[field]:
            return BONUS_MISMATCH
        else:
            return BONUS

    def get_tf_bonus(self, field_data, i, field):
        return *self.get_tf(field_data, i), self.get_bonus(field_data, i, field)

    def get_titles(self, topk):
        titles = []
        for page_id, score in topk:
            save_counter, line_number = divmod(page_id, DUMP_LIMIT)

            # NOTE: THIS REMAINS THE ONLY MAJOR ISSUE IN MY CODE
            # IT WORKS, BUT I DO NOT KNOW WHY.
            if save_counter != 0:
                line_number -= 1

            # try opening the file if possible
            path = f"{self.path_to_inverted_index}/title{save_counter}.txt"
            if not exists(path):
                continue

            # open the file and read the specified line number
            with open(path, "r") as f:
                lines = f.readlines()
                title = lines[line_number].strip()
                titles.append((score, f"{page_id}, {title}"))

        titles.extend([(-1, "-1, ''")] * (10 - len(titles)))
        return titles
