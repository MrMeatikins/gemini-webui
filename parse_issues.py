import json

states = {
    "ae56a905-81b7-4f9a-a2e5-7a842d66b8f4": "Done",
    "875ea790-38cf-4cbe-a2cc-9aecc7430d2a": "Cancelled",
    "31fb326d-3884-4405-8cd0-26ed5e96f4d1": "Backlog",
    "d142bbba-7042-4eab-88bc-88dea4f60ba9": "In Progress"
}

# Need to fetch the list of issues from the API
import urllib.request

url = "http://127.0.0.1:5000" # wait, I don't know the Plane API URL locally.
