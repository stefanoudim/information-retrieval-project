import nltk
import csv
import string
from collections import defaultdict
from rank_bm25 import BM25Okapi
import math
def query_proc(query,dic,selected_option):
    wnl = nltk.WordNetLemmatizer()
    lower = query.lower()
    terms = nltk.word_tokenize(lower)
    no_punc_list=[]
    for term in terms:
        if term not in string.punctuation:
            no_punc_list.append(term)
    final_query = [wnl.lemmatize(term) for term in no_punc_list]
    if selected_option == 'Boolean Retrieval':
        boolean(final_query,dic)
    elif selected_option == 'VSM':
        vector_space_model(final_query, dic)
    else:
        okapi_bm25(final_query,dic)
  
    
    
def boolean(query,dic):
    result = None
    current_set = None
    last_logical_op = "and"  # Default behavior is AND
   
    
    for term in query:
      if term in ["and", "or", "not"]:
         last_logical_op = term
         continue

      term_set = set(dic.get(term, []))

      if current_set is None:
         current_set = term_set
      elif last_logical_op == "and":
         current_set &= term_set
      elif last_logical_op == "or":
         current_set |= term_set
      elif last_logical_op == "not":
         current_set -= term_set
      else:
        # Default behavior is AND
         current_set &= term_set

    if result is None:
        result = current_set
    elif last_logical_op == "or":
        result |= current_set
    elif last_logical_op == "not":
        result -= current_set
    else:
        # Default behavior is AND
        result &= current_set


    with open('output.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for doc_id, row in enumerate(reader, start=1):
            if doc_id in result:
                print(f'Document {doc_id}:\n',row)



def vector_space_model(query, dic):
    term_counts = defaultdict(dict)


    with open('processed_output.csv', 'r', newline='', encoding='utf-8') as file:
       reader = csv.reader(file)
    
       for doc_id, row in enumerate(reader, start=1):
         # Process each term in the line
         line = ' '.join(row)
         terms = line.split()
         terms = [term.strip(string.punctuation) for term in terms]
       
         for term, docs_containing_term in dic.items():
            # Count occurrences of the term in the current line
            term_count = terms.count(term)            
            term_counts[term][f'doc{doc_id}'] = term_count
    
    term_df = defaultdict(int)

    # Iterate over each term in the 'dic' dictionary
    for term, docs_containing_term in dic.items():
        # Update document frequency for each term based on the set of documents in 'dic'
        for doc_id in docs_containing_term:
            term_df[term] += 1
    
    
    term_idf = {}
    for term, df in term_df.items():
        # Calculate IDF for each term
        idf = math.log10(50 / df)
        term_idf[term] = idf
    
    
    tf_idf = {}
    for term, doc_freq in term_df.items():
        tf_idf[term] = {}
        for doc, term_freq in term_counts[term].items():
            tf_idf[term][doc] = term_freq * term_idf[term]
            

    
    
    query_tf = {}
    for word in query:
        query_tf[word] = query.count(word)
        
    query_tfidf = {term: query_tf[term] * term_idf.get(term, 0) for term in query}
    query_norm = math.sqrt(sum(tfidf ** 2 for tfidf in query_tfidf.values()))
    normalized_query_tfidf = {term: tfidf / query_norm if query_norm != 0 else 0 for term, tfidf in query_tfidf.items()}
    
    if query_norm != 0:
        normalized_tf_idf = {}
        doc_norms = {doc_id: math.sqrt(sum(tfidf[doc_id] ** 2 for tfidf in tf_idf.values())) for doc_id in tf_idf[list(tf_idf.keys())[0]]}
        normalized_tf_idf = {term: {doc_id: tfidf / doc_norms[doc_id] for doc_id, tfidf in values.items()} for term, values in tf_idf.items()}
    
        cos = {}
        for doc_id in normalized_tf_idf[list(normalized_tf_idf.keys())[0]]:
            # Initialize the similarity score for the current document
            similarity_score = 0.0
            # Iterate over each term in the query
            for term, q_tfidf_value in normalized_query_tfidf.items():
            # Check if the term exists in the corpus (tf_idf dictionary)
                if term in normalized_tf_idf:
                    # Calculate the contribution of the current term to the similarity score
                    term_tfidf_value = normalized_tf_idf[term].get(doc_id, 0.0)
                    similarity_score += term_tfidf_value * q_tfidf_value

                    # Store the similarity score for the current document
            cos[doc_id] = similarity_score
        top_5_documents = sorted(cos.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_document_numbers = [int(doc[0][3:]) for doc in top_5_documents]
    
    
        with open('output.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

        # Create a dictionary to store rows with document numbers as keys
            rows_dict = {str(doc_id): row for doc_id, row in enumerate(reader, start=1)}

        # Iterate over the top_5_document_numbers and print the corresponding rows
            for doc_number in top_5_document_numbers:
                row = rows_dict.get(str(doc_number))
                if row:
                    print(f'Document {doc_number}:\n','. '.join(row))
    else:
        print("No matching results found.")
                 
def okapi_bm25(final_query,dic):
    dictionary_list = [[] for _ in range(50)]   
    for term, document_numbers in dic.items():
        for doc_number in document_numbers:
            dictionary_list[doc_number - 1].append(term)
            
    bm25 = BM25Okapi(dictionary_list)
    li = []
    with  open('output.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            li.append('. '.join(row))
    
    result = bm25.get_top_n(final_query, li, n=3)

    for doc in result:
        document_index = doc 
        print(f'Document {li.index(document_index)+1}:')
        print(doc)
        

    
    
