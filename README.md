# dataverse-helper-scripts

This repository contains several one-off or not-often-used scripts used for Dataverse related work.

1. [Github Issues to CSV](#github-issues-to-csv) - Pull selected github issues into a CSV file
2. [EZID DOI update/verify](#ezid-doi-updateverify) - Update EZID target urls for migrated datasets.  Verify that the DOIs point to the correct url.
3. [Basic Stress Test](#stress-tests) - Run basic browsing scenarios


## Github Issues to CSV

Use the github API to pull Issues into a CSV file

### Initial Setup

- Requires [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html)
    - OS X install: ```sudo pip install virtualenvwrapper```

1. Open a Terminal    
1. cd into ```src/github_issue_scraper```
1. Make a virtualenv: ```mkvirtualenv github_issue_scraper```
1. Install packages (fast): ```pip install -r requirements/base.txt```
1. Within ```src/github_issue_scraper```, copy ```creds-template.json``` to ```creds.json``` (in the same folder)
1. Change the ```creds.json``` settings appropriately.

### Setup (2nd time around)

1. Open a Terminal    
1. cd into ```src/github_issue_scraper```
1. Type ```workon github_issue_scraper``` (and press Return)

### Run a script

1. Set your repository, token information, output file name, and filters in ```creds.json```
1. cd into ```src/github_issue_scraper```
1. Run the program
    - From the Terminal: ```python pull_issues.py```
1. An output file will be written to ```src/github_issue_scraper/output/[file specified in creds.json]```

### Creds.json file notes

- Sample file

```json
{       
  "REPOSITORY_NAME" : "iqss/dataverse",
  "API_USERNAME" : "jsmith",
  "API_ACCESS_TOKEN" : "access-token-for-your-repo",

  "OUTPUT_FILE_NAME" : "github-issues.csv",
  "GITHUB_ISSUE_FILTERS" : {
        "labels" : "Component: API",
        "assignee" : "",
        "creator" : "",
        "labels_to_exclude" : "Status: QA"
    }
}
```

- ```API_USERNAME``` - your github username without the ```@```
- ```API_ACCESS_TOKEN``` - see: https://github.com/blog/1509-personal-api-tokens
- ```OUTPUT_FILE_NAME``` - Always written to ```src/github_issue_scraper/output/(file name)```
- ```GITHUB_ISSUE_FILTERS```
  - Leave filters blank to exclude them.  
    - JSON below would include all ``assignee`` values

```json
  "assignee" : "",
```

  - Comma separate multiple ```labels``` and ```labels_to_exclude```
    - Example of issues matching 3 labels: ```Component: API```, ```Priority: Medium``` and ```Status: Design```
      - (spaces between commas are stripped before attaching to api url)
```json
  "labels" : "Component: API, Priority: Medium, Status: Design",
```


## EZID DOI update/verify

* Location ```src/ezid_helper```

Scripts for two basic tasks:
  1. Update EZID target urls for migrated datasets.  
  2. Quality check: Verify that the DOIs point to the correct url.

### Input File

- Pipe ```|``` delimited .csv file with the following data:
  1.  Dataset id (pk from the 4.0 db table *dataset*)
  2.  Protocol 
  3.  Authority
  4.  Identifier
- Sample rows
```text
66319|doi|10.7910/DVN|29379
66318|doi|10.7910/DVN|29117
66317|doi|10.7910/DVN|28746
66316|doi|10.7910/DVN|29559
```

#### Input file creation

The input file is the result of a query from the postres psql shell:

* Basic query
```sql
select id, protocol, authority, identifier from dataset where protocol='doi' and authority='10.7910/DVN' order by id desc;
```

* Basic query to pipe ```|``` delimited text file

```sql
COPY (select id, protocol, authority, identifier from dataset where protocol='doi' and authority='10.7910/DVN' order by id desc) TO
'/tmp/file-name-with-dataset-ids.csv' (format csv, delimiter '|')
```

### Running the script
(to do)

### Output
(to do)


## Stress Tests

These are basic tests using [locustio](http://docs.locust.io/en/latest/quickstart.html).

### Initial Setup


- Requires [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html)
    - OS X install: ```sudo pip install virtualenvwrapper```
    - **Don't forget the Shell Startup File**: https://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file

1. Open a Terminal    
1. cd into ```src/stress_tests```
1. Make a virtualenv: ```mkvirtualenv stress_tests```
1. Install locustio: ```pip install -r requirements/base.txt```
    - This takes a couple of minutes

#### Initial Setup: update settings

1. Within ```src/stress_tests```, copy ```creds-template.json``` to ```creds.json``` (in the same folder)
1. **Change the ```creds.json``` settings appropriately.**

### Setup (2nd time around)

1. Open a Terminal    
1. cd into ```src/stress_tests```
1. Type ```workon stress_tests``` (and press Return)

### Run a script

1. Set your server and other information in ```creds.json```
1. cd into ```src/stress_tests```
1. Run a test script.  In this example run **basic_test_02.py**
    - From the Terminal: ```locust -f basic_test_02.py```
1. Open a browser and go to: http://127.0.0.1:8089/

### Run a performance script For Harvard Dataverse QA  
1. Set your server and other information in ```creds.json```
2. cd into ```src/stress_tests```
3. Run a test script.
    - From the Terminal: ```locust -f dataverse_perf.py```
4. Open a browser and go to: http://127.0.0.1:8089/
   5. HOST https://qa.dataverse.org
   6. duration 10 minutes
