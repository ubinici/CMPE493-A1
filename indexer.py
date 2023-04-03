import os
import re
import json
import string
from collections import defaultdict

# Define a set of English stopwords
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn",
    "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't",
    "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn",
    "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn",
    "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or",
    "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should",
    "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs",
    "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up",
    "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while",
    "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're",
    "you've", "your", "yours", "yourself", "yourselves"
}

# Function to tokenize the input text
def tokenize(text):
    text = text.lower() # Convert text to lowercase
    text = re.sub(r'\d+', '', text) # Remove digits from the text
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text) # Remove punctuation from the text
    tokens = text.split()  # Split the text into tokens (words)
    tokens = list(filter(lambda token: token not in STOPWORDS, tokens)) # Remove stopwords from the tokens
    return tokens

# Function to index a document
def index_doc(doc_id, text, index):
    tokens = tokenize(text) # Tokenize the input text
    for position, token in enumerate(tokens): # Iterate through tokens with their positions
        if token not in index: # If the token is not in the index, create an empty entry for it
            index[token] = {}
        if doc_id not in index[token]: # If the document ID is not in the token's entry, create an empty list for it
            index[token][doc_id] = []
        index[token][doc_id].append(position) # Add the token's position in the document to the index

# Function to build the index from a collection of files
def build_index(files):
    index = defaultdict(dict) # Create an empty index using defaultdict
    # Define regular expressions to retrieve document IDs and content
    doc_pattern = re.compile(r'<REUTERS.*?NEWID="(\d+)".*?>(.*?)<\/REUTERS>', re.DOTALL)
    content_pattern = re.compile(r'<TITLE>(.*?)<\/TITLE>|<BODY>(.*?)<\/BODY>', re.DOTALL)

    for file_name in os.listdir(files): # Iterate through the files in the directory
        if not file_name.endswith('.sgm'): # Skip files that don't have the .sgm extension
            continue

        with open(os.path.join(files, file_name), 'r', encoding='latin-1') as f: # Open the .sgm file
            print(f"Processing file: {file_name}")
            content = f.read() # Read the file content

        for match in doc_pattern.finditer(content): # Iterate through the matched documents in the content
            doc_id = int(match.group(1)) # Get the document ID
            content = match.group(2) # Get the document content
            sections = content_pattern.findall(content) # Find the title and body sections in the document
            text = ' '.join(' '.join(t) for t in sections) # Combine the title and body sections into a single text
            index_doc(doc_id, text, index) # Index the document

    return index

# Function to save the index to a file
def save_index(index, path):
    print(f"Saving index to file: {path}")
    with open(path, 'w', encoding='utf-8') as index_file: # Open the output file
        json.dump(index, index_file, indent=4, sort_keys=True) # Write the index as JSON to the file

# Main function
def main():
    print("Initializing indexing operations.")
    files = 'reuters21578/reuters21578' # Directory containing the input files
    index = build_index(files) # Build the index from the input files
    save_index(index, 'inverted_index.json') # Save the index to a JSON file
    print("Finished indexing all files.")

# Check if the script is being run directly and not imported as an external module
if __name__ == '__main__':
    
    main() # Call the main function