#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import json


auth = HTTPBasicAuth("simon.berthoud@swisstopo.ch", "XXXXXXX")
url = "https://jira-integration.beecollaboration.com"

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


all_issues = {}


page = 0
maxResults = 50
total = 1
while page < total:
    response = requests.get(url + '/rest/api/2/search?jql=project=BGDIDI_KB&startAt={}&maxResults={}'.format(page, maxResults), auth=("simon.berthoud@swisstopo.ch", "XXXXXXX"))
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
        name = response ['fields']['issuetype']['name']
        if name == 'BGDI Web publication' or name =='MGDI publication' or name == 'MGDI metadata and acceptance':
            issue = {}
            issue["id"] = response ['id' ]
            issue["key"] = response['key']
            issue["summary"] = response['fields']['summary']

            epic = {}
            epic["key"] = response['fields']['parent']['key']
            epic["id"] = response['fields']['parent']['id']
            epic["summary"] = response['fields']['parent']['fields']['summary']

            issue['epic'] = epic

        all_issues.append(issue)

    page += 1
    total = payload['total']

with open("mapping.json", 'w') as f:
    f.write(json.dumps(my_dict))


def create_epic(summary, description):      #We build the strcture of a dictionnary that contains the necessary fields to set an epic
    epic = {
        "fields": {
            "project": {
                "key": "BGDIDI_KB"
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name":"epic"               #add epic_name (customfield_10007)
            },
            "customfield_100006": "",
        }
    }

epics = {}
# {
#     "BGDIDI_KB-2417": { ... },
# }
for issue in payload['issues']:                   #We extract the values from bgdi main that we will use to build epic
    if name == 'BGDI main':
        if issue['customfield_100006'] == 'null':
            epic = create_epic(summary=issue['summary'], description=issue['description'])
            epics[issue['key']] = epic

with open('epics_to_create.json','w') as f:
    f.write(json.dumps(epics))


# len(key) == len(summary) == len(description)
for issue_key,epic in epics.items():          #At each iteration we create an epic by calling the function create_epic

    retour = requests.post(URL, data=epic)
    # retour contains info about epic id
    response = retour.json()

    # payload for assigning issues to epic
    payload = {
        "issues": [
            issue_key
        ]
    }
    requests.post(url + '/rest/agile/1.0/epic/{epicKey}/issue'.format(epicKey=response['key']), json=payload, auth=auth)

    return retour.json()


#Create an Epic:
#{"fields":{"project":{"key": "TEST"},"customfield_10401": "Epic Name 01","summary": "REST EXAMPLE1","description": "Creating an Epic via REST","issuetype": #{"name": "Epic"}}}

# customfield_10401 can be different on another JIRA installation.
# -> I think for our installation it's 'customfield_10007'



def assign_issue_to_epic(epic, issue):
   	issue['epic'] = epic['key']
    response = request.post(URL, json=issue, auth)
    if not response.stat
    return response.json()






