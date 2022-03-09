#!/usr/bin/env python

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[5]:


# Set executable path and browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[6]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[7]:


html = browser.html
news_soup = soup(html, 'html.parser')


# In[8]:


# we've assigned slide_elem as the variable to look for the <div /> 
# tag and its descendent (the other tags within the <div /> element)
# This is our parent element. This means that this element holds 
# all of the other elements within it, and we'll reference it when we want to filter search results even further
# The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag 
# with the class of list_text. CSS works from right to left, such as returning the last item on the list 
# instead of the first. Because of this, when using select_one, the first matching element returned will be a 
# <li /> element with a class of slide and all nested elements within it
slide_elem = news_soup.select_one('div.list_text')


# In[9]:


# we chained .find onto our previously assigned variable, slide_elem
# we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data."
# this shows us the full HTML
slide_elem.find('div', class_='content_title')


# In[10]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# get_text() was added -when this new method is chained onto .find(), only the text 
# of the element is returned. The code above, for example, would return only 
# the title of the news article and not any of the HTML tags or elements
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[11]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[12]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[13]:


# Find and click the full image button
# Notice the indexing chained at the end of the first line of code? 
# With this, we've stipulated that we want our browser to click the second button.
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[14]:


# With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[15]:


# Find the relative image url
# An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
# What we've done here is tell BeautifulSoup to look inside the <img /> tag for 
# an image with a class of fancybox-image. Basically we're saying, 
# "This is where the image we want lives—use the link that's inside these tags."

img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[16]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[17]:


# With this line, we're creating a new DataFrame from the HTML table. 
# The Pandas function read_html() specifically searches for and returns 
# a list of tables found in the HTML. By specifying an index of 0,
#  we're telling Pandas to pull only the first table it encounters, 
# or the first item in the list. Then, it turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# Assign column names to the new DataFrame for additional clarity.
df.columns=['description', 'Mars', 'Earth']

# By using the .set_index() function, we're turning the Description column into the
# DataFrame's index. inplace=True means that the updated index will remain in place, 
# without having to reassign the DataFrame to a new variable
df.set_index('description', inplace=True)
df


# ### Visit the NASA Mars News Site

# In[18]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[19]:


# Convert the browser html to a soup object 
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[20]:


slide_elem.find('div', class_='content_title')


# In[21]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[22]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[23]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[24]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[26]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[27]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[28]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[29]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[30]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


html = browser.html
html_soup = soup(html,'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
image_div = html_soup.find_all('div', class_='item')

 # Iterate through each image
for image_links in image_div:
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    link = image_links.find('a')
    href = link['href']
    title = image_links.find('img')
    title = title['alt']

    image_url = f'{url}{href}'
    browser.visit(image_url)

    html = browser.html

    subpage_soup = soup(html,'html.parser')

    jpg_image = subpage_soup.find('div', class_='wide-image-wrapper')
    a_html = jpg_image.find('a')
    full_image = a_html['href']
    full_image = f'{url}{full_image}'

    title = subpage_soup.find('div', class_='cover')
    title = title.find('h2').text
    
    hemisphere_image_urls.append({'img_url': full_image, 'title': title})
  


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[35]:


# 5. Quit the browser
browser.quit()

