#!/usr/bin/env python
# Description: Script to get data using 2 extractor
# First extractor give urls as output, than are then
# used as input in the second extractor
__author__ = 'ignacioelola'

import importio_rsc


def get_data(guid_level_1, guid_level_2, start_url):

    query_level_1 = {"input": {"webpage/url": start_url}}

    response_level_1 = importio_rsc.query_api(query_level_1, guid_level_1)

    all_results = []
    for result in response_level_1["results"]:
        source_url_level_2 = result["url"]
        print "Querying %s" % source_url_level_2
        query_level_2 = {"input": {"webpage/url": source_url_level_2}}
        response_level_2 = importio_rsc.query_api(query_level_2, guid_level_2)

        results_level_2 = response_level_2.get("results")

        all_results.append({"url": source_url_level_2,
                            "url/_text": result["url/_text"],
                            "results": results_level_2})

    return all_results