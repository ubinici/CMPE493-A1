import re
import string
import json
from indexer import tokenize

# Function to parse the user query in order to determine whether it is a phrase search or proximity search
def query_parser(query):
    phrase_pattern = re.compile(r'"(.*?)"') # Regular expression for phrase query
    proximity_pattern = re.compile(r'(\w+)\s+(\d+)\s+(\w+)') # Regular expression for proximity query

    phrase_match = phrase_pattern.search(query) # Search for the phrase query matches
    proximity_match = proximity_pattern.search(query) # Search for the proximity query matches

    if phrase_match is not None: # If it is a phrase search, return the query type and the queried phrase
        return 'phrase', phrase_match[1]

    elif proximity_match is not None: # If it is a proximity search, return the query type and the queried phrase that contains an integer between two strings
        return 'proximity', (
            proximity_match[1],
            int(proximity_match[2]),
            proximity_match[3],
        )

    else: # If it is neither, return None for both query type and parsed query
        return None, None

# Function to carry out phrase search operations
def phrase_query(query, index):
    tokens = tokenize(query) # Tokenize the query

    if not tokens: # If no tokens, return an empty list
        return []

    postings = [set(index[token].keys()) if token in index else set() for token in tokens] # Fetch postings list for tokens
    candidates = set.intersection(*postings) # Look for the intersection of the posting lists
    matching_docs = [] # Create an empty list for matching IDs

    for doc_id in candidates: # Iterate through the candidate document IDs
        positions = [index[token][doc_id] for token in tokens] # Fetch the positions for each token in the current document
        has_matching_positions = False
        
        for position0, position1 in zip(positions[:-1], positions[1:]): # Iterate through position pairs
            matching_positions = [p1 - p0 == 1 for p0, p1 in zip(position0, position1)] # Check if adjacent positions match using list comprehension
            if any(matching_positions): # If there are any matching positions
                matching_docs.append(doc_id) # Add matching document IDs
                has_matching_positions = True
                break
        
        if not has_matching_positions:
            continue

    return sorted(matching_docs) # Return sorted list of matching documents

# Function to carry out proximity search operations
def proximity_query(query, index):
    token1, max_dist, token2 = query # Dissect the query tuple accordingly

    if token1 in index and token2 in index: # Check if both tokens are in the index
        intersection = set(index[token1].keys()).intersection(index[token2].keys()) # Compute the intersection and store it in the variable
        matching_docs = [doc_id for doc_id in intersection # Iterate through common document IDs
                         if any(abs(p1 - p2) - 1 <= max_dist for p1 in index[token1][doc_id] for p2 in index[token2][doc_id])] # Check if the distance between the two tokens is within range
    
    else:
        matching_docs = []

    return sorted(matching_docs) # Return sorted list of matching documents

# Function to process the parsed query in accordance with its type
def query_processor(query_type, parsed_query, index):

    if query_type == 'phrase': # Check if query type was returned phrase search type
        return phrase_query(parsed_query, index) # Return the relevant function for this query type
    
    elif query_type == 'proximity': # Check if the query type was returned proximity search type
        return proximity_query(parsed_query, index) # Return the relevant function for this query type

# Function to get the user input and determine whether the format of the query is valid
def get_query():

    ERROR_MESSAGE = (
    "Invalid query format.\n"
    "For phrase queries, please place your query between quotation marks.\n"
    "For proximity queries, do not forget to indicate the number of words with a number."
    )

    while True:        
        query = input("Enter your query: ") # Get user input for the query    
        query_result = query_parser(query) # Return the parsed query and assign it to a variable

        if query_result is None: # If the query format is invalid, print the error message and ask for another input
            print(ERROR_MESSAGE)
            continue

        else: # If the query format is valid, dissect the parsed query tuple accordingly and return it
            query_type, parsed_query = query_result
            return query_type, parsed_query

# Check if the script is being run directly and not imported as an external module
if __name__ == '__main__':
    with open('inverted_index.json', 'r', encoding='utf-8') as index_file: # Open and read the inverted index JSON file
        index = json.load(index_file) # Load the JSON data into the index variable

    query_type, query_data = get_query() # Call the get_query function to obtain the query type and query data from the user
    result = query_processor(query_type, query_data, index) # Return the processed query using its type, data, and the index
    print(f"Results for query '{query_data}': {result}") # Print the results of the query
