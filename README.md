## Gojira Grab - Jira Comment Tracker

Windows users - please install Windows Terminal before running this script - https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-us&gl=PL
App updates automatically on startup.

### Running the script

`python3 jira-test.py jiraid jirapassword`

On first run, app retrieves comments from the last 7 days. 

### Excluding comnments from specific users
The 'exclude.yaml' file (created on first run) accepts user emails that will be excluded from retrieved comments (e.g. yourself)

Single entry in the yaml file should look like this:

`- 'andy@mail.com'`

### Available releases:
https://github.com/andydobrucki/gojira/releases

Namaste

