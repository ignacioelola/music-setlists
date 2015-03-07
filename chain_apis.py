#!/usr/bin/env python
# Description: Script to get data using 2 extractor
# First extractor give urls as output, than are then
# used as input in the second extractor
__author__ = 'ignacioelola'

import importio_rsc


def get_data(guid_level_1, guid_level_2, first_input, save_data_class=None, first_input_name="webpage/url", pages=None, api_type="rest"):

    query_level_1 = {"input": {first_input_name: first_input}}

    if api_type == "rest":
        if pages:
            for page in range (1,pages):
                print "Page %s" % page
                response_level_1 = importio_rsc.query_api(query_level_1, guid_level_1, page)
                get_data_level_2(response_level_1, save_data_class, guid_level_2)            
        else:
            response_level_1 = importio_rsc.query_api(query_level_1, guid_level_1)
            get_data_level_2(response_level_1, save_data_class, guid_level_2)
    elif api_type == "comet":
        response_level_1 = importio_rsc.query_api_comet(query_level_1, guid_level_1)
        response_level_1 = {"results":response_level_1}
        get_data_level_2(response_level_1, save_data_class, guid_level_2)
    else:
        print "Wrong api type"


def get_data_level_2(response_level_1, save_data_class, guid_level_2):
    all_results = []
    for result in response_level_1["results"]:
        source_url_level_2 = result["url"]
        print "Querying %s" % source_url_level_2
        query_level_2 = {"input": {"webpage/url": source_url_level_2}}
        response_level_2 = importio_rsc.query_api(query_level_2, guid_level_2)

        results_level_2 = response_level_2.get("results")

        if save_data_class:
            save_data_class.save_result({"url": source_url_level_2,
                                         "url/_text": result["url/_text"],
                                         "results": results_level_2})
        else:
            all_results.append({"url": source_url_level_2,
                                "url/_text": result["url/_text"],
                                "results": results_level_2})

    if not save_data_class:
        return all_results