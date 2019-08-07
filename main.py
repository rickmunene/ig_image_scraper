import os
import re
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


def get_image_urls(username):
    links = []
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(
        '/Users/jordon/Downloads/chromedriver', options=options)
    browser.get('https://www.instagram.com/' + username + '/?hl=en')
    Pagelength = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    print('Please wait, scrolling now.')
    # Infinte Scroll until reaches very bottom
    match = False
    while(match == False):
        lastCount = lenOfPage

        # Get image links while scrolling (doesn't work otherwise)
        source = browser.page_source
        data = bs(source, 'html.parser')
        body = data.find('body')
        script = body.find('span')
        for link in script.findAll('a'):
            if re.match("/p", link.get('href')):
                links.append('https://www.instagram.com' + link.get('href'))
        time.sleep(3)
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            source = browser.page_source
            data = bs(source, 'html.parser')
            body = data.find('body')
            script = body.find('span')
            for link in script.findAll('a'):
                if re.match("/p", link.get('href')):
                    links.append('https://www.instagram.com' +
                                 link.get('href'))
            match = True
    return links


def download_images():
    username = input('Enter instagram username to scrape: ')
    links = get_image_urls(username)
    images = list(dict.fromkeys(links))
    print(len(images), 'total images.')
    folder_name = input('Enter directory name to save images: ')
    os.mkdir(folder_name)
    for x in images:
        file_name = x.split('/')[-2]
        fullfilename = os.path.join(folder_name, file_name + '.jpg')
        test = requests.get(x)
        html = test.text
        data = bs(html, 'html.parser')
        image = data.find('meta', property='og:image')
        image_url = image['content']
        urllib.request.urlretrieve(image_url, fullfilename)


def main():
    download_images()


if __name__ == '__main__':
    main()
