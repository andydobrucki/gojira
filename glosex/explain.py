"""
AI Glossary Browser Script
Author: Andrzej Dobrucki, SDV, SRPOL

This script is used to browse glossaries stored in a MongoDB database. It prompts the user for a search term, finds all terms in the database that contain the search term, and displays them to the user. The user can then select a term by its number to view its full glossary entry.

The script uses the following functions:
- connect_to_db: Connects to the MongoDB database and returns the collection of terms.
- search_terms: Searches the database for terms containing the given search term and returns the results.
- display_terms: Displays the enumerated terms to the user.
- get_user_selection: Prompts the user to select a term by its number and returns the selected term.
- display_entry: Displays the full glossary entry for the selected term.

"""
from pymongo import MongoClient

def display_logo():
    logo = """
  _____________________   ____
 /   _____/\______ \   \ /   /
 \_____  \  |    |  \   Y   / 
 /        \ |    `   \     /  
/_______  //_______  /\___/   
        \/         \/         

SDV Glossary Browser (c) 2024 SDV, SRPOL
/bye to exit
    """
    print (logo)

display_logo()

client = MongoClient('mongodb://localhost:27017/')
db = client['glossary_db'] 
collection = db['terms']
while True:
    search_term = input("Enter a search term: ")
    if search_term == "/bye":
            break

    results = collection.find({"term": {"$regex": search_term, "$options": 'i'}})
    
    results_list = list(results)
    if not results_list:
        print("Term not found in glossary")
        continue

    for i, result in enumerate(results_list):
        print(f"{i}: {result['term']}")

    number = int(input("Enter a number: "))

    entry = results_list[number]
    print(f"Term: {entry['term']}")
    print(f"Category: {entry['category']}")
    print(f"Sub Category: {entry['sub_category']}")
    print(f"Description: {entry['description']}")