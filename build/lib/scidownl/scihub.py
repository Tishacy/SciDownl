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
        self.check_out_path()
        self.read_available_links()

    def check_out_path(self):
        if not os.path.isdir(self.out):
            os.mkdir(self.out)

    def read_available_links(self):
        with open(get_resource_path('link.txt'), 'r') as f:
            self.scihub_url_list = [l[:-1] for l in f.readlines()]

    def update_link(self, mod='c'):
        update_link(mod)
        self.read_available_links()
    
    def use_scihub_url(self, index):
        self.scihub_url = self.scihub_url_list[index]
        print(STD_INFO + 'Choose the available link %d: %s' %(index, self.scihub_url))
        if self.scihub_url[-3:] == "red":
            self.scihub_url = self.scihub_url.replace('red', 'tw')

    def download(self, choose_scihub_url_index=-1):
        """Download the pdf of self.doi to the self.out path.
        
        params:
            choose_scihub_url_index: (int) 
                -1: Auto-choose the scihub urls.
                >=0: index of scihub url in scihub url links.
        """

        # Auto choose scihub urls.
        if choose_scihub_url_index == -1:
            # Check valid scihub urls
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
                        return print(STD_INFO + "Please manually update Scihub links by $scidownl -u")

                self.use_scihub_url(scihub_url_index)
                scihub_paper_url = '%s/%s' %(self.scihub_url, str(self.doi))
                res = self.sess.get(scihub_paper_url, stream=True)
                if res.text in ['\n', ''] or res.status_code in [429, 404]:
                    print(STD_ERROR + "Current Scihub link is invalid, changing another link...")
                    scihub_url_index += 1
                else:
                    break
        else:
            self.use_scihub_url(choose_scihub_url_index)
            scihub_paper_url = '%s/%s' %(self.scihub_url, str(self.doi))
            res = self.sess.get(scihub_paper_url, stream=True)

        if self.is_captcha_page(res) or res.headers['Content-Type'] == 'application/pdf':
            pdf = {
                'pdf_url': scihub_paper_url,
                'title': self.check_title(self.doi)
            }
            print(STD_INFO + colored('PDF url', attrs=['bold']) + " -> \n\t%s" %(pdf['pdf_url']))
            print(STD_INFO + colored('Article title', attrs=['bold']) + " -> \n\t%s" %(pdf['title']))
        else:
            pdf = self.find_pdf_in_html(res.text)

        self.download_pdf(pdf)
        # try:
        #     pdf = self.find_pdf_in_html(res.text)
        #     self.download_pdf(pdf)
        # except:
        #     print(STD_ERROR + "Failed to access the article.")

    def find_pdf_in_html(self, html):
        """Find pdf url and title in a scihub html

        params:
            html: (str) scihub html in string format.

        returns:
            (dict) {
                'pdf_url': (str) real url of the pdf.
                'title': (str) title of the article.
            }
        """
        pdf = {}
        soup = BeautifulSoup(html, 'html.parser')
        
        pdf_url = soup.find('iframe', {'id': 'pdf'}).attrs['src'].split('#')[0]
        pdf['pdf_url'] = pdf_url.replace('https', 'http') if 'http' in pdf_url else 'http:' + pdf_url
        
        title = ' '.join(self._trim(soup.title.text.split('|')[1]).split('/')).split('.')[0]
        title = title if title else pdf['pdf_url'].split('/')[-1].split('.pdf')[0]
        pdf['title'] = self.check_title(title)
        print(STD_INFO + colored('PDF url', attrs=['bold']) + " -> \n\t%s" %(pdf['pdf_url']))
        print(STD_INFO + colored('Article title', attrs=['bold']) + " -> \n\t%s" %(pdf['title']))
        return pdf

    def check_title(self, title):
        """Check title to drop invalid characters.
        
        params:
            title: (str) original title.
        
        returns:
            (str) title that drops invalid chars.
        """
        rstr = r"[\/\\\:\*\?\"\<\>\|]" # / \ : * ? " < > |
        new_title = re.sub(rstr, " ", title)[:200]
        return new_title

    def download_pdf(self, pdf):
        """Download the pdf by given a pdf dict.

        params:
            pdf: (dict) {
                'pdf_url': (str) real url of the pdf,
                'title': (str) title of the article
            }
        """
        print(STD_INFO + "Verifying...")
        res = self.sess.get(pdf['pdf_url'], stream=True)
        while True:
            if self.is_captcha_page(res):
                print(STD_INFO + "Captcha is required.")
                html = res.content.decode('latin1')
                res.close()
                res = self.process_captcha_code(html, pdf)
            else:
                print(STD_INFO + "Verification success.")
                if os.path.isfile('./captcha_code.jpg'):
                    if sys.platform == 'win32':
                        os.system('del captcha_code.jpg')
                    else:
                        os.system('rm captcha_code.jpg')
                break

        retry_times = 0
        while 'Content-Length' not in res.headers and retry_times < 10:
            print('\r' + STD_INFO + "Retrying...", end="")
            res.close()
            res = self.sess.get(pdf['pdf_url'], stream=True)
            retry_times += 1
        tot_size = int(res.headers['Content-Length']) if 'Content-Length' in res.headers else 0
        out_file_path = os.path.join(self.out, pdf['title']+'.pdf')
        downl_size = 0
        with open(out_file_path, 'wb') as f:
            for data in res.iter_content(chunk_size=1024, decode_unicode=False):
                f.write(data)
                downl_size += len(data)
                if tot_size != 0:
                    perc = int(downl_size/tot_size*100)
                    perc_disp = colored('[%3d%%] ' %(perc), 'green')
                else:
                    perc_disp = colored(STD_INFO)
                print("\r{0}Progress: {1} / {2}".format(perc_disp, downl_size, tot_size), end='')
        print('\n' + STD_INFO + "Done.".ljust(50))

    def is_captcha_page(self, res):
        """Check if the result page is a captcha page."""
        return 'must-revalidate' in res.headers['Cache-Control']
        # return res.headers['Content-Type'] == "text/html; charset=UTF-8"

    def process_captcha_code(self, html, pdf):
        """Process the html text of captcha page."""
        soup = BeautifulSoup(html, 'html.parser')
        captcha_url_pre = '/'.join(pdf['pdf_url'].split('/')[:3])
        captcha_img_url = captcha_url_pre + soup.find('img').attrs['src']
        with open('./captcha_code.jpg', 'wb') as img:
            img.write(self.sess.get(captcha_img_url).content)
        img = Image.open("./captcha_code.jpg")
        img.show()

        captcha_data = {}
        captcha_data['id'] = soup.find('input', {'type':'hidden', 'name':'id'}).attrs['value']
        print(STD_INPUT, end='')
        captcha_data['answer'] = input('Type the captcha: ')
        res = self.sess.post(pdf['pdf_url'], data=captcha_data, stream=True)
        return res

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
    test_dois = [
        '10.1093/oxfordjournals.jmicro.a023417',
        # '10.1002/chin.197335038',
        # 'https://doi.org/10.1097/00010694-193910000-00022',
        # 'https://doi.org/10.1097/00010694-197704000-00011',
        # 'https://doi.org/10.1016/b978-0-444-81490-6.50054-6',
        # 'https://doi.org/10.1097/00010694-198008000-00014',
        # 'https://doi.org/10.1097/00010694-197704000-00011',
        # 'https://doi.org/10.1097/00010694-196111000-00035',
        # 'https://doi.org/10.1097/00010694-197301000-00016',
        # 'https://doi.org/10.1097/00010694-198904000-00014',
    ]
    for doi in test_dois:
        SciHub(doi, 'paper').download(choose_scihub_url_index=3)
