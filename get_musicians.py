#!/usr/bin/env python
# Description: Script to get the list of all musicians distributed by genre
__author__ = 'ignacioelola'

import csv
import chain_extractors


def save_data(filename, results):
    for result in results:
        genre = result.get("url/_text")
        if genre:
            genre = genre.replace("List of ", "").encode("utf-8")
        for result_level_2 in result["results"]:
            musician = result_level_2.get("musician")
            if musician:
                musician = musician.encode("utf-8")
            new_row = [genre, musician]

            with open(filename, "a") as infile:
                writer = csv.writer(infile)
                writer.writerow(new_row)


if __name__ == '__main__':

    guids_level_1 = ["0a7ccd62-377f-4b94-aca0-c74a78984b6b",
                     "68f6efda-85f3-41f7-b252-77e1aadb7c3c",
                     "ff4c3352-0ba6-4428-8ec3-9c5b00d58aa8"]

    guid_level_2 = "bf973c4e-3914-4fc8-a7a1-68be11dea7a8"

    source_url = "http://en.wikipedia.org/wiki/Category:Lists_of_musicians_by_genre"

    output_filename = "data/musicians.csv"
    with open(filename, "w") as infile:
        writer = csv.writer(infile)
        writer.writerow(["genre", "musician"])

    for guid_level_1 in guids_level_1:
        # Get list of musicians by genre
        chain_apis_results = chain_extractors.get_data(guid_level_1, guid_level_2, source_url)
        save_data(output_filename, chain_apis_results)

        # WARNING: I think some lists might require a different level 2 guid
