import csv
import search
def index_run(keywords, selected_option): 
  dic = {}
    
  with open('processed_output.csv','r', newline='', encoding='utf-8') as file:
       reader = csv.reader(file)
       for line_num, line in enumerate(reader, start=1):
           for column in line:
               items = column.split(', ')
               for item in items:
                   if item not in dic:
                       dic[item] = []
                   if item in dic:
                       if line_num not in dic[item]:
                           dic[item].append(line_num)
        
  search.query_proc(keywords,dic, selected_option)
  


    
        
    