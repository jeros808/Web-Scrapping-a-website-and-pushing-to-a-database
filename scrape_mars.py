
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
import time
import requests
from splinter import Browser
def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = False)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    htmlstuff = browser.html
    soup = BeautifulSoup(htmlstuff, "html.parser")
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text



    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')


    image_html = browser.html

    soup = BeautifulSoup(image_html, "html.parser")

    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path


    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)

    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    soup = BeautifulSoup(facts_html, 'html.parser')

    table_data = soup.find('table', class_="tablepress tablepress-id-mars")
    table_all = table_data.find_all('tr')


    labels = []
    values = []

    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
            

    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })


    fact_table = mars_facts_df.to_html(header = False, index = False)
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    usgs_html = browser.html

    soup = BeautifulSoup(usgs_html, "html.parser")

    returns = soup.find('div', class_="collapsible results")
    hemispheres = returns.find_all('a')

    hem_image_urls =[]

    for a in hemispheres:
       
        title = a.h3
        link = "https://astrogeology.usgs.gov" + a['href']
        
        browser.visit(link)
        time.sleep(5)

        image_page = browser.html
        results = BeautifulSoup(image_page, 'html.parser')
        img_link = results.find('div', class_='downloads').find('li').a['href']
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = img_link
        
        hem_image_urls.append(image_dict)
        

    mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_images": hemisphere_image_urls
    }
    return mars_dict
