# -*- coding: utf-8 -*-
"""Download paper to pdf through Scihub.
"""
import requests, os, sys, re
from bs4 import BeautifulSoup
from PIL import Image
from termcolor import colored

from .update_link import update_link, get_resource_path


STD_INFO = colored('[INFO] ', 'green')
STD_ERROR = colored('[ERROR] ', 'red')
STD_WARNING = colored('[WARNING] ', 'yellow')
STD_INPUT = colored('[INPUT] ', 'blue')

class SciHub(object):
    def __init__(self, doi, out='.'):
        self.doi = doi
        self.out = out
        self.sess = requests.Session()
        self.check()

    def check(self):
        if not os.path.isdir(self.out):
            os.mkdir(self.out)

    def check_title(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, " ", title)
        return new_title

    def read_available_links(self):
        print(STD_INFO + 'Reading available links of Scihub...')
        with open(get_resource_path('link.txt'), 'r') as f:
            self.scihub_url_list = [l[:-1] for l in f.readlines()]
        print(STD_INFO + "Successfully read available links of Scihub.")

    def update_link(self, mod='c'):
        update_link(mod)
        self.read_available_links()

    def find_pdf_in_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        self.pdf_url = soup.find('iframe', {'id': 'pdf'}).attrs['src'].split('#')[0]
        self.title = ' '.join(self._trim(soup.title.text.split('|')[1]).split('/'))
        print(STD_INFO + colored('PDF url', attrs=['bold']) + " -> \n\t%s" %(self.pdf_url))
        print(STD_INFO + colored('Article title', attrs=['bold']) + " -> \n\t%s" %(self.title))

    def is_captcha_page(self, res):
        if res.headers['Content-Type'] == "text/html; charset=UTF-8":
            return True
        return False

    def process_captcha_code(self, html):
        soup = BeautifulSoup(html, 'lxml')
        captcha_url_pre = '/'.join(self.pdf_url.split('/')[:3])
        captcha_img_url = captcha_url_pre + soup.find('img').attrs['src']
        with open('./captcha_code.jpg', 'wb') as img:
            img.write(self.sess.get(captcha_img_url).content)
        img = Image.open("./captcha_code.jpg")
        img.show()

        captcha_data = {}
        captcha_data['id'] = soup.find('input', {'type':'hidden', 'name':'id'}).attrs['value']
        print(STD_INPUT, end='')
        captcha_data['answer'] = input('Type the captcha: ')
        res = self.sess.post(self.pdf_url, data=captcha_data, stream=True)
        return res

    def download_pdf(self):
        print(STD_INFO + "Verifying...")
        res = self.sess.get(self.pdf_url, stream=True)
        while True:
            if self.is_captcha_page(res):
                print(STD_INFO + "Captcha is required.")
                html = res.content.decode('latin1')
                res = self.process_captcha_code(html)
            else:
                print(STD_INFO + "Verification success.")
                if os.path.isfile('./captcha_code.jpg'):
                    if sys.platform == 'win32':
                        os.system('del captcha_code.jpg')
                    else:
                        os.system('rm captcha_code.jpg')
                break

        tot_size = int(res.headers['Content-Length'])
        out_file_path = os.path.join(self.out, self.check_title(self.title) + '.pdf')
        downl_size = 0
        with open(out_file_path, 'wb') as f:
            for data in res.iter_content(chunk_size=512, decode_unicode=False):
                f.write(data)
                downl_size += len(data)
                perc = int(downl_size/tot_size*100)
                perc_disp = colored('[%3d%%] ' %(perc), 'green')
                print("\r{0}Progress: {1}KB / {2}KB".format(perc_disp, downl_size//1024, tot_size//1024), end='')
        print('\n' + STD_INFO + "Done.".ljust(50))

    def download(self):
        self.read_available_links()
        scihub_url_index = 0
        while True:
            if scihub_url_index >= len(self.scihub_url_list):
                print(STD_WARNING + 'All Scihub links are invalid.')
                print(STD_INPUT)
                update_req = input('Would you like to update Scihub links? (y/n): ')
                if update_req == 'y':
                    self.update_link(mod = 'c')
                    self.download()
                elif update_req == 'n':
                    print(STD_INFO + "Please manually update Scihub links by $scidownl -u")
                return

            url_pre = self.scihub_url_list[scihub_url_index]
            print(STD_INFO + 'Choose the available link %d: %s' %(scihub_url_index, url_pre))
            paper_url = '%s/%s' %(url_pre, str(self.doi))

            res = self.sess.get(paper_url)
            content = res.text
            if res.text in ['\n', ''] or res.status_code in [429]:
                print(STD_ERROR + "Current Scihub link is invalid, changing another link...")
                scihub_url_index += 1
            else:
                break

        try:
            self.find_pdf_in_html(content)
            self.download_pdf()
        except:
            print(STD_ERROR + "Failed to access the article.")

    def _trim(self, s):
        """Drop spaces located in the head or the end of the given string.
        """
        if len(s) == 0:
            return s
        elif s[0] == ' ':
            return self._trim(s[1:])
        elif s[-1] == ' ':
            return self._trim(s[:-1])
        else:
            return s


if __name__=="__main__":
    a = SciHub('https://doi.org/10.5539/cis.v4n4p72', 'paper')
    # a = SciHub('https://doi.org/10.1101/cshperspect.a023812', 'paper')
    a.download()
