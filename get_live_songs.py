#!/usr/bin/env python
# Description: Script to get the list of all musicians distributed by genre
__author__ = 'ignacioelola'

import csv
import chain_apis
import importio_rsc


class SaveData():

    def __init__(self):
        self.filename = None

        self.mp = None
        self.url = None

    def initialize_files(self, file1):

        self.filename = file1

        # Write headers in the files (as well as blank them if they exist)
        # with open(self.filename, "w") as infile:
        #     writer = csv.writer(infile)
        #     writer.writerow(["musician", "show", "year", "song"])

    def save_result(self, result):

        if result.get("results"):
            show = result.get("url/_text").encode("utf-8")
            url_split = result.get("url").split("/")
            year = url_split[-2].encode("utf-8")

            for result_level2 in result.get("results"):
                song = result_level2.get("songs").encode("utf-8")
                new_row = [musician, show, year, song]
                with open(self.filename, "a") as infile:
                    writer = csv.writer(infile)
                    writer.writerow(new_row)

def get_inputs(infile):

    inputs = []
    with open(infile, "r") as f:
        reader = csv.reader(f)
        for row_count, row in enumerate(reader):
            if row_count > 505:
                if "list of" not in row[1].lower() and "lists of" not in row[1].lower():
                    inputs.append(row[1])
    clean_inputs = set(inputs)
    return inputs



def main():
    global musician

    guid_level_1 = "5d52fe9d-6dc5-4a56-b6cb-a0e5e65042c2"
    guid_level_2 = "b1a10a4c-2be2-4266-a145-25ae51730627"

    output_filename = "data/live_songs.csv"

    list_inputs = get_inputs("data/musicians.csv")

    data_savior = SaveData()
    data_savior.initialize_files(output_filename)

    # Get list of musicians by genre
    for musician in list_inputs:
        chain_apis_results = chain_apis.get_data(guid_level_1, guid_level_2, musician, data_savior, "musician", api_type="comet")


if __name__ == '__main__':

    main()
