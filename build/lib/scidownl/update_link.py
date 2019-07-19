# -*- coding: utf-8 -*-
"""Update available Scihub links

method 1: Crawling the website https://lovescihub.wordpress.com/
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


def update_link(mod='c'):
    LINK_FILE = open(get_resource_path('link.txt'), 'w', encoding='utf-8')
    print(STD_INFO + "Updating links ...")
    PATTERN = r">(htt[^:]+://sci-hub.[^</]+)<"
    if mod == 'c':
        # method 1: crawl the website.
        # src_url = "https://sci-hub.top/"
        src_url = "https://lovescihub.wordpress.com/"
        # src_url = "http://tool.yovisun.com/scihub/"
        html = requests.get(src_url).text
        available_links = re.findall(PATTERN, html)
        for link in available_links:
            if link[-3:] != "fun":
                print(STD_INFO + "%s" %(link))
                LINK_FILE.write(link + '\n')
    elif mod == 'b':
        # method 2: brute force search
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

        def basic_func(index, link):
            try:
                html = requests.get(link, timeout=6).content
                soup = BeautifulSoup(html, 'lxml')
                title = soup.title.contents[0]
                if title[:7] == "Sci-Hub":
                    print('\n' + STD_INFO + "%s" %(link))
                    LINK_FILE.write(link + '\n')
                else:
                    print("\r%spassing...".ljust(60) %(STD_INFO), end='')
            except:
                print("\r%spassing...".ljust(60) %(STD_INFO), end='')

        spider = MSpider(basic_func, get_url_list(), batch_size=10)
        spider.crawl()  
    LINK_FILE.close()

def get_resource_path(path):
    dir_path = os.path.dirname(__file__)
    dir_path = dir_path if dir_path else os.getcwd()
    return os.path.join(dir_path, path)


if __name__=="__main__":
    update_link()
