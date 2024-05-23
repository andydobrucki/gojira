"""
AI Glossary Expander Script
Author: Andrzej Dobrucki, SDV, SRPOL

This script is used to expand glossaries from a csv file, using OS Llama3
It reads terms from a CSV file, calls an API to generate descriptions for each term, and writes the terms and their descriptions to a new CSV file. It also displays an ASCII logo for SDV at the start of the script.

The script uses the following functions:
- call_api: Calls the API with the given data and returns the response.
- get_description: Gets the description for a term from the API.
- process_csv: Reads terms from the input CSV file, gets their descriptions, and writes them to the output CSV file.
- display_logo: Displays an ASCII logo for SDV.

"""

import requests
import json
import csv
import os 
import argparse
from pymongo import MongoClient

def call_api(data):
    url = "http://localhost:11434/api/generate"
    call = {
        "model": "llama3",
        "prompt": "You are a glossary writer working in a linux development team, where developers develop systems for automotive industry. You are going to explain terms from a feature list Based on category and subcategory. Please return only the glossary entry in form of a single sentence ready to paste into final glossary, nnothing else. Category =" + data['category'] + ". Sub category =" + data['sub-category'] + ". term = "+data['term'],
        "stream":False
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(call))
    return response.json()
    

def get_description(category, sub_category, term):
    data = {
        'category': category,
        'sub-category': sub_category,
        'term': term
    }
    response = call_api(data)
    description = response['response']
    return description

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
        reader = csv.reader(csv_in)
        writer = csv.writer(csv_out)
        next(reader, None)  # skip the headers

        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['glossary_db']  # use or create a database called 'glossary_db'
        collection = db['terms']  # use or create a collection called 'terms'

        for row in reader:
            category, sub_category, term = row
            description = call_api({'category': category, 'sub-category': sub_category, 'term': term})

            # Create a document
            doc = {
                'category': category,
                'sub_category': sub_category,
                'term': term,
                'description': description['response']
            }

            # Insert the document into the collection
            collection.insert_one(doc)

            print(f"{category}>{sub_category}>{term}>>> {description['response']}")
            writer.writerow([category, sub_category, term, description['response']])

def display_logo():
    logo = """
  _____________________   ____
 /   _____/\______ \   \ /   /
 \_____  \  |    |  \   Y   / 
 /        \ |    `   \     /  
/_______  //_______  /\___/   
        \/         \/         

AI Glossary Expander (c) 2024 SDV, SRPOL
    """
    print (logo)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')



parser = argparse.ArgumentParser(description="AI Glossary Expander")
parser.add_argument('input_csv', type=str, help='The input CSV file')
parser.add_argument('output_csv', type=str, help='The output CSV file')
args = parser.parse_args()

clear_screen()
display_logo()
process_csv(args.input_csv, args.output_csv)