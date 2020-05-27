from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import re
import time


def InitBrowser():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    return browser

def ScrapeMars():
    marsData = {}
    browser = InitBrowser()

    marsData['news'] = GetNews(browser)
    marsData['image'] = GetImage(browser)
    marsData['weather'] = GetWeather(browser)
    marsData['facts'] = GetFacts(browser)
    marsData['hemispheres'] = GetHemispheres(browser)

    browser.quit()

    return marsData



def GetNews(browser):
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    time.sleep(1)

    soup = bs(browser.html, 'lxml')

    article = soup.find('div', class_ = 'list_text')

    title = article.find('a').text

    summary = article.find('div', class_ = "article_teaser_body").text

    return {'title': title, 'summary': summary}

def GetImage(browser):
    featuredImageUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(featuredImageUrl)
    time.sleep(1)
    
    imageSoup = bs(browser.html, 'lxml')

    featuredImgUrl = 'https://www.jpl.nasa.gov/' + imageSoup.find('footer').find('a')['data-fancybox-href']

    return {'url': featuredImgUrl}

def GetWeather(browser):
    twitterUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterUrl)
    
    time.sleep(5)

    twitterSoup = bs(browser.html, 'lxml')

    tweets = twitterSoup.find_all('div', attrs = {'data-testid': 'tweet'})
    for tweet in tweets:
        weather = tweet.find('div', class_ = 'r-bnwqim')
        weatherText = weather.find('span').text
        if 'InSight' in weatherText:
            break

    return weatherText

def GetFacts(browser):
    factsUrl = 'https://space-facts.com/mars/'

    facts = pd.read_html(factsUrl)

    dfFacts = facts[0]

    dfFacts.columns = ['Stat', 'Value']
    dfFacts.set_index('Stat', inplace = True)
    
    factsHtml = dfFacts.to_html()

    return factsHtml

def GetHemispheres(browser):
    hemiUrl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemiUrl)
    
    time.sleep(1)

    hemiSoup = bs(browser.html, 'lxml')

    lHemispheres = []

    hemispheres = hemiSoup.find_all('div', class_ = 'description')

    baseUrl = 'https://astrogeology.usgs.gov'

    for hemi in hemispheres:
        browser.visit(hemiUrl)
        
        dictHemi = {}
        dictHemi['title'] = (hemi.find('h3').text).replace(' Enhanced', '')
        
        browser.click_link_by_partial_text(dictHemi['title'])
        
        hemiSoup2 = bs(browser.html, 'lxml')
        
        dictHemi['img_url'] = hemiSoup2.find('div', class_ = 'downloads').find('a')['href']
        
        lHemispheres.append(dictHemi)

    return lHemispheres