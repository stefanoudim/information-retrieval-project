import web_crawler
from tkinter import *

def on_search():
    search_text = entry.get()
    keywords = entry2.get()
    selected_option = clicked.get()
    if search_text and keywords:
        web_crawler.crawler_run(search_text, keywords, selected_option)
    else:
        if not search_text:
            entry_var.set('Invalid Search')
        else:
            entry2_var.set('Invalid Keywords')

gui = Tk()
gui.geometry('500x200+500+250')
gui.title("Search Engine")
gui.resizable(False, False)

Label(gui, text='Search').grid(row=0, column=0, padx=(120, 10), pady=40, sticky='e')
entry_var = StringVar()
entry = Entry(gui, width=30, textvariable=entry_var)
entry.grid(row=0, column=1, padx=(0, 50), pady=40, sticky='w')

# Add a second entry widget below the existing one
Label(gui, text='Keywords').grid(row=1, column=0, padx=(120, 10), pady=40, sticky='e')
entry2_var = StringVar()
entry2 = Entry(gui, width=30, textvariable=entry2_var)
entry2.grid(row=1, column=1, padx=(0, 50), pady=10, sticky='w')

Button(gui, text='Search', command=on_search).grid(row=1, column=1, padx=(200, 0), pady=(40), sticky='e')

options = ['Boolean Retrieval', 'VSM', 'Okapi BM25']
clicked = StringVar()
clicked.set('Boolean Retrieval')
OptionMenu(gui, clicked, *options).place(relx=0.5, rely=0.5, anchor=CENTER)

gui.mainloop()
