## Gojira Grab - Jira Comment Tracker

Windows users - This script is best watched on Windows Terminal https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-us&gl=PL


### Installation
Install dependencies:
`pip3 install -r requirements.txt` 

### Running the script
1. Run the script once to create empty yaml files

`python3 jira-test.py`

2. Provide jira_url and jql_query in config yaml
3. Then run the script again with id and password:

`python3 jira-test.py jiraid jirapassword`

When first run, app retrieves comments from the last 7 days. 
Hit enter to see the first comment on the list.
After all comments have been viewed, app goes into watch mode and monitors for new comments every 5 minutes.

App updates automatically on startup based on repo's release tag. 

### Excluding comments from specific users
The 'exclude.yaml' file (created on first run) accepts user emails that will be excluded from retrieved comments (e.g. yourself)

Single entry in the yaml file should look like this:

`- 'andy@mail.com'`

### Available releases:
https://github.com/andydobrucki/gojira/releases

Namaste
