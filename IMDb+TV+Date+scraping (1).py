
# coding: utf-8

# In[12]:

#To Do:
#Iterate over multiple TT codes
# Missing dot in date field format code

import unicodecsv as csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup


# In[13]:

#ttcode = "tt0460681"
ttcode = str(raw_input('Type/paste IMDb tt code:'))

#Determine number of seasons
mainurl = "http://www.imdb.com/title/%s/" % (ttcode)
seasons = 1
seasoncount = 1

rmain = requests.get(mainurl)
soup = BeautifulSoup(rmain.content, "lxml")


# In[14]:

#Total available seasons
titles = soup.findAll("div",{"class": "seasons-and-year-nav"})
seriesname = soup.findAll("h1",{"itemprop":"name"})[0].text
seriesname = seriesname.strip()

#Grabs TV series name to store for csv filename
filename = ''.join(e for e in seriesname if e.isalnum()) +" TV Data Export.csv"

seasons = int(titles[0].findAll("a")[0].text)


# In[15]:

#Write file with column headers
with open(filename, 'w') as csvfile:
    w = csv.writer(csvfile)
    w.writerow(['Series', 'Season', 'Episode', 'Title', 'Air Date', 'Description'])
    csvfile.close


# In[16]:

#For each season until seasoncount exceeds total seasons
while (seasoncount < (seasons)):
    
    #Scrape data from TV season page
    url = "http://gb.imdb.com/title/%s/episodes?season=%s" % (ttcode, seasoncount)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")
    titles = soup.findAll("div",{"class": "info"})

    #Find episode data snd store in variables
    seriestitle = [seriesname for i in titles]
    episodetitle = [i.findAll("a",{"itemprop":"name"})[0].text for i in titles]
    
    episodedate = [i.findAll("div",{"class":"airdate"})[0].text for i in titles]
    episodedate = [w.strip().replace('.','') for w in episodedate]
    episodedate = [datetime.strptime(w, '%d %b %Y').date() for w in episodedate]
    
    episodedesc = [i.findAll("div",{"itemprop":"description"})[0].text for i in titles]
    episodedesc = [w.replace('\n', '') for w in episodedesc]
    episodedesc = [w.strip() for w in episodedesc]
    
    seasonnumber = [seasoncount for i in titles]
    
    episodenumber = [i.find("meta").attrs['content'] for i in titles]
    
    #Combine variables into a set
    l = [i for i in zip(seriestitle, seasonnumber, episodenumber, episodetitle, episodedate, episodedesc)]

    #Add all sets to csv file
    with open(filename, 'a') as csvfile:
        w = csv.writer(csvfile)
        for i in l:
            w.writerow(i)
    
    #increment the counter        
    seasoncount = seasoncount + 1


# In[17]:

#For final season
  
#Scrape data from TV season page
url = "http://gb.imdb.com/title/%s/episodes?season=%s" % (ttcode, seasoncount)
r = requests.get(url)


# In[18]:

#Find final season first episode name
soup = BeautifulSoup(r.content, "lxml")
firstepname = soup.findAll("a",{"itemprop":"name"})[0]

#Check if final season has episode titles - if not, skip the season
if firstepname.text != "Episode #%s.1" %(seasoncount):
    
    titles = soup.findAll("div",{"class": "info"})

    #Find episode data and store in variables
    seriestitle = [seriesname for i in titles]
    episodetitle = [i.findAll("a",{"itemprop":"name"})[0].text for i in titles]
    
    episodedate = [i.findAll("div",{"class":"airdate"})[0].text for i in titles]
    episodedate = [w.strip().replace('.','') for w in episodedate]
    episodedate = [datetime.strptime(w, '%d %b %Y').date() for w in episodedate]
    
    episodedesc = [i.findAll("div",{"itemprop":"description"})[0].text for i in titles]
    episodedesc = [w.replace('\n', '') for w in episodedesc]
    episodedesc = [w.strip() for w in episodedesc]
    
    seasonnumber = [seasoncount for i in titles]
    
    episodenumber = [i.find("meta").attrs['content'] for i in titles]
    
    #Combine variables into a set
    l = [i for i in zip(seriestitle, seasonnumber, episodenumber, episodetitle, episodedate, episodedesc)]

    #Add all sets to csv file
    with open(filename, 'a') as csvfile:
        w = csv.writer(csvfile)
        for i in l:
            w.writerow(i)
        csvfile.close

