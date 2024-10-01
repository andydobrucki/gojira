# GOJIRA - Jira Tools by SRPOL / SDV
# GOJIRA Comment Tracker - Track JIRA new comments
# a.dobrucki@samsung.com 
# v.0.1

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


# Define your JQL Query here
jql_str = 'filter = 87554 AND summary !~ "N/A" AND type = sub-task AND status not in (Closed, Resolved, "Drop")'
ascii_art_file = 'art.ascii'

# seen comments file
SEEN_COMMENTS_FILE = 'seen_comments.yaml'

def print_ascii_art(file_path):
    with open(file_path, 'r') as file:
        art = file.read()
        print(art)


def establish_jira_connection(username, password):
    print_ascii_art(ascii_art_file)
    print("Gojira Grab - JIRA Comment tracker 0.1 \nJira Tools by SRPOL / SDV")
    print("Connecting to Jira...")
    JIRA_URL = "https://jira.slsi.samsungds.net/"
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
    
    jira_issues = import_jira_issues(jira_client)
    
    for issue in jira_issues:
        if issue.fields.comment.comments:
            recent_comments = [
                comment for comment in issue.fields.comment.comments 
                if datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z') > seven_days_ago
            ]
            for comment in recent_comments:
                if comment.id not in seen_comments:
                    all_comments.append((issue, comment))
                    seen_comments.add(comment.id)
    
    # Sort all comments from newest to oldest
    all_comments.sort(
        key=lambda item: datetime.strptime(item[1].created, '%Y-%m-%dT%H:%M:%S.%f%z'), 
        reverse=True
    )
    
    # Comment list
    os.system('clear')

    print('Used Query: ' + jql_str)
    for issue, comment in all_comments:
        created_date = datetime.strptime(comment.created, '%Y-%m-%dT%H:%M:%S.%f%z')
        formatted_date = created_date.strftime('%d-%m-%Y %H:%M')
        print(f"{issue.key}, {formatted_date}, - {comment.author.displayName} - CET, {issue.fields.summary}")
    
    return all_comments

def main():
    # [-h] for help
    # username and password are required as arguments
    parser = argparse.ArgumentParser(description='Show latest activity in JIRA issues.')
    parser.add_argument('username', type=str, help='JIRA username')
    parser.add_argument('password', type=str, help='JIRA password')
    args = parser.parse_args()

    jira_client = establish_jira_connection(args.username, args.password)
    seen_comments = load_seen_comments()
    
    while True:
        all_comments = show_latest_activity(jira_client, seen_comments)
        
        if all_comments:
            input("Press Enter to see the first new comment or wait for the next update...")
            for issue, comment in all_comments:
                clean_comment = clean_html(comment.body)
                os.system('clear')
                print(f"Issue: {issue.key}, Title: {issue.fields.summary}")
                print(f'Link: {issue.self}')
                print(f"Author: {comment.author.displayName}, Created: {comment.created}")
                print(f"Comment: {clean_comment}")
                input("Press Enter to see the next comment...")
        else:
            print("No new comments.")
            time.sleep(100)  
        
        save_seen_comments(seen_comments)

if __name__ == "__main__":
    main()