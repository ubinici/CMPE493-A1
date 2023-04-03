================================================================================
README - Text Indexer and Query Processor
================================================================================

This program consists of two Python scripts: indexer.py and query_processor.py.

indexer.py        : This script is responsible for indexing a collection of 
                    documents compiled under SGM files in the "reuters21578" 
                    folder and generating an inverted index.

query_processor.py: This script allows the user to perform phrase and proximity
                    queries using the inverted index created by indexer.py.

Python Version    : 3.8 or higher is recommended.

Instructions for Running the Program:
--------------------------------------------------------------------------------

1. Ensure that you have Python 3.8 or higher installed on your system. To check
   the installed version, open a terminal or command prompt and run:

   python --version

2. Install the required packages if necessary.

3. Place the indexer.py, query_processor.py, and your document collection in the
   same directory.

4. Run the indexer.py script to generate the inverted index. In the terminal or
   command prompt, navigate to the directory containing the scripts and run:

   python indexer.py

   This will create a JSON file named 'inverted_index.json' containing the
   inverted index.

5. Run the query_processor.py script to perform queries using the generated
   inverted index. In the terminal or command prompt, run:

   python query_processor.py

   Follow the on-screen instructions to enter your query. The script will return
   the document IDs that match the query.

Note: Make sure that the document collection is in the "reuters21578/reuters21578"
      directory, or modify the script accordingly to point to the correct
      directory.

