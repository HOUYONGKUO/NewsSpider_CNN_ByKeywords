'''
copyright @HOUYONGKUO
Created on 2022/07/19
Crawl CNN news based on keywords
'''

import os
import re
import bs4
import time
import math
import json
import requests
from tqdm import tqdm
from selenium import webdriver


def getPageList(driver, keywords):
    """
    Get news pages by keywords
    """

    # CNN (USA)
    # Sections = us,politics,world,opinion,health/business/entertainment/sport/travel/style, if all CNN just no section
    url = 'https://edition.cnn.com/search?size=10&q=' + keywords + '&sections=us,politics,world,opinion,health' + '&types=article' + '&sort=relevance'

    # Jump to the URL
    driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    # CNN headlines with news hyperlinks
    pageList = soup.select('h3.cnn-search__result-headline')
    linkList = []

    # Get the number of related news
    str_ = soup.find('div', attrs={'class': 'cnn-search__results-count'})
    number = re.findall(r'\d+', str_.contents[0])
    num = int(number[2])
    page_num = int(math.ceil(num / 10))
    print(f'A total of {num} news related to the keyword {keywords} were retrieved, totaling {page_num} pages')

    # TODO: If the data is more than 200, only the first 200 will be retrieved
    if num > 200:
        num = 200
        page_num = int(math.ceil(num / 10))
        print(f'Due to the large amount of data, only the first 200 are collected, totaling {page_num} pages')

    # Start time
    time_start = time.time()

    # Get news on page 1
    remove_livenews = re.compile(r'live-news')
    remove_interactive = re.compile(r'interactive')
    print(f'Start collecting news on page 1 about {keywords}')
    for page in pageList:
        link = page.a["href"]
        # Delete the news link about live-news and interactive
        if remove_livenews.search(link):
            pass
        elif remove_interactive.search(link):
            pass
        else:
            url_full = 'https:' + link
            linkList.append(url_full)

    # Get the second page and the following related news URLs
    # The second page and later URLs will be added to the page number-related parts, they are processed separately
    for i in range(2, page_num + 1):
        print(f'Start collecting news on page {i} about {keywords}')
        url_flipover = url + f'&from={(i - 1) * 10}' + f'&page={i}'
        driver.get(url_flipover)
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        pageList = soup.select('h3.cnn-search__result-headline')
        for page in pageList:
            link = page.a["href"]
            # Delete the news link about live-news and interactive
            if remove_livenews.search(link):
                pass
            elif remove_interactive.search(link):
                pass
            else:
                url_full = 'https:' + link
                linkList.append(url_full)

    # End time
    time_end = time.time()
    # Total search time
    time_c = time_end - time_start
    print('Total search time', '%.2f' % time_c, 's')
    return linkList


def check(string, sub_str):
    if string.find(sub_str) == -1:
        return False
    else:
        return True


def getImgList(soup):
    '''
    To get news images url list
    '''
    images = soup.find_all('img', class_='media__image owl-lazy')
    imglist = ''
    for i in images:
        image = i.get("src")
        # The link in the source code is missing ’http:‘ at the beginning, so we have to add it ourselves
        # TODO: Some webpages crawl thumbnails, if there is another way please add a new rule
        # Restore Thumbnails to Larger
        if check(image, 'topics') is True:
            image = image.replace('topics', 'horizontal-large-gallery')
        if check(image, 'small-11') is True:
            image = image.replace('small-11', 'exlarge-169')
        image = 'http:' + image
        # print(image)
        imglist = image + ','
    return imglist


def getContent(url, keywords):
    '''
    To get news content including date, title, text content and image
    '''

    # Set driver and url
    driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    # Get news date
    date = "".join(list(filter(str.isdigit, url)))

    # Get news title
    # TODO: The title containing ' will output \' , it may be a problem with json storage
    title = soup.h1.text
    # print(title)

    # Get text content
    pList_1 = soup.find_all("div", class_="el__leafmedia el__leafmedia--sourced-paragraph")
    pList_2 = soup.find_all("div", class_="zn-body__paragraph")

    content = ''
    for p1 in pList_1:
        content += p1.text + r'\n'
    for p2 in pList_2:
        content += p2.text + r'\n'
    # print(content)

    # Get image list
    image = getImgList(soup)

    # # Set text format to save
    data = {
        'ID': keywords,
        'Date': date,
        'Title': title,
        'Content': content,
        'URL': url,
        'Image': image,
    }
    return data, image


def saveFile(data, image, path, filename):
    # If file path is none to create file
    if not os.path.exists(path):
        os.makedirs(path)

    # Save file
    with open(path + filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    # Save image file
    if len(image) != 0:
        i = 1
        for p in image:
            image_path = path + filename
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            with open(image_path + f'/{filename}_img_{i}.jpg', 'wb') as f:
                r = requests.get(p)
                r.raise_for_status()
                f.write(r.content)
                f.close()
                i += 1


def download_CNNNews_by_keywords(driver, keyword, savedir):
    # Set 2nd-class keyword
    kwlist = {''}
    print(f'\nkeywords include: {kwlist}, total: {len(kwlist)}')
    for i in range(len(kwlist)):
        for kw in kwlist:
            keywords = keyword + kw
            print(f'=====================Now, retrieve {i + 1}/{len(kwlist)} keywords：{keywords}=====================')

            time_start = time.time()
            pageList = getPageList(driver, keywords)

            print(f'=====================Now, start to save news content about {keywords}=====================')
            print(f'Remove live-news and interactive, remaining: {len(pageList)} news, now start to save')
            for n in tqdm(range(99, len(pageList)), desc="Save news content: "):
                # Set save path and save filename
                path = savedir + '/' + 'NewsClassificationDataset' + '/' + keywords + '/'
                fileName = keywords + '_' + str(n + 1)

                # Get news content
                content, image = getContent(pageList[n], keywords)

                # The crawler is too fast to be found easily, rest for 1s.
                time.sleep(1)

                # Save file
                saveFile(content, image, path, fileName)

            # End time
            time_end = time.time()

            # Time consuming
            time_c = time_end - time_start
            print(f'Results:{i + 1}/{len(kwlist)} keywords：{keywords}, time consuming：', '%.2f' % time_c, 's')

            # Quit driver and close all windows
            driver.quit()


if __name__ == '__main__':
    '''
    main function
    '''
    # Web crawler by keyword
    keyword = ""
    savedir = ""

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-site-isolation-trials")
    driver = webdriver.Chrome(chrome_options=options)
    download_CNNNews_by_keywords(driver, keyword, savedir)
    print("=====================Congratulations on completing the CNN News web crawler!=====================")
