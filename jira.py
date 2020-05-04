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
            verify=False
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
def create_issue(summary, description, labels=None):
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
            "labels": labels
        }
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


# Save all stuff that needs to be created, epics
# along with a list of issues that belong to the epic
epics = {}
# {
#     "BGDIDI_KB-2417": {
#         "content": { ... },
#         "issues": []
# }



# Step 1
# --------

# init values for paginated calls
page = 0
maxResults = 1
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
        # print(issue)
        # name of the issuetype
        name = issue['fields']['issuetype']['name']
        
        # we look for issues of type subtask
        if name == 'BGDI Web publication' or name =='MGDI publication' or name == 'MGDI metadata and acceptance':
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
                gdwh_description = parent['fields']['description']
                gdwh_description += f"\n------------------------\n"
                gdwh_description += f"__Status: {parent['fields']['status']['name']}\n"
                gdwh_description += f"__MuM_GDS_link: {parent['fields']['customfield_10505']}\n"
                gdwh_description += f"__Original_Data_Path: {parent['fields']['customfield_10606']}\n"
                
                gdwh_issue = create_issue(
                    summary="[GDWH] " + parent['fields']['summary'],
                    description=gdwh_description,
                    labels=parent['fields']['labels']
                )
                
                epics[parent_key]['issues'] = []
                epics[parent_key]['issues'].append(gdwh_issue)

            # create content for 'BGDI web publication'/'MGDI publication'/'MGDI metadata and acceptance'
            # ---------------------------------------
            # 
            #       TODO
            # 
            # 
            # ----------------------------------------


    # increase page index by one
    page += 1

    # Disabled until we wanna process everything
    # total = payload['total']


# Save all stuff that needs to be created to file
with open('epics_to_create.json','w') as f:
    f.write(json.dumps(epics, indent=4))


# We quit here
sys.exit(1)
# =========================================================================================================================================================

for issue in payload['issues']:                   #We extract the values from bgdi main that we will use to build epic
    if name == 'BGDI main':
        if issue['customfield_100006'] == 'null':
            epic = create_epic(summary=issue['summary'], description=issue['description'])
            epics[issue['key']] = epic



key = "BGDIDI_KB-2427"   #exemple de clé pour une issue (ici intégration). On va aller cherche les projets main puis ensuite les sous-tâches associés (subtask)

liste = [2400, 2500]

my_dict = {}

#   "BGDIDI_KB-2455": {
#      "key": "BGDIDI_KB-2455",
#      "id": "43921",
#      "summary": "ch.bafu.erosion-gruenland_bodenabtrag_feb"
#      "epic": {
#          "epic": "BGDIDI_KB-2417",
#          "id": "42542",
#          "summary": "Monatliche Erosionsrisikokarten des Schweizer Dauergrünland BAFU",
#      }
#   }





with open("mapping.json", 'w') as f:
    f.write(json.dumps(my_dict))



# len(key) == len(summary) == len(description)
for issue_key,epic in epics.items():          #At each iteration we create an epic by calling the function create_epic
    print(epic)
    #retour = requests.post(URL, data=epic)

    # retour contains info about epic id
    response = retour.json()

    # payload for assigning issues to epic
    payload = {
        "issues": [
            issue_key
        ]
    }
    print(payload)
    # requests.post(url + '/rest/agile/1.0/epic/{epicKey}/issue'.format(epicKey=response['key']), json=payload, auth=auth)

    #return retour.json()


#Create an Epic:
#{"fields":{"project":{"key": "TEST"},"customfield_10401": "Epic Name 01","summary": "REST EXAMPLE1","description": "Creating an Epic via REST","issuetype": #{"name": "Epic"}}}

# customfield_10401 can be different on another JIRA installation.
# -> I think for our installation it's 'customfield_10007'


# =========================================================================================================================================================
#We extract the values from BGDI Web publication, MGDI publication and MGDI metadata and acceptance that we will use to build tasks


for issue in payload['issues']:
    if name == 'BGDI Web publication' or name =='MGDI publication' or name == 'MGDI metadata and acceptance':
#        if issue['customfield_100006'] == 'null':
            task = create_issue(summary=issue['summary'], description=issue['description'])
            task[issue['key']] = task






def assign_issue_to_epic(epic, issue):
    issue['epic'] = epic['key']
    response = request.post(URL, json=issue, auth=auth)
    if not response.status_code == 200:
        print("Error",response.text)
    return response.json()






