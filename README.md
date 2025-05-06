# About this project
## What it does
It retrieves research papers from arXiv based on user keywords, using one of three different retrieval algorithms available.
## How it works
Through a simple UI, the user is able to search the corpus (which consists of 50 documents) for papers relevant to their desired keywords. Additionally, the user is able to choose one of three different retrieval algorithms:
1. Boolean Retrieval
2. Vector Space Model (VSM)
3. Okapi BM25

On the UI, the user must fill in two text boxes and select one of the three algorithms. In the first text box, the user must enter the keyword(s) to search arXiv for relevant papers, forming the corpus. We will refer to these keywords as 'search words'. In the second text box, the user must enter the keyword(s) that will be used by the retrieval algorithms to search through the corpus and return relevant documents. We will refer to this input as the 'query'. Finally, we will refer to the selected retrieval algorithm as the 'selected algorithm'.
### interface.py
This file displays the UI panel and handles its structure. When the user presses the Search button, the `on_search` function calls `web_crawler.py` and passes the search words, the query and the selected algorithm.
### web_crawler.py
This file searches for documents on arXiv based on the user's search words. It then uses BeautifulSoup, to parse the HTML and extract key data from the first 50 relevant documents:
+ Title
+ Authors
+ Abstract
+ Date of submission

The data is written to a file named `output.csv` which contains 50 rows (one for each document) and 4 columns (one for each data element). Then, the program calls `processing.py`, passing only the query and the selected algorithm, as the search words are no longer needed.
### processing.py
This file is responsible for processing the text in `output.csv`. The steps include:
+ Converting all letters to lowercase
+ Tokenization (splitting text into words)
+ Removing punctuation marks and stopwords
+ Lemmatization (reducing words to their base form)

The processed text is saved in `processed_output.csv`, where each word appears in lowercase and lemmatized form, separated by commas. The program then calls  `index.py` and passes the query and selected algorithm.
### index.py
This file creates the inverted index. All terms in `processed_output.csv` are inserted into a dictionary, where each term is mapped to a list of document numbers (1-50) in which it appears. Finally, the program calls `search.py`, passing the query, the inverted index and the selected algorithm. 
### search.py
The code in this file processes the query in the same manner as the text in `output.csv`, following identical preprocessing steps. Finally, the program runs the algorithm that was selected by the user, printing the title, authors, abstract and submission date of each relevant document to the terminal.
## Important notes ⚠
- Run only the `interface.py` file. Running other files separately will cause errors.
- If you opt to use the Boolean Retrieval algorithm and wish to include more than one word in your query you will have to use the words 'AND' or 'OR', while there's also the option of using the word 'NOT'. This algorithm returns **every** document that contains the query term(s), whereas VSM and Okapi BM25 will return five and three documents respectively every time (those with the highest similarity to your query).
- Make sure you install the required packages before running the program: `pip install nltk bs4 requests rank_bm25`
