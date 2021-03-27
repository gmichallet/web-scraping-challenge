#!/usr/bin/env python
# coding: utf-8

# In[26]:


# Dependencies and Setup
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the NASA Mars News Site
url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[4]:


# Parse Results HTML with BeautifulSoup
# Find Everything Inside:
#   <ul class="item_list">
#     <li class="slide">

html = browser.html
news_soup = bs(html, "html.parser")
slide_element = news_soup.select_one("ul.item_list li.slide")


# In[5]:


slide_element.find("div", class_="content_title")


# In[6]:


# Scrape the Latest News Title

news_title = slide_element.find("div", class_="content_title").get_text()
print(news_title)


# In[7]:


# Scrape the Latest Paragraph Text
news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
print(news_paragraph)


# In[8]:


# FEATURED IMAGE
# NASA JPL Site
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


url = 'https://www.jpl.nasa.gov/spaceimages/'
browser.visit(url)


# In[10]:


# Create a Beautiful Soup object
html = browser.html
soup = bs(html, 'html.parser')


# In[11]:


#Get the images
images = soup.findAll('img')
example = images[0]
example


# In[12]:


# Use Base URL to Create Absolute URL
img_url = f"https://www.jpl.nasa.gov{images}"
print(img_url)


# In[13]:


#MARS WEATHER

url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)


# In[15]:


# HTML Object 
html_weather = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html_weather, 'html.parser')

# Find elements that contain tweets
latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

# Retrieve all elements that contain news title in the specified range
# Look for entries that display weather related words to exclude non weather related tweets 
for tweet in latest_tweets: 
    weather_tweet = tweet.find('p').text
    if 'Sol' and 'pressure' in weather_tweet:
        print(weather_tweet)
        break
    else: 
        pass


# In[19]:


#MARS FACTS

# Visit Mars facts url 
facts_url = 'http://space-facts.com/mars/'

# Use Panda's `read_html` to parse the url
mars_facts = pd.read_html(facts_url)

# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
mars_df = mars_facts[0]

# Assign the columns `['Description', 'Value']`
mars_df.columns = ['Description','Value']

# Set the index to the `Description` column without row indexing
mars_df.set_index('Description', inplace=True)

# Save html code to folder Assets
mars_df.to_html()

data = mars_df.to_dict(orient='records')  

# Display mars_df
mars_df


# In[30]:


#MARS HEMISPHERES

# Go to hemisphere website through splinter module 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[31]:


hemisphere_image_urls = []

# Get a List of All the Hemispheres
links = browser.find_by_css("a.product-item h3")
for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
    hemisphere_image_urls.append(hemisphere)
    
    # Navigate Backwards
    browser.back()


# In[32]:


hemisphere_image_urls


# In[ ]:




