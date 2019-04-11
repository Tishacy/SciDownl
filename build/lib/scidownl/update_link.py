# -*- coding: utf-8 -*-
"""Update available Scihub links

method 1: Crawling the website https://sci-hub.top, which updates available Scihub links every 30 mins.
method 2: Brute force search
"""
import string, requests, re, os
from bs4 import BeautifulSoup
from mspider.spider import MSpider
from termcolor import colored

LETTERS = list(string.ascii_lowercase)
STD_INFO = colored('[INFO] ', 'green')
STD_ERROR = colored('[ERROR] ', 'red')
STD_WARNING = colored('[WARNING] ', 'yellow')
STD_INPUT = colored('[INPUT] ', 'blue')

def get_url_list():
    url_list = []
    url_pre = 'http://sci-hub.'
    url_pre2 = 'https://sci-hub.'
    for first_letter in LETTERS:
        for last_letter in LETTERS:
            url = url_pre + first_letter + last_letter
            url2 = url_pre2 + first_letter + last_letter
            url_list.extend([url, url2])
    return url_list

def basic_func(index, url):
    try:
        html = requests.get(url, timeout=3).content
        soup = BeautifulSoup(html, 'lxml')
        title = soup.title.contents[0]
        if title[:7] == "Sci-Hub":
            print("\n%s%s" %(STD_INFO, url))
            LINK_FILE.write(url + '\n')
        else:
            print("\r%spassing...".ljust(60) %(STD_INFO), end='')
    except:
        print("\r%spassing...".ljust(60) %(STD_INFO), end='')

def update_link(mod='c'):
    LINK_FILE = open(get_resource_path('link.txt'), 'w', encoding='utf-8')
    print(STD_INFO + "Updating links ...")
    if mod == 'c':
        html = requests.get("https://sci-hub.top/").content.decode()
        pattern = r">(htt[^:]+://sci-hub.[^<]+)<"
        available_links = re.findall(pattern, html)
        for link in available_links:
            print(STD_INFO + "%s" %(link))
            LINK_FILE.write(link + '\n')
    elif mod == 'b':
        spider = MSpider(basic_func, get_url_list(), batch_size=18)
        spider.crawl()
    LINK_FILE.close()

def get_resource_path(path):
    dir_path = os.path.dirname(__file__)
    dir_path = dir_path if dir_path else os.getcwd()
    return os.path.join(dir_path, path)


if __name__=="__main__":
    update_link()
