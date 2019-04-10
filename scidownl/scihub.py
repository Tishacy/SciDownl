# -*- coding: utf-8 -*-
"""Download paper to pdf through Scihub.
"""
import requests, wget
from bs4 import BeautifulSoup
from PIL import Image

class SciHub(object):
    def __init__(self, doi, out):
        self.doi = doi
        self.out = out
        self.sess = requests.Session()

    def read_available_links(self):
        print('[INFO]: Reading available links of Scihub...')
        with open('./link.txt', 'r') as f:
            self.scihub_url_list = [l[:-1] for l in f.readlines()]
        print("[INFO]: Successfully read available links of Scihub.")

    def update_links(self, mod='c'):
        pass

    def find_pdf_in_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        self.pdf_url = soup.find('iframe', {'id': 'pdf'}).attrs['src'].split('#')[0]
        self.title = ' '.join(self._trim(soup.title.text.split('|')[1]).split('/'))
        print("[INFO]: PDF url -> \n\t%s" %(self.pdf_url))
        print("[INFO]: Article title -> \n\t%s" %(self.title))

    def is_validation_page(self, html):
        try:
            BeautifulSoup(html, 'lxml').find('img', {'id':'captcha'}).attrs
            return True
        except:
            return False

    def process_validation_code(self, html):
        soup = BeautifulSoup(html, 'lxml')
        validation_url_pre = '/'.join(self.pdf_url.split('/')[:3])
        validation_img_url = validation_url_pre + soup.find('img').attrs['src']
        with open('./validation_code.jpg', 'wb') as img:
            img.write(self.sess.get(validation_img_url).content)
        img = Image.open("./validation_code.jpg")
        img.show()

        validation_data = {}
        validation_data['id'] = soup.find('input', {'type':'hidden', 'name':'id'}).attrs['value']
        validation_data['answer'] = input('[INPUT]: Type the validation code: ')
        self.sess.post(self.pdf_url, data=validation_data)
        print("[INFO]: Post the validation code data.")

    def download_pdf(self):
        res = self.sess.get(self.pdf_url)
        html = res.content.decode('latin1')
        if self.is_validation_page(html):
            print("[INFO]: Validation code is required.")
            self.process_validation_code(html)
        print("[INFO]: Downloading...")
        wget.download(self.pdf_url, out='%s/%s.pdf' %(self.out, self.title))

    def download(self):
        scihub_url_index = 0
        while True:
            if scihub_url_index >= len(self.scihub_url_list):
                print('[WARNING]: All Scihub links are invalid.')
                update_req = input('[INPUT]: Would you like to update Scihub links? (y/n): ')
                if update_req == 'y':
                    self.update_links(mod = 'c')
                    self.download()
                elif update_req == 'n':
                    print("[INFO]: Please manually update Scihub links by $????")
                return

            url_pre = self.scihub_url_list[scihub_url_index]
            print('[INFO]: Choose the available link %d: %s' %(scihub_url_index, url_pre))
            paper_url = '%s/%s' %(url_pre, str(self.doi))

            res = self.sess.get(paper_url)
            content = res.content.decode('utf-8')
            if content in ['\n', '']:
                print("[ERROR]: Current Scihub link is invalid, changing another link...")
                url_index += 1
            else:
                break

        # try:
        self.find_pdf_in_html(content)
        self.download_pdf()
        # except:
        #     print("[ERROR]: Failed to access the article.")

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
    # a = SciHub('10.1039/C1CS15065K', '.')
    a = SciHub('https://doi.org/10.1016/S0040-4020(01)89282-6', '.')
    a.read_available_links()
    print(a.scihub_url_list)
    a.download()
