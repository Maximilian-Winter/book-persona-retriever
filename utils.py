import csv
import os
from collections import Counter
from os.path import join

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
RANK_DATASET_DIR = join(PROJECT_DIR, "data/hla_books")
CACHE_DIR = join(PROJECT_DIR, "./.cache")


def cat_files(source_filepaths, target_filepath):
    assert(isinstance(source_filepaths, list))

    with open(target_filepath, 'w') as outfile:
        for filename in source_filepaths:
            with open(filename) as infile:
                for line in infile:
                    outfile.write(line)


def range_middle(n):
    return [round(n/2)]


def range_exclude_middle(n):
    middle = range_middle(n)[0]
    return [i for i in range(n) if i != middle]


class TextService:

    @staticmethod
    def write(target, lines_it):
        counter = Counter()
        with open(target, "w") as o:
            for line in lines_it:
                o.write(line + "\n")
                counter["total"] += 1

        print("Saved: {}".format(target))
        print("Rows written: {}".format(counter["total"]))


class CsvService:

    @staticmethod
    def write(target, lines_it, header=None, notify=True):
        assert(isinstance(header, list) or header is None)

        counter = Counter()
        with open(target, "w") as f:
            w = csv.writer(f, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if header is not None:
                w.writerow(header)

            for content in lines_it:
                w.writerow(content)
                counter["written"] += 1

        if notify:
            print(f"Saved: {target}")
            print("Total rows: {}".format(counter["written"]))

    @staticmethod
    def read(target, delimiter='\t', quotechar='"', skip_header=False):
        with open(target, newline='\n') as f:
            for i, row in enumerate(csv.reader(f, delimiter=delimiter, quotechar=quotechar)):
                if skip_header and i == 0:
                    continue
                yield row
