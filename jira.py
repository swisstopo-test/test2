#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import urllib
import pprint
import dateutil.parser
import traceback


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

username = sys.argv[1]
password = sys.argv[2]

api = JiraApi(username, password)

# Basic flow for the migration:
# -----------------------------
# 1. search for all issues of type bgdi main
# 2. create an epic for each issue in the new project
# 3. create an issue with the content of bgdi main in the new project an associate it with the epic
# 4. create an issue in the new project for each subtask in the 'old' bgdi main ticket and associate it with the epic


# keep a reference to all bgdi main issue in BGDIDI
bgdi_main_issues = {}

# Helper functions
# ----------------------------------------------------------------------

# Helper function to create an issue structure
def create_issue(key, summary, description, component, labels=None):
    # """
    # {
    #     "fields": {
    #         "project": {
    #             "key": "BGDIINF_SB"
    #         },
    #         "summary": "make mf-geoadmin3.dev.bgdi.ch dev again",
    #         "description": "Not sure if there's already an issue for this, if yes please close this one.\r\nIf you open https://mf-geoadmin3.dev.bgdi.ch/ without additional params, backend services (catalog, identify, layer config etc) from prod environment are used.\r\nThis is misleading and confusing and makes the dev environment useless.\r\nplease change the default service source to dev root urls:\r\n```\r\nhttps://mf-chsdi3.dev.bgdi.ch/\r\n```",
    #         "issuetype": {
    #             "name": "Task"
    #         }
    #     }
    # }
    # """
    # If no labels are provided, just create an empty list
    if labels is None:
        labels = []

    issue = {
        'fields': {
            "project": {
                "key": "BGDIDIC"
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": "Task"
            },
            "labels": labels,
            "components": [{"name":component}]
        },
       #  "update":{
       #    "issuelinks":[
       #       {
       #          "add":{
       #             "type":{
       #                "name":"Clones",
       #                "inward":"is cloned by",
       #                "outward":"clones"
       #             },
       #             "outwardIssue":{
       #                "key":key
       #             }
       #          }
       #       }
       #    ]
       # }
    }
    return issue
    

# Helper function to create an epic structure
def create_epic(summary, description, labels=None):      #We build the strcture of a dictionnary that contains the necessary fields to set an epic
    # If no labels are provided, just create an empty list
    if labels is None:
        labels = []

    epic = {
        "fields": {
            "project": {
                "key": "BGDIDIC"
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": "Epic"
            },
            # The customfield_10007 is the name of the epic
            # Note: since we don't have a special epic name, we just use the
            # title (i.e. the summary)
            "customfield_10007": summary,
            "labels": labels
        }
    }
    return epic


def create_comment(author, body):
    return {
        "author" : {
            "name": author
        },
        "body": body
    }


# Save all stuff that needs to be created, epics
# along with a list of issues that belong to the epic
epics = {}
# {
#     "BGDIDI_KB-2417": {
#         "content": { ... },
#         "issues": {}
# }



# Step 1
# --------

# init values for paginated calls
page = 0
maxResults = 50
total = 1

while page < total:
    response = api.get(uri=api.format_search_query('project=BGDIDI_KB') + '&startAt={}&maxResults={}'.format(page, maxResults))


    # in case sth unexpected happenend
    # we print the text to get some hints why it failed
    if response.status_code != 200:
        print(response.text)

    payload = response.json()
    # payload
    # {
    #   "expand": "schema,names",
    #   "startAt": 0,
    #   "maxResults": 50,
    #   "total": 6,
    #   "issues": [
    #      {...}

    for issue in payload['issues']:
        try:
            # print(issue)
            # name of the issuetype
            issuetype = issue['fields']['issuetype']['name']
            
            # we look for issues of type subtask
            if issuetype == 'BGDI Web publication' or issuetype =='MGDI publication' or issuetype == 'MGDI metadata and acceptance':
                # check if a new epic for the parent was already
                # added to 'epics' data structure
                parent_key = issue['fields']['parent']['key']
                if parent_key not in epics:

                    # in order to get all information about the issue,
                    # we have to make a second call
                    response = api.get(url=issue['fields']['parent']['self'])
                    parent = response.json()
                    fields = parent['fields']
                    

                    # create the content for the epic
                    epics[parent_key] = {}
                    epics[parent_key]['content'] = create_epic(
                        summary=parent['fields']['summary'],
                        description=parent['fields']['description'],
                        labels=parent['fields']['labels']
                    )

                    # create the content for the GDWH (former bgdi main) issue

                    # We add some information that was in customfields to the description
                    gdwh_description = parent['fields']['description'] or ''
                    gdwh_description += f"\n------------------------\n"
                    gdwh_description += f"__Status: {parent['fields']['status']['name']}\n"
                    gdwh_description += f"__MuM_GDS_link: {parent['fields']['customfield_10505']}\n"
                    gdwh_description += f"__Original_Data_Path: {parent['fields']['customfield_10606']}\n"
                    
                    comments = []
                    if 'comment' in parent['fields'] and parent['fields']['comment']['comments']:
                        for _comment in parent['fields']['comment']['comments']:
                            created = dateutil.parser.parse(_comment['created'])
                            comment_date = created.strftime('%d %b %Y at %H:%M')
                            body = f"_{_comment['author']['displayName']} commented on {comment_date}:_\n\n"
                            body += _comment['body']
                            comments.append({"body": body})


                    gdwh_issue = create_issue(
                        key=parent_key,
                        summary="[GDWH] " + parent['fields']['summary'],
                        description=gdwh_description,
                        component='GDWH',
                        labels=parent['fields']['labels']
                    )
                    
                    epics[parent_key]['issues'] = {}
                    epics[parent_key]['issues'][parent_key] = {}
                    epics[parent_key]['issues'][parent_key]['issue'] = gdwh_issue
                    epics[parent_key]['issues'][parent_key]['comments'] = comments


                # create content for 'BGDI web publication'/'MGDI publication'/'MGDI metadata and acceptance'
                description = issue['fields']['description'] or ''
                if issuetype == 'BGDI Web publication':
                    description += f"\n------------------------\n"
                    description += f"__Status: {issue['fields']['status']['name']}\n"
                    if 'customfield_10501' in issue['fields'] and 'value' in issue['fields']['customfield_10501']:
                        description += f"__Category: {issue['fields']['customfield_10501']['value']}\n"
                    description += f"__MuM_PubL_link: {issue['fields']['customfield_10506']}\n"
                    description += f"__GDWH_export_link: {issue['fields']['customfield_10503']}\n"
                    description += f"__Testlink_viewer: {issue['fields']['customfield_10507']}\n"
                    component = 'WEB'
                else:
                    component = 'MGDI'
                subtask = create_issue(
                        key=issue['key'],
                        summary="[WEB] " + issue['fields']['summary'],
                        description=description,
                        component=component,
                        labels=issue['fields']['labels']
                )

                # for the comments we need to make another call
                resp = api.get(url=issue['self'])
                issue = resp.json()
                # pprint.pprint(issue)
                comments = []
                if 'comment' in issue['fields'] and issue['fields']['comment']['comments']:
                    for _comment in issue['fields']['comment']['comments']:
                        created = dateutil.parser.parse(_comment['created'])
                        comment_date = created.strftime('%d %b %Y at %H:%M')
                        body = f"_{_comment['author']['displayName']} commented on {comment_date}:_\n\n"
                        body += _comment['body']
                        comments.append({"body": body})

                # add to the list of tasks that will belong to the epic
                epics[parent_key]['issues'][issue['key']] = {}
                epics[parent_key]['issues'][issue['key']]['issue'] = subtask
                epics[parent_key]['issues'][issue['key']]['comments'] = comments

        except Exception as e:
            pprint.pprint(issue)
            traceback.print_exc()
            print(e)

    # increase page index by one
    page += 1

    # Disabled until we wanna process everything
    total = payload['total']


# Save all stuff that needs to be created to file
with open('epics_to_create.json','w') as f:
    f.write(json.dumps(epics, indent=4))



