# -*- coding: utf-8 -*-
import argparse, os

from .scihub import *
from .update_link import *


def main():
    """Command line tool to download pdfs via DOI from Scihub.
    """
    parser = argparse.ArgumentParser("Command line tool to download pdf via DOI from Scihub.")
    # parser.add_argument('DOI', help="the DOI number of the paper")
    parser.add_argument('-c', '--choose', help="choose scihub url by index")
    parser.add_argument('-D', '--DOI', help="the DOI number of the paper")
    parser.add_argument('-o', '--output', help="directory to download the pdf")
    parser.add_argument('-u', '--update', action='store_true', help="update available Scihub links")
    parser.add_argument('-l', '--list', action='store_true', help="list current saved sichub urls")
    args = parser.parse_args()

    if args.DOI:
        SCIHUB_URL_INDEX = int(open(get_resource_path('cur_scihub_index.txt'), 'r').read())
        if not args.output:
            sci = SciHub(args.DOI)
        else:
            sci = SciHub(args.DOI, args.output)
        sci.download(choose_scihub_url_index=SCIHUB_URL_INDEX)
    elif args.update:
        update_link()
    elif args.list:
        link_file_path = get_resource_path('link.txt')
        cur_scihub_index = int(open(get_resource_path('cur_scihub_index.txt'), 'r').read())
        if not os.path.isfile(link_file_path):
            open(link_file_path, 'w')
        with open(link_file_path, 'r') as link_file:
            for i, link in enumerate(link_file.readlines()):
                if i == cur_scihub_index:
                    print('* [{0}] {1}'.format(i, link[:-1]))
                else:
                    print('  [{0}] {1}'.format(i, link[:-1]))
    elif args.choose:
        open(get_resource_path('cur_scihub_index.txt'), 'w').write(args.choose)
        cur_scihub_url = open(get_resource_path('link.txt'), 'r').readlines()[int(args.choose)].replace('\n', '')
        print("Current scihub url: %s" %(cur_scihub_url))
    else:
        print("Command line tool to download pdfs via DOI from Scihub.")

if __name__=="__main__":
    main()
