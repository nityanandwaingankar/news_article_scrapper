#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import numpy as np


# In[2]:


#requests module we can get the HTML content and save into the coverpage variable
url = 'https://www.theguardian.com/international'
r1 = requests.get(url)
coverpage = r1.content  #get content


# In[3]:


soup1 = BeautifulSoup(coverpage,'html.parser') #make a BS instance

coverpage_news = soup1.find_all('a',class_="u-faux-block-link__overlay js-headline-text")
#coverpage_news
#print(soup1.prettify())


# In[4]:


#final assembly
number_of_articles = len(coverpage_news) #make len later
# Empty lists for content, links and titles
news_contents = []
list_links = []
list_titles = []
list_dateTime= []
list_author = []


# In[5]:


for n in np.arange(0, number_of_articles):
    
    # only news articles (there are also albums and other things)
    #if "inenglish" not in coverpage_news[n].find('a')['href']:  
     #   continue
    
    # Getting the link of the article
    link = coverpage_news[n]['href']
    list_links.append(link)   #link of article
    
    # Getting the title
    title = coverpage_news[n].get_text()
    list_titles.append(title) #title of article
    
    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html.parser')
    
    try:
        auth = soup_article.find('a', rel = 'author')
        list_author.append(auth.get_text()) #get name of author

    except AttributeError:
        list_author.append("Editor") #get name of author
    
    paratext = soup_article.find_all('p')# steps for getting article
    
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(paratext)):
        paragraph = paratext[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    news_contents.append(final_article)
    


# In[6]:


#print(list_links)
#print(list_titles)
#print(list_author)

#for i in range(len(news_contents)):
 #   print('\n\n\n')
  #  print(news_contents[i])


# In[ ]:


#!pip install pymongo do in anaconda navigator
from pymongo import MongoClient 
client = MongoClient("mongodb+srv://test:test@cluster0.pyt3p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") #login to database as user


# In[ ]:


db = client.get_database('Article_database')
records = db.article_record  #pull collection from database


# In[ ]:


records.count_documents({})


# In[ ]:


new_students = []
for i in range(len(news_contents)):
    a_dict = {'title':list_titles[i],'link':list_links[i],'author':list_author[i],'content':news_contents[i]}
    dict_copy = a_dict.copy()
    new_students.append(dict_copy)
    #records.insert_one(new_student)
    
#new_students
records.insert_many(new_students) #push many records into the collection


# In[13]:


#making a csv file
main_list = []
for i in range(len(news_contents)):
    #print(len(news_contents))
    #temp_list = []
    temp_list = [list_titles[i],list_links[i],list_author[i],news_contents[i]]
    #print(temp_list)
    main_list.append(temp_list)
    


# In[15]:


import pandas as pd
my_array = np.array(main_list, dtype=object)
df = pd.DataFrame(my_array, columns = ['Title','url links','Author','Content'])


# In[16]:


df.to_csv (r'C:\Users\waing\Desktop\Scraper\export_dataframe.csv', index = False, header=True)


# In[17]:


#TO read a document from the collection
records.find_one{} 

records.find_one{'author':'Linda Geddes'}#find by author name

records.find_one({'title':'The ‘culture wars’ are a symptom, not the cause, of Britain’s malaise'})#find by title



