import requests
from bs4 import BeautifulSoup
import csv
import processing

def crawler_run(search_text, keywords, selected_option):
   URL = f"https://arxiv.org/search/?query={search_text}&searchtype=all&source=header"
   page = requests.get(URL)
   soup = BeautifulSoup(page.content, "html.parser")

   # Check if the page was fetched successfully
   if page.status_code == 200:
       # Try to find the main container
       results = soup.find(id="main-container")

       # Check if the main container is found
       if results:
           with open('output.csv', 'w', newline='') as file:
               # Create a CSV writer
               writer = csv.writer(file)
               file.write('')
            
           metadata = results.find_all("li", class_="arxiv-result")
        
           for meta_element in metadata:
               title_element = meta_element.find("p", class_="title")
               authors_element = meta_element.find("p", class_="authors")
               abstract_element = meta_element.find("span", class_="abstract-full")
               date_element = meta_element.find("p", class_="is-size-7")
            
               if title_element:
                   title = title_element.text.strip()
               else: 
                   title = ""
                
               if authors_element:
                   authors = ' '.join([author.strip() for author in authors_element.stripped_strings])
               else:
                   authors = ""
            
               if abstract_element:
                   abstract = abstract_element.text.strip()
               else:
                   abstract = ""
            
               if date_element:
                   strr = date_element.text.strip()
                   date = strr.split('\n')[0]
               else:
                   date = ""
                
            
            
               with open('output.csv', 'a', newline='', encoding='utf-8') as file:
                   # Create a CSV writer
                   writer = csv.writer(file)
                   writer.writerow([title, authors, abstract, date])
               
                
               
       else:
           print("Main container not found on the page.")
   else:
       print(f"Failed to fetch the page. Status code: {page.status_code}")
    
   processing.processing_run(keywords, selected_option)