from splinter import Browser
from bs4 import BeautifulSoup # as soup
import pandas as pd
import datetime as dt
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def get_soup(browser, url):
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    return soup


def scrape():
    browser = init_browser()
    listings = {}

    url = "https://mars.nasa.gov/news/"

    browser.visit(url)
    time.sleep(1)

    html = browser.html

    soup = BeautifulSoup(html, "html.parser")

    listings["title"] = soup.find("div", class_="content_title").get_text().strip()
    listings["paragraph"] = soup.find("div", class_="article_teaser_body").get_text().strip()

    url = "https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    next_link = "https://www.jpl.nasa.gov" + soup.find("a", class_="group cursor-pointer block").get("href").strip()
    soup = get_soup(browser, next_link)

    listings["featured_img"] = soup.find("img", class_="BaseImage").get('src').strip()

    facts_url = "https://space-facts.com/mars/"
    soup = get_soup(browser, facts_url)
    table_content = soup.find("table", id="tablepress-p-mars-no-2")

    table_headers = []
    table_contentlist = []
    first = True

    for childTd in table_content.findAll("td"):
        if first == True:
            table_headers.append(childTd.text)
            first = False
        else:
            table_contentlist.append(childTd.text)
            first = True
    listings["table_headers"] = table_headers
    listings["table_content"] = table_contentlist

    next_link = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    soup = get_soup(browser, next_link)
    imgLinks = soup.findAll("a", class_="itemLink product-item")
    i = 0
    hemisphere_image_urls = []
    for imgl in imgLinks:
        if i % 2 == 1:
            i += 1
            continue
        i += 1
        img_url = "https://astropedia.astastrogeology.usgs.gov" + imgl.get("href").strip().replace("/search/map",
                                                                                                   "/download") + ".tif/full.jpg"
        title = imgl.get("href").strip().replace("enhanced", "").split("/")[-1].capitalize() + " Hemisphere"
        hemisphere_image_urls.append({"img_url": img_url, "title": title})

    listings["hemisphere_image_urls"] = hemisphere_image_urls
    browser.quit()
    return listings