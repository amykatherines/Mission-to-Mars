
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # headless=False meansyou won't see the web app scraping actions
    browser = Browser('chrome', **executable_path, headless=False)

    # call the mars_news function
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html
    news_soup = soup(html, 'html.parser')

    # If there's an error, Python will continue to run the remainder of the code. 
    try: 
        # we've assigned slide_elem as the variable to look for the <div /> 
        # tag and its descendent (the other tags within the <div /> element)
        # This is our parent element. This means that this element holds 
        # all of the other elements within it, and we'll reference it when we want to filter search results even further
        # The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag 
        # with the class of list_text. CSS works from right to left, such as returning the last item on the list 
        # instead of the first. Because of this, when using select_one, the first matching element returned will be a 
        # <li /> element with a class of slide and all nested elements within it
        slide_elem = news_soup.select_one('div.list_text')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        # get_text() was added -when this new method is chained onto .find(), only the text 
        # of the element is returned. The code above, for example, would return only 
        # the title of the news article and not any of the HTML tags or elements
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    # If it runs into an AttributeError, Python will return nothing 
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
# ### Featured Images

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    # Notice the indexing chained at the end of the first line of code? 
    # With this, we've stipulated that we want our browser to click the second button.
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        # An img tag is nested within this HTML, so we've included it.
        # .get('src') pulls the link to the image.
        # What we've done here is tell BeautifulSoup to look inside the <img /> tag for 
        # an image with a class of fancybox-image. Basically we're saying, 
        # "This is where the image we want lives—use the link that's inside these tags."

        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    # ### Mars Facts
    try:
        # With this line, we're creating a new DataFrame from the HTML table. 
        # The Pandas function read_html() specifically searches for and returns 
        # a list of tables found in the HTML. By specifying an index of 0,
        #  we're telling Pandas to pull only the first table it encounters, 
        # or the first item in the list. Then, it turns the table into a DataFrame.
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
      return None
    
    # Assign column names to the new DataFrame for additional clarity.
    df.columns=['description', 'Mars', 'Earth']

    # By using the .set_index() function, we're turning the Description column into the
    # DataFrame's index. inplace=True means that the updated index will remain in place, 
    # without having to reassign the DataFrame to a new variable
    df.set_index('description', inplace=True)
    
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())