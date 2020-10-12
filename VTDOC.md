<!-- Output copied to clipboard! -->


<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 4; WARNINGs: 1; ALERTS: 13.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>
<a href="#gdcalert2">alert2</a>
<a href="#gdcalert3">alert3</a>
<a href="#gdcalert4">alert4</a>
<a href="#gdcalert5">alert5</a>
<a href="#gdcalert6">alert6</a>
<a href="#gdcalert7">alert7</a>
<a href="#gdcalert8">alert8</a>
<a href="#gdcalert9">alert9</a>
<a href="#gdcalert10">alert10</a>
<a href="#gdcalert11">alert11</a>
<a href="#gdcalert12">alert12</a>
<a href="#gdcalert13">alert13</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>



# Vector Tile Pipeline Installation Protocol


## _swisstopo Vector Tile Pipeline_


##  \
Client: Federal Office of Topography, swisstopo

This document is available online at:

[https://docs.google.com/document/d/1-uTQtYwqaO8S0AiJMxX3y5h1Sc4fEqpT_KzuqqN45r8/edit?usp=sharing](https://docs.google.com/document/d/1-uTQtYwqaO8S0AiJMxX3y5h1Sc4fEqpT_KzuqqN45r8/edit?usp=sharing)

Customer tickets: [https://github.com/geoadmin/config-vt-schema-lbm/issues](https://github.com/geoadmin/config-vt-schema-lbm/issues)

Authors: Adam Laza; Luis Suter

** \
**COSIG_19_26 \
 \
Copyright © 2020 MapTiler AG. All rights reserved.

[https://www.maptiler.com/](https://www.maptiler.com/)


# Table of Contents


[TOC]



# Introduction {#introduction}

The purpose of this document is to document the steps of the swisstopo Vector Tiles Pipeline, developed by MapTiler for the Federal Office of Topography (swisstopo). This manual provides:



*   An overview of the infrastructure, and overviews of the steps taken in the cartography process and steps for creating PROD tiles,
*   Step-by-Step instructions on Server installation,
*   Github actions to run the Vector Tiles pipeline,
*   Vector Tile database preparation (including manual imports of data), 
*   References to the feature layer work of swisstopo cartographers, 
*   The functions used to generate the vector tiles, 
*   The instructions on how to load these tiles into the Cloud, and
*   How to make copies of the tiles within the Cloud.


# 


# Overviews {#overviews}


## Infrastructure Overview and Links {#infrastructure-overview-and-links}

The first image shows the setup of the Virtual EC2 machine, including the connections between postgres databases and APACHE server, with links to relevant pieces below


# 

<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")


SwissTopo VT Pipeline:



*   [https://swisstopo.maptiler.ch](https://swisstopo.maptiler.ch/)

SwissTopo DEV inspect:



*   [https://swisstopo.maptiler.ch/tileset/dev](https://swisstopo.maptiler.ch/tileset/dev)

SwissTopo DEV tilejson:



*   [https://swisstopo.maptiler.ch/api/tilejson/dev](https://swisstopo.maptiler.ch/api/tilejson/dev)

SwissTopo PROD inspect:



*   [https://swisstopo.maptiler.ch/tileset/prod](https://swisstopo.maptiler.ch/tileset/prod)

SwissTopo PROD tilejson:



*   [https://swisstopo.maptiler.ch/api/tilejson/prod](https://swisstopo.maptiler.ch/api/tilejson/prod)

PgAdmin:



*   [https://swisstopo.maptiler.ch/pgadmin4](https://swisstopo.maptiler.ch/pgadmin4)

DEV schema docs:



*   [https://geoadmin.github.io/config-vt-schema-lbm/](https://geoadmin.github.io/config-vt-schema-lbm/)

MapTiler Server admin:



*   [https://swisstopo.maptiler.ch/admin](https://swisstopo.maptiler.ch/admin)

This image provides an overview of the technical infrastructure composing the Vector Tiles pipeline, including the connections between existing BGDI databases, the virtual machine setup, the GitHub repository, local machines, and MapTiler Cloud.



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")



## Overview of cartographer process {#overview-of-cartographer-process}



1. Make any change into *.sql or *.yaml file to modify data visualization, generalization or any other change. You can modify it either locally in your cloned repository or do it directly in the GitHub editor on the web.
2. Promote your changes as a pull request to the master branch. It triggers _SwissTopo CI generate reports _workflow. A new branch is created for your pull request and statistics about tile size and tile speed generation are created and added to your pull request as a comment. It takes about half an hour.(Purple arrows in the schema.)
3. Inspect the statistic and see how your modifications have affected the tiles. After that you can either:
    1. Do another modification and commit it into the pull request. The statistics will be re-recreated.
    2. Merge your pull request into master branch. It takes about half an hour. It triggers _SwissTopo CI - import sql_ workflow. (Orange arrow in the schema). 
4. Check the live-preview of master branch at: [https://swisstopo.maptiler.ch/tileset/dev](https://swisstopo.maptiler.ch/tileset/dev).
5. Create a release of tiles on GitHub webpage. (Green arrows in schema.) Generated tiles will be uploaded as release artefacts and also uploaded to SwissTopo account at MapTiler cloud.


## Overview of PROD tiles creation process {#overview-of-prod-tiles-creation-process}



1. (optional) Make sure your data in the PROD database are up to date. Run Import data workflow from GitHub and choose the PROD branch. Or run re-import of data locally as described in [Manual steps for Database Preparation](#manual-steps-for-database-preparation). Re-import of data takes about two hours.
2. Merge master branch into PROD branch. It triggers _SwissTopo CI - import sql_ workflow. Or you can run import of sql locally as described in 

<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Work on Layers/Import of sql"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Work on Layers/Import of sql](#heading=h.43ls5cxkfbrh)
3. Create a new release over the PROD branch. It triggers _SwissTopo CI - generate mbtiles_ workflow. Or you can generate tiles locally as described in 

<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "Generate Vector Tiles"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[Generate Vector Tiles](#heading=h.vwkxg5vd8mt2).
4. If you have used GitHub Action, MBTiles will be uploaded to MapTiler Cloud and to the release at GitHub. 
5. (optional) If you want to upload the mbtiles to S3 bucket you have to do it manually as described in 

<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "CloudPush"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[CloudPush](#heading=h.d9a03kiktrm7) and 

<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: undefined internal link (link text: "AWS CLI"). Did you generate a TOC? </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

[AWS CLI](#heading=h.mc84t8pt3a78).


# 


# Server Installation step-by-step {#server-installation-step-by-step}

This section describes the configuration of the server and actions taken to set up the server for hosting swisstopo vector tiles.


## Host machine

The VT-pipeline was tested on Ubuntu 20.04 and Debian 10 systems. On these systems it should run without any problem. We know there are issues running it on Amazon Linux but no further research was made.


## EC2 machine {#ec2-machine}

MapTiler was provided access to a swissTopo AWS account (see [#6](https://github.com/geoadmin/config-vt-schema-lbm/issues/6)).

_The instance type of the EC2 machine used for testing was a General Purpose m5ad.4xlarge, with the following configuration: _



*   vCPUs: 16
*   Memory (GiB): 64 GiB
*   Instance Storage(GB): 2x300 (SSD)
*   Network Performance: Up to 10 Gigabit
*   OS: Debian 10 Buster 64-bit (x86)
*   AMI: debian-10-amd64-daily-20200512-261 (community AMI)

_The instance launched were always with the following configuration: _



*   Region: eu-central-1
*   Network: main
*   Subnet: Public Subnet in AZ a
*   Auto-assing Public IP: Use subnet setting (Enable)
*   Existing security group: maptiler


## GitHub Personal Access Token (PAT) {#github-personal-access-token-pat}

To eventually run GitHub Actions on a self-hosted runner a Personal Access Token (PAT) is required. The PAT is always linked to a developer account. 

To generate a PAT, go to Personal Account/Settings/Developer Settings/Personal Access Tokens and click on the “Generate new token” button.

_Give your new token a name by selecting the following specs:_



*    repo Full control of private repositories
    *   repo:status Access commit status
    *    repo_deployment Access deployment status
    *    public_repo Access public repositories
    *    repo:invite Access repository invitations
    *    security_events Read and write security events
*    write:packages Upload packages to github package registry
*    read:packages Download packages from github package registry
*    delete:packages
*    workflow Update github action workflows

After setting these scopes, click on “Generate” button. A new PAT will be generated and displayed on screen. 

Finally, copy the token string to your clipboard and paste it into the Ansible configuration file (ansible/roles/github_actions_runner/defaults/main.yml) as the “access_token” variable.


## Ansible {#ansible}

The initial installation is done with Ansible. Ansible automates the installation of Docker, the self-hosted GitHub actions runner and apt packages. For that, Ansible needs to be installed on our computer (control node) and SSH access to an EC2 machine (remote node/host) is required.  (related to [#16](https://github.com/geoadmin/config-vt-schema-lbm/issues/16))


### Install Ansible on control node {#install-ansible-on-control-node}

_Detailed instructions how to install Ansible can be found in Ansible [docs](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)._


### Ansible playbook and configuration {#ansible-playbook-and-configuration}

_The Ansible playbook can be downloaded from GitHub repo: _

[tool-vt-generation-pipeline](https://github.com/geoadmin/tool-vt-generation-pipeline)

_Ansible will need to be set up in with the following configuration: _

 _Set name of host for ansible/hosts.yaml_


```
vt-pipeline
```


_Set variables for host (such as github repo and software version) and roles_

ansible/inventory/vt-pipeline.yml


```
- hosts: vt-pipeline
 vars:
   github_account: geoadmin
   github_repo: config-vt-schema-lbm
   docker_version: "5:19.03.*"
 roles:
 - install_packages
 - docker
 - github_actions_runner

```



*   Set configuration for SSH 
    *   ansible/inventory/host_vars/vt-pipeline.yml
        *   The variable `ansible_host `has to match to Public DNS or Public IP of launched EC2 machine. 
        *   The variable `ansible_ssh_private_key_file` must be a path to the SSH private key.


```
ansible_host: "insert Public DNS or IP address of EC2 machine"
ansible_user: admin
ansible_become: true
ansible_ssh_private_key_file: ~/.ssh/path/to/private/key
```


_A docker version can be set_

ansible/inventory/vt-pipeline.yml


    Roles:


    Docker:

_Install_packages:_

There is nothing to be configured. Just keep in mind that apt repositories are configured for Debian Buster.

_set configuration for self-hosted runner with github_actions_runner: _

ansible/roles/github_actions_runner/defaults/main.yml 


```
# Runner user - user under which is the local runner service running
runner_user: "admin"

# Directory where the local runner will be installed
runner_dir: /opt/actions-runner

# Version of the GitHub Actions Runner
runner_version: "latest"

# If found, replace already registered runner
replace_runner: yes

# Do not show Ansible logs which may contain sensitive data (registration token)
hide_sensitive_logs: yes

# Personal Access Token for your GitHub account
access_token: "insert Personal Access Token here"

# GitHub address
github_server: "https://github.com"

# The steps to generate Personal Access Token was described in GitHub Actions section.
```



### Run Ansible deploy {#run-ansible-deploy}

_Ansible automated deploy can be run from its directory on a control node with following command:_


```
ansible-playbook inventory/vt-pipeline.yml -i hosts.yaml
```



## After Ansible installation {#after-ansible-installation}

_There are also some manual steps which need to be done after the automated Ansible installation with SSH into an EC2 machine._


```
ssh -i .ssh/path/to/private/key admin@ec2-public-dns-address
```



### tool-vt_generation-pipeline {#tool-vt_generation-pipeline}


### _Clone GitHub [tool-vt-generation-pipeline](https://github.com/geoadmin/tool-vt-generation-pipeline)  repo._ {#clone-github-tool-vt-generation-pipeline-repo}


```
git clone https://github.com/geoadmin/tool-vt-generation-pipeline.git
```



### Mount SSD disks {#mount-ssd-disks}

_Run install script install.sh_


```
cd tool-vt-generation-pipeline
sudo bash install.sh
```


_This script mounts the SSD disks into /mnt/lssd._

_It also moves the Docker and actions-runner directory to the SSD disk and creates symlinks for them. Both directories can be large and should be stored on the SSD disk._


### Install MapTiler-CLI {#install-maptiler-cli}

Install MapTiler CLI that uploads released mbtiles to your Cloud account.

Steps to install are described in README as well.

The API token to your Cloud is stored as GitHub secret MAPTILER_API_KEY. You can modify it there.

Install MapTiler CLI


```
cd tool-vt-generation-pipeline
python3 -m venv /mnt/lssd/venv
/mnt/lssd/venv/bin/pip install -r requirements.txt
/mnt/lssd/venv/bin/python setup.py install
```



## GitHub Setting {#github-setting}


### Self-hosted runner {#self-hosted-runner}

If the Ansible automated deploy with a correct PAT insertion was successful, you should see a self-hosted runner registered in the [config-vt-schema-lbm](https://github.com/geoadmin/config-vt-schema-lbm) repo, under Settings/Actions/Self-hosted runners. 

To better distinguish the self-hosted runners, it is advisable to add a label (e.g. swiss-topo-1) to each runner. This can be done by clicking on the expand arrow next to the already existing labels (self-hosted, Linux, x64).

Labels are used in GH Actions configuration to define which runner should be a specific workflow run on. In *.yaml files that define the workflow we use these labels:



*   import-workflow
*   push-workflow
*   pull-request-workflow
*   release-workflwo


### GitHub secrets {#github-secrets}


GitHub Secrets serve to store all passwords securely. It is not possible to display them. You can only update them in GitHub/Settings/Secrets. All secrets are read by GitHub Actions workflows and stored as environment variables.



*   AWS_ACCESS_KEY_ID - The Amazon access key available via [IAM service administration interface](https://console.aws.amazon.com/iam/home?#security_credential).
*   AWS_SECRET_ACCESS_KEY_ID - The Amazon access secure key available via [IAM service administration interface](https://console.aws.amazon.com/iam/home?#security_credential).
*   MAPTILER_API_KEY - API key for automated upload of mbtiles to SwissTopo MapTiler Cloud account after every release.
*   MAPTILER_LICENSE - MapTiler license key available at your MapTiler Cloud account, section Account/Desktop/Your licenses
*   VT_DUMPER_PSWD - Password provided to connect to the SwissTopo database.
*   PG_PASSWORD - Password for user geoadmin to both ltvt_master and ltvt_prod databases.
*   MT_SERVER_PSWD - Password for administration of MapTiler server.


# GitHub actions/workflows {#github-actions-workflows}

This section describes the GitHub actions to trigger the automatic production of vector tiles from swisstopo data, including the generation of statistics reports on the performance of the vector tiles pipeline.

_All GH Actions workflow definitions are stored in yaml files on GitHub: `config-vt-schema-lbm/.github/workflows/`_


## Import data {#import-data}



<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")


Triggers: 



*   Manual

Branch: Selected manually



*   select master branch to import data into master/DEV database.
*   select PROD branch to import data into PROD database.

Workflow definition file: import.yaml



1. Workflow gets dumps from the SwissTopo db server according to configuration in .env file using utility pg_dump. Dump files are stored in the EC2 file system.
2. Dumps are restored into the databases using utility pg_restore.
3. Geometry is transformed from LV95 (EPSG:2056) into Web-mercator (EPSG:3857)
4. SQL files are imported into the database.


## Swisstopo CI - generate reports {#swisstopo-ci-generate-reports}



<p id="gdcalert8" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert9">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image4.png "image_tooltip")


Triggers:		



*   On pull request
*   Manual

Branch:



*   Master
*   Selected manually for manual trigger

Workflow definition file: pull_request.yaml



1. The PR branch is cloned on the EC2 local file system.
2. A copy of the database is made.
3. SQL files are imported into the copy of the database.
4. Performance tests are run over the copy of the database.
5. Statistics are generated and stored at the file system.


## Swisstopo CI - _update PR comments_ {#swisstopo-ci-update-pr-comments}

Triggers:		



*   Cron - every 15 minutes
*   Manual

Workflow definition file: pr_updater.yml

This workflow checks every 15 minute if there is any new PR and if there is any report generated for the PR. It links PR with generated statistics and uploads the report from the filesystem as a comment to the matching PR.

**_SwissTopo CI - import sql_**



<p id="gdcalert9" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert10">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image5.png "image_tooltip")


Triggers:



*   On push
*   Manual

Branches:



*   Master (for master/DEV database)
*   PROD (for PROD database)
*   Selected manually for manual trigger

Workflow definition file: push.yml

This workflow contains two jobs that run in parallel.

Job: import_sql



1. Selected branch is cloned on the EC2 file system.
2. SQL files are imported into the database.

Job: generate_docs:



1. master branch is cloned on the EC2 file system
2. ghpages branch is cloned on the EC2 file system
3. Documentation is generated based on .yaml files
4. Generated files (markdowns and images) are copied into the ghpages branch
5. Modifications are committed

Documentation is then available at [https://geoadmin.github.io/config-vt-schema-lbm/](https://geoadmin.github.io/config-vt-schema-lbm/)


## _SwissTopo CI - generate mbtiles_ {#swisstopo-ci-generate-mbtiles}



<p id="gdcalert10" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert11">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image6.png "image_tooltip")


Triggers:



*   On release
*   Manual

Branches:



*   Master
*   Selected manually for manual trigger

Workflow definition file: release.yml



1. Selected branch is cloned on the EC2 file system.
2. Tiles are generated and stored at the file system.
3. Metadata are updated so the name of the dataset contains the release version.
4. Mbtiles are uploaded to the release as artefacts.
5. Mbtiles are uploaded to MapTiler Cloud.


# 


# Manual steps for Database Preparation {#manual-steps-for-database-preparation}

This section describes the steps needed to prepare the database of swisstopo data for the generation of vector tiles.

All the manual steps follow steps from GitHub Actions workflow. The only difference is that GitHub stores passwords and keys as GitHub secrets and the workflows have access to them. If you want to run steps manually you have to export necessary keys and passwords into environment variables.


## Starting the db container {#starting-the-db-container}

_Create folder for ci_cache (pgdata are located here)_


```
mkdir ci_cache
```


_Clone config-vt-schema-lbm_


```
git clone https://github.com/geoadmin/config-vt-schema-lbm.git
```


_Run make commands from config-vt-schema-lbm directory:_


```
cd config-vt-schema-lbm
```


_Initiate directories_


```
make init-dirs
```


_Start Docker container with running Postgresql_


```
make start-db
```


_or_


```
docker-compose up -d postgres
```



_It is advisable to configure your database in pgdata/postgresql.conf. You can use e.g. PgTune to generate configuration for your hardware. Do not forget to restart the database container._


```
docker-compose down
docker-compose up -d postgres
```



## Configuration {#configuration}

Configuration is located in .env and .env-postgres.

Make sure that postgres values in .env-postgres are always synchronized with those in .env.

Configuration files .env and .env-postgres are different in master and PROD branch.

Some of important configuration options are:

_BBOX is set to the extent of Switzerland_


```
BBOX=5.9559,45.818,10.4921,47.8084
```


_MBTILES_FILE is set to custom name_


```
MBTILES_FILE=ch.swisstopo.leichte-basiskarte.mbtiles
```


EC2_HOST ip address of EC2 virtual machine


```
EC2_HOST=http://18.197.30.154
```


There are three sources of data - ltvt, uvek and kogis databases.

There is different staging for master and PROD branch  (*_prod vs *_master etc.)

You can change the host address or user in the LTVT_DBCONN string.

Password is stored in the environment variable VT_DUMPER_PSWS which reads from GitHub secrets. 

Note that PTS_DB and HN_DB must match to dbname in layers/poi/poi.sql in dblink definition.


```
LTVT_DB=ltvt_master
LTVT_DBCONN=postgresql://vt_dumper:${VT_DUMPER_PSWD}@10.220.5.87/${LTVT_DB}
LTVT_TABLES=-n lbm
LTVT_DUMP_FILE=./data/ltvt_master.dump

PTS_DB=uvek_master
PTS_DBCONN=postgresql://vt_dumper:${VT_DUMPER_PSWD}@10.220.5.87/${PTS_DB}
PTS_TABLES=-t bav.oev_haltestellen
PTS_DUMP_FILE=./data/pts_master.dump

HN_DB=kogis_master
HN_DBCONN=postgresql://vt_dumper:${VT_DUMPER_PSWD}@10.220.5.87/${HN_DB}
HN_TABLES=-t bfs.gwr_addresses
HN_DUMP_FILE=./data/hn_master.dump
```



## Table selection {#table-selection}

You can choose which tables should be dumped/restored in options LVTV_TABLES, PTS_TABLES, HN_TABLES. Use pg_dump [syntax](https://www.postgresql.org/docs/12/app-pgdump.html).

-n pattern - Dump only schemas matching pattern. Multiple schemas can be selected by writing multiple `-n` switches.

-N pattern - Do not dump any schemas matching pattern

- t pattern - Dump only tables with names matching pattern. For this purpose, “table” includes views, materialized views, sequences, and foreign tables. Multiple tables can be selected by writing multiple -t switches.

-T pattern - Do not dump any tables matching pattern. The pattern is interpreted according to the same rules as for -t. -T can be given more than once to exclude tables matching any of several patterns.


## Process of import step-by-step {#process-of-import-step-by-step}

Manual process of import is identical with steps done by SwissTopo CI - import data workflow. Workflow definition is located in config-vt-schema-lbm/.github/workflows/init_db.yml

_Export password as environment variable_


```
export VT_DUMPER_PSWD=XXXXX
```


_Get dump of all database (it may take some time)_


```
make get-dumps
```



_Prepare db, create necessary functions and extensions and import bgdi data from dump _


_Import new data for the Leichte Basis Karte (LTVT) and uvek (public transport stops) and kogis (house numbers) database:_


```
make import-ltvt
make import-pts
make import-hn
```


Transform coordinate systems from the local (EPSG 2056) Web Mercator (EPSG 3857):


```
make transform-geometry
```



# 


# Work on Layers/Import of sql {#work-on-layers-import-of-sql}

This section refers to the iterative work by swisstopo cartographers, who will produce the files that define the schemas applied to the swisstopo data.

_After data import and after any modification to layers in *.sql or *.yaml files run:_


```
make clean
make build
make import-sql
```


_The YAML format definition file is available here:_

[https://docs.google.com/document/d/1WC8Ulriaybaioj1dNzgEgHxPB6Qp2SHeZnNc9vzkh3Y/edit#heading=h.ubi9p9x34ylt](https://docs.google.com/document/d/1WC8Ulriaybaioj1dNzgEgHxPB6Qp2SHeZnNc9vzkh3Y/edit#heading=h.ubi9p9x34ylt)


# 


# Generate Vector Tiles {#generate-vector-tiles}

This section describes the steps to generate vector tiles from the database of swisstopo data in combination with the definition formats from swisstopo cartographers.

Checkout the master branch for DEV tiles. Checkout the PROD branch for PROD tiles.

If you haven’t done it in the previous step make sure that changes in .sql and .yaml files are imported into db. You can do it by running these commands.


```
make clean
make build
make import-sql
```


_Use the following command to generate the tiles._


```
make generate-tiles
```


_Generated mbtiles are located at `config-vt-schema-lbm/data/ch.swisstopo.leichte-basiskarte.mbtiles`_


# 


# CloudPush {#cloudpush}

CloudPush is a utility that is part of the MapTiler Engine. Engine is available as a Docker container. If the Docker image is not available at your system you can get it from [DockerHub](https://hub.docker.com/r/maptiler/engine/).


```
docker pull maptiler/engine
```


The Amazon access and the secure key are available via [IAM service administration interface](https://portal.aws.amazon.com/gp/aws/developer/account/index.html?action=access-key). Your MapTiler Desktop PRO license key is stored in your Cloud account within the pages: **Account/Desktop/Your licenses**.

Create an alias for CloudPush, insert following as environment variables:



*   `MAPTILER_LICENSE - `MapTiler license key, see you Cloud account
*   `AWS_ACCESS_KEY_ID - `AWS Access Key, see IAM service administration
*   `AWS_SECRET_ACCESS_KEY - `AWS Secret Access Key, see IAM service administration
*   `AWS_HOST - `set to` s3.eu-central-1.amazonaws.com`


```
alias cloudpush="docker run -ti --rm -v $(pwd):/data
-e MAPTILER_LICENSE=*YOUR_LICENSE_KEY* 
-e AWS_ACCESS_KEY_ID=*AWS_ACCESS_KEY* 
-e AWS_SECRET_ACCESS_KEY=*SECRET_ACCESS_KEY* 
-e AWS_HOST=s3.eu-central-1.amazonaws.com maptiler/engine cloudpush"
```



List your bucket:


```
cloudpush s3://swisstopo-maptiler-data list
```



Add mbtiles to S3 bucket:


```
cloudpush --basename tiles/ch.swisstopo.leichte-basiskarte/*TAG_NAME* s3://swisstopo-maptiler-data add data/ch.swisstopo.leichte-basiskarte.mbtiles
```



# AWS CLI {#aws-cli}

While CloudPush extracts mbtiles into directory structure at S3 bucket, we use AWS CLI to copy the mbtiles file. AWS CLI is installed on every EC2 machine by default.

You have to configure AWS CLI either manually:


```
$ aws configure
AWS Access Key ID [None]: *AWS_ACCESS_KEY*
AWS Secret Access Key [None]: *SECRET_ACCESS_KEY*
Default region name [None]: eu-central-1
Default output format [None]: json
```



Or by exporting your AWS credentials as environment variables:


```
export AWS_ACCESS_KEY_ID=*AWS_ACCESS_KEY*
export AWS_SECRET_ACCESS_KEY=*SECRET_ACCESS_KEY*
```



Copy mbtiles to S3 bucket:


```
aws s3 cp data/ch.swisstopo.leichte-basiskarte.mbtiles \
s3://swisstopo-maptiler-data/tiles/ch.swisstopo.leichte-basiskarte/*TAG_NAME/
```



Create tiles.json based on already generated metadata.json. Copy already generated metadata.json from S3 to EC2:


```
aws s3 cp s3://swisstopo-maptiler-data/tiles/ch.swisstopo.leichte-basiskarte/*TAG_NAME*/metadata.json .
```



Create tiles.json


```
cat metadata.json | jq '. + {"tilejson": "2.0.0", "tiles": ["https://swisstopo-maptiler-data.s3.eu-central-1.amazonaws.com/tiles/ch.swisstopo.leichte-basiskarte/${TAG_NAME}/{z}/{x}/{y}.pbf"]}' > tiles.json
```



Copy newly created tiles.json to S3 bucket


```
aws s3 cp tiles.json s3://swisstopo-maptiler-data/tiles/ch.swisstopo.leichte-basiskarte/${TAG_NAME}/
```



# MapTiler Server

Maptiler server is available as a Docker container


```
docker pull maptiler/server:2.0
```


Once is MapTiler Server running you can access to its administration at: [https://swisstopo.maptiler.ch/admin](https://swisstopo.maptiler.ch/admin)



<p id="gdcalert11" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert12">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image7.png "image_tooltip")


Password is stored as GitHub secret MT_SERVER_PSWD.

After signing in you can see PostGIS connection to databases.



<p id="gdcalert12" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image8.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert13">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image8.png "image_tooltip")


You can add a new connection by clicking on ADD POSTGIS button. Then just fill in Postgres connection string:



<p id="gdcalert13" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image9.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert14">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image9.png "image_tooltip")


Be aware that a database you want to add, has to contain a table named contents.

For ltvt_master and ltvt_prod is added automatically after every commit into the corresponding branch. If you want to add it manually you can do it as follows (you have to modify name and json_with_layers):


```
DROP TABLE IF EXISTS contents;
CREATE TABLE contents (
name text UNIQUE PRIMARY KEY NOT NULL,
get_tile text NOT NULL,
extent box2d NOT NULL,
view_center real ARRAY[2] NOT NULL,
view_zoom integer NOT NULL,
minzoom integer NOT NULL,
maxzoom integer NOT NULL,
attribution text NOT NULL,
description text NOT NULL,
vector_layers json NOT NULL,
properties json
);

INSERT INTO contents (
name,
get_tile,
extent,
view_center,
view_zoom,
minzoom,
maxzoom,
attribution,
description,
vector_layers,
properties)
VALUES (
'SwissTopo_LBM_DEV',
'getmvt',
'BOX(5.9559 45.818,10.4921 47.8084)',
'{8.2,46.8}',
7,
0,
14,
'<a href="https://www.openmaptiles.org/" target="_blank">&copy; OpenMapTiles</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
'A tileset showcasing all SwissTopo layers in OpenMapTiles. https://openmaptiles.org',
'[{json_with_layers}]',
NULL
);
```


After adding a new connection to PostGIS, check the Tiles section and publish the tiles. You also have to change id to dev (for ltvt_master) or prod (for ltvt_prod) by clicking on Change ID button in order to have valid links from swisstopo.maptiler.ch domain.

More documentation at [https://support.maptiler.com/s9-server/knowledgebase/all](https://support.maptiler.com/s9-server/knowledgebase/all)

