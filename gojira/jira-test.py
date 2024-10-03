# GOJIRA - Jira Tools by SRPOL / SDV
# GOJIRA Grab - Comment Tracker - Track JIRA new comments
# a.dobrucki@samsung.com 

import autoupdater
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
from jira import JIRA
import argparse
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
import os
import time
import yaml

ASCII_ART_FILE = 'art.ascii'
SEEN_COMMENTS_FILE = 'seen_comments.yaml'
EXCLUDE_FILE = 'exclude.yaml'
CONFIG_FILE = "config.yaml"


def initialize_files():
    if not os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE, 'w') as file:
            yaml.safe_dump([], file)
    
    if not os.path.exists(SEEN_COMMENTS_FILE):
        with open(SEEN_COMMENTS_FILE, 'w') as file:
            yaml.safe_dump([], file)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            yaml.dump({'jql_str': '', 'jira_url': ''}, file)

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_version():
    version_file = "version.txt"
    if os.path.exists(version_file):
        with open(version_file, 'r') as file:
            return file.read().strip()
    return "0.0"  # Default version if no version file exists

def print_light_green(text):
    light_green = '\033[92m'
    reset = '\033[0m'
    return f"{light_green}{text}{reset}"
    
def print_ascii_art(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        art = file.read()
    print(art)

def load_exclusion_list():
    if (os.path.exists(EXCLUDE_FILE)):
        with open(EXCLUDE_FILE, 'r') as file:
            return set(yaml.safe_load(file))
    return set()

def establish_jira_connection(username, password, JIRA_URL):
    print_ascii_art(ASCII_ART_FILE)
    print(f"Gojira Grab - JIRA Comment tracker {get_current_version()} \nJira Tools by SRPOL / SDV")
    print("Connecting to Jira...")

    jira_client = JIRA(options={'server': JIRA_URL, 'verify': False}, basic_auth=(username, password))
    print("No Strong OAUTH Detected. Bypassing.")
    return jira_client

def import_jira_issues(jira_client):
    jira_issues = jira_client.search_issues(jql_str)
    return jira_issues

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def load_seen_comments():
    if os.path.exists(SEEN_COMMENTS_FILE):
        with open(SEEN_COMMENTS_FILE, 'r') as file:
            return set(yaml.safe_load(file))
    return set()

def save_seen_comments(seen_comments):
    with open(SEEN_COMMENTS_FILE, 'w') as file:
        yaml.safe_dump(list(seen_comments), file)

def show_latest_activity(jira_client, seen_comments):
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    all_comments = []
    exclusion_list = load_exclusion_list()
    jira_issues = import_jira_issues(jira_client)
    
    for issue in jira_issues:
        if issue.fields.comment.comments:
            recent_comments = [
                comment for comment in issue.fields.comment.comments 
                if datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z') > seven_days_ago
                and comment.author.emailAddress not in exclusion_list
            ] 
            for comment in recent_comments:
                if comment.id not in seen_comments:
                    all_comments.append((issue, comment))
                    seen_comments.add(comment.id)
    
    all_comments.sort(
        key=lambda item: datetime.strptime(item[1].created, '%Y-%m-%dT%H:%M:%S.%f%z'), 
        reverse=True
    )
    
    clear_console()


    print('Used Query: ' + jql_str)
    for issue, comment in all_comments:
        created_date = datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z')
        formatted_date = created_date.strftime('%d-%m-%Y %H:%M')
        issue_key_colored = print_light_green(issue.key)
        print(f"{issue_key_colored} {formatted_date}, - {comment.author.displayName}, {issue.fields.summary}")

    
    return all_comments  

initialize_files()
config = load_config(CONFIG_FILE)
if config['jql_str'] == '':
    print("Error: 'jql_str' is not defined in the jql_string.yaml file")
    exit(1)
elif config['jira_url'] =='':
    print('Error: JIRA URL is not defined in the config.yaml file')
    exit(1)
else:
    jql_str = config['jql_str']
    JIRA_URL = config['jira_url']

def main():

    # [-h] for help
    # username and password are required as arguments
    autoupdater.check_for_update()
    parser = argparse.ArgumentParser(description='Show latest activity in JIRA issues.')
    parser.add_argument('username', type=str, help='JIRA username')
    parser.add_argument('password', type=str, help='JIRA password')
    args = parser.parse_args()
    jira_client = establish_jira_connection(args.username, args.password, JIRA_URL)
    seen_comments = load_seen_comments()
    
    while True:
        all_comments = show_latest_activity(jira_client, seen_comments)
        
        if all_comments:
            input("Press Enter to see the first new comment or wait for the next update...")
            for issue, comment in all_comments:
                clean_comment = clean_html(comment.body)
                clear_console()
                print(f"Issue: {issue.key}, Title: {issue.fields.summary}")
                print(f'Link: {issue.self}')
                print(f"Author: {comment.author.displayName}, Created: {comment.created}")
                print(f"Comment: {clean_comment}")
                input("Press Enter to see the next comment...")
        else:
            print("No new comments.")
            time.sleep(300)  
        
        save_seen_comments(seen_comments)

if __name__ == "__main__":
    main()