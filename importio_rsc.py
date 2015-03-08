#!/usr/bin/env python
# description: Resources to use the importio platform
__author__ = 'ignacioelola'

import requests
import json
import time
import urllib
import sys
import os
import inspect
import logging
import importio
import latch


# Function to read your credentials.
# Credentials need to be in a JSON file called auth_credentials.json
#  in the format:
# {
# "userGuid": YOUR-USER-GUID,
# "apiKey": YOUR-API-KEY
# }
def read_credentials():
    with open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/auth_credentials.json",
              "r") as infile:
        auth_credentials = json.load(infile)
    return auth_credentials


# Function to query the REST API
def query_api(query,
              api_guid,
              page=None,
              endpoint="http://api.import.io/store/connector/"):

    auth_credentials = read_credentials()

    timeout = 5

    full_url = endpoint + api_guid + "/_query?_user=" + auth_credentials["userGuid"] + "&_apikey=" + urllib.quote_plus(
                auth_credentials["apiKey"])
    if page:
        query["page"] = page

    try:
        r = requests.post( full_url,
            data=json.dumps(query), timeout=timeout)
        rok = r.ok
        rstatus_code = r.status_code
        rtext = r.text
    except:
        rok = False
        rstatus_code = 000
        rtext = "exception"

    if rok is True and rstatus_code == 200 and "errorType" not in r.json():
        results = r.json()
        return results
    else:
        print "Error %s, %s on page %s , Retrying now (1)..." % (rstatus_code, rtext, query["input"]["webpage/url"])
        sys.stdout.flush()
        time.sleep(2.5)

        try:
            r = requests.post(full_url,
                data=json.dumps(query), timeout=timeout)
            rok = r.ok
            rstatus_code = r.status_code
            rtext = r.text

        except:
            rok = False
            rstatus_code = 000
            rtext = "exception"

        if rok is True and rstatus_code == 200 and "errorType" not in r.json():
            results = r.json()
            return results
        else:
            print "Error %s, %s on page %s , Could not complete the query" % (rstatus_code, rtext, query["input"]["webpage/url"])
            sys.stdout.flush()
            try:
                error = json.loads(r.content)["error"]
            except:
                try:
                    error = r.status_code
                except:
                    error = "0"
            return {}

def query_api_comet(query, api_guid):

    # To use an API key for authentication, use the following code:
    auth_credentials = read_credentials()
    client = importio.importio(user_id=auth_credentials["userGuid"], api_key=auth_credentials["apiKey"], host="https://query.import.io")

    # Once we have started the client and authenticated, we need to connect it to the server:
    client.connect()

    # Because import.io queries are asynchronous, for this simple script we will use a "latch"
    # to stop the script from exiting before all of our queries are returned
    # For more information on the latch class, see the latch.py file included in this client library
    global queryLatch
    queryLatch = latch.latch(1)

    # Define here a global variable that we can put all our results in to when they come back from
    # the server, so we can use the data later on in the script
    global dataRows
    dataRows = []

    # Issue queries to your data sources and with your inputs
    # You can modify the inputs and connectorGuids so as to query your own sources
    # Query for tile setlist.fm connector
    client.query({
      "connectorGuids": [
        api_guid
      ],
      "input": query["input"]
    }, callback)


    print "Queries dispatched, now waiting for results"

    # Now we have issued all of the queries, we can "await" on the latch so that we know when it is all done
    queryLatch.await()

    print "Latch has completed, all results returned"

    # It is best practice to disconnect when you are finished sending queries and getting data - it allows us to
    # clean up resources on the client and the server
    client.disconnect()

    # Now we can print out the data we got
    return dataRows

# In order to receive the data from the queries we issue, we need to define a callback method
# This method will receive each message that comes back from the queries, and we can take that
# data and store it for use in our app
def callback(query, message):
  global dataRows
  
  # Disconnect messages happen if we disconnect the client library while a query is in progress
  if message["type"] == "DISCONNECT":
    print "Query in progress when library disconnected"
    # print json.dumps(message["data"], indent = 4)

  # Check the message we receive actually has some data in it
  if message["type"] == "MESSAGE":
    if "errorType" in message["data"]:
      # In this case, we received a message, but it was an error from the external service
      print "Got an error!" 
      # print json.dumps(message["data"], indent = 4)
    else:
      # We got a message and it was not an error, so we can process the data
      # print "Got data!"
      # print json.dumps(message["data"], indent = 4)
      # Save the data we got in our dataRows variable for later
      dataRows.extend(message["data"]["results"])
  
  # When the query is finished, countdown the latch so the program can continue when everything is done
  if query.finished(): queryLatch.countdown()