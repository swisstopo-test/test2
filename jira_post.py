#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import urllib
import pprint

class JiraApi:

    def __init__(self, username, password):
        self.host_url = "https://jira-integration.beecollaboration.com"
        self.auth = HTTPBasicAuth(username, password)

    # helper function to format search query
    def format_search_query(self, search_query):
        # search query is a string exactly as it would be entered in the 
        # jira gui issue search
        encoded_query = urllib.parse.quote(search_query)
        return f"/rest/api/2/search?jql={encoded_query}"


    def get(self, url=None, uri=None):
        # jira api requires that the content-type header is set
        headers = {'content-type': 'application/json'}
        if uri is not None:
            url = self.host_url + uri
        response = requests.get(
            url,
            auth=self.auth, 
            headers=headers,
            verify=True
        )
        return response

    def post(self, url=None, uri=None, payload=None):
        # jira api requires that the content-type header is set
        headers = {'content-type': 'application/json'}
        if uri is not None:
            url = self.host_url + uri
        response = requests.post(
            url,
            json=payload,
            auth=self.auth, 
            headers=headers,
            verify=True
        )
        return response

username = sys.argv[1]
password = sys.argv[2]

api = JiraApi(username, password)

def create_issue_link(from_key, to_key):
    return {
        "outwardIssue": {
            "key": to_key
        },
        "inwardIssue": {
            "key": from_key
        },
        "type": {
            "id": "10001"
        }
    }

with open('epics_to_create.json', 'r') as f:
    epics = json.loads(f.read())

count = 0
for key, epic in epics.items():
    if count > 0:
        break
    resp = api.post(uri='/rest/api/2/issue', payload=epic['content'])
    new_epic_key = resp.json()['key']
    new_issue_keys = []
    for old_key, issue_and_comment in epic['issues'].items():
        # create issue
        issue = issue_and_comment['issue']
        resp = api.post(uri='/rest/api/2/issue', payload=issue)
        print(resp.text)
        new_issue = resp.json()
        new_issue_key = new_issue['key']
        

        # create issue link
        issuelink = create_issue_link(new_issue_key, old_key)
        resp = api.post(uri='/rest/api/2/issueLink', payload=issuelink)

        new_issue_keys.append(new_issue_key)

        # create issue comments
        for comment in issue_and_comment['comments']:
            resp = api.post(url=new_issue['self'] + '/comment', payload=comment)


    if new_issue_keys:
        print(new_issue_keys)
        resp = api.post(uri=f'/rest/agile/1.0/epic/{new_epic_key}/issue', payload={'issues':new_issue_keys})
        print(resp.text)