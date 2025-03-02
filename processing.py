import csv  
import nltk
import string
import index
from nltk.book import *
def processing_run(keywords, selected_option):
  stopwords = nltk.corpus.stopwords.words('english')
  wnl = nltk.WordNetLemmatizer()

  string_list = [] 
  with open('output.csv', 'r', newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      for lines in reader:

          for i in range(4):
             cleaned_list = []
             no_punc_list = []
             element = lines[i]
             lower_case = element.lower() 
             tok_element = nltk.word_tokenize(lower_case)
           
             for tok in tok_element:
                 if tok not in string.punctuation:
                     no_punc_list.append(tok)
          
             for tok in no_punc_list:
                 if tok not in stopwords:
                    if i != 1 or (i == 1 and  tok != 'authors'):
                        if i != 3 or (i==3 and tok != 'submitted'):
                            cleaned_list.append(tok)
             lem_list = [wnl.lemmatize(tok) for tok in cleaned_list]
             string_list.append(', '.join(lem_list)) 
        
        
  with open('processed_output.csv','w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      for i in range(0, len(string_list), 4):
          row_list = string_list[i:i+4]
          writer.writerow(row_list)
    
    

  index.index_run(keywords, selected_option)