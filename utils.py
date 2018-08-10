
# coding: utf-8

# In[2]:


import urllib.robotparser as rp
import requests
import re
from bs4 import BeautifulSoup  # for scraping
from pprint import pprint  # pretty printing
from itertools import chain


from textblob import TextBlob, Word
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords, wordnet
import wikipedia


# In[3]:


parser = rp.RobotFileParser()
def robot_checker(url, base, agent="*"):
    parser.set_url(base+"/robots.txt")
    parser.read()
    if parser.can_fetch(url, agent)==True:
        return requests.get(url)
    else:
        print("sorry, but you are not allowed to scrape this page.")


# In[8]:


class ScrapeAll:
    def __init__(self, url):
        response = requests.get(url)
        self.url = url
        page = response.content
        self.page = BeautifulSoup(page, "html.parser")

    def hyperlinks(self):
        links = self.page.find_all("a")
        hyperlinks = []
        for i in links:
            h = i.get("href")
            if h is None:
                continue
            if h.startswith("http"):
                hyperlinks.append(h)
            else:
                hyperlinks.append(self.url + h)
        return hyperlinks

    def h_p(self):
        h = self.page.find_all(re.compile("h[1-6]|p"))
        head_par = [i.get_text() for i in h]
        return "\n".join(head_par)

    def get_tags(self, tag):
        return [i.get_text() for i in self.page.select(tag)]


# In[18]:


class SuperList:
    def __init__(self, list):
        self.list = list

    def unlist(self):
        return list(chain.from_iterable(self.list))

    def merge(self):
        return " ".join([str(i) for i in self.list])

    def find(self, type):
        t = []
        for i in self.list:
            if type == "number" and str(i).isdigit():
                t.append(i)
            if type == "letter" and str(i).isalpha():
                t.append(i)
        return t


# In[22]:


class Cleaner:
    def __init__(self, str):
        self.str = TextBlob(str)

    def get_words(self):
        return self.str.words

    def get_sentences(self):
        return self.str.sentences

    def lemmatize(self):
        return [w.lemmatize() for w in self.str.words]

    def clean_stopwords(self):
        sw = stopwords.words("english")
        return [i for i in self.str.words if i not in sw]

    def uppercase(self):
        return [w.upper() for w in self.str.words]

    def lowercase(self):
        return [w.lower() for w in self.str.words]

    def freq_dist(self):
        nltk.FreqDist(self.clean_stopwords()).plot(50, cumulative=True)


# In[32]:


py = wikipedia.page("Python programming language")


# In[36]:


s = ScrapeAll(py.url)
pprint(s.hyperlinks())


# In[37]:


pprint(s.get_tags("ol.references > li"))


# In[41]:


pprint(s.h_p())


# In[43]:


sl = SuperList(wikipedia.search("python"))
pprint(sl.merge())


# In[44]:


pprint(wikipedia.summary("Facebook", sentences=10))


# In[45]:


pprint(wikipedia.search("python"))


# In[47]:


c = Cleaner(py.content)
pprint(c.freq_dist())

