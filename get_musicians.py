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
        with open(self.filename, "w") as infile:
            writer = csv.writer(infile)
            writer.writerow(["genre", "musician"])

    def save_result(self, result):

        genre = result.get("url/_text")
        if genre:
            genre = genre.replace("List of ", "").replace(" artists", "").replace(" musicians", "").encode("utf-8")
        for result_level_2 in result["results"]:
            musician = result_level_2.get("musician/_text")
            if musician:
                if isinstance(musician, list):
                    musician = musician[0].encode("utf-8")
                else:
                    musician = musician.encode("utf-8")

                if "List of" in musician:
                    # Third layer works poorly atm
                    new_url = result_level_2.get("musician")
                    new_query = {"input": {"webpage/url": new_url}}
                    new_response = importio_rsc.query_api(new_query, "bf973c4e-3914-4fc8-a7a1-68be11dea7a8")

                    for new_result in new_response["results"]:
                        musician = result_level_2.get("musician/_text")
                        if musician:
                            if isinstance(musician, list):
                                musician = musician[0].encode("utf-8")
                            else:
                                musician = musician.encode("utf-8")
                            new_row = [genre, musician]

                            with open(self.filename, "a") as infile:
                                writer = csv.writer(infile)
                                writer.writerow(new_row)
                else:

                    new_row = [genre, musician]

                    with open(self.filename, "a") as infile:
                        writer = csv.writer(infile)
                        writer.writerow(new_row)


def main():
    guid_level_1 = "0a7ccd62-377f-4b94-aca0-c74a78984b6b"
    guid_level_2 = "bf973c4e-3914-4fc8-a7a1-68be11dea7a8"

    source_url = "http://en.wikipedia.org/wiki/Category:Lists_of_musicians_by_genre"

    output_filename = "data/musicians.csv"

    data_savior = SaveData()
    data_savior.initialize_files(output_filename)

    # Get list of musicians by genre
    chain_apis_results = chain_apis.get_data(guid_level_1, guid_level_2, source_url, data_savior)


if __name__ == '__main__':

    main()
