# -*- coding: utf-8 -*-
import argparse, os

from .scihub import *
from .update_link import *

def main():
    """Command line tool to download pdfs via DOI from Scihub.
    """
    parser = argparse.ArgumentParser("Command line tool to download pdf via DOI from Scihub.")
    # parser.add_argument('DOI', help="the DOI number of the paper")
    parser.add_argument('-D', '--DOI', help="the DOI number of the paper")
    parser.add_argument('-o', '--output', help="directory to download the pdf")
    parser.add_argument('-u', '--update', action='store_true', help="update available Scihub links")
    parser.add_argument('-l', '--list', action='store_true', help="list current saved sichub urls.")
    args = parser.parse_args()

    if args.DOI:
        if not args.output:
            sci = SciHub(args.DOI)
        else:
            sci = SciHub(args.DOI, args.output)
        sci.download()
    elif args.update:
        update_link()
    elif args.list:
        link_file_path = get_resource_path('link.txt')
        if not os.path.isfile(link_file_path):
            open(link_file_path, 'w')
        with open(link_file_path, 'r') as link_file:
            for i, link in enumerate(link_file.readlines()):
                print('[{0}] {1}'.format(i, link[:-1]))
    else:
        print("Command line tool to download pdfs via DOI from Scihub.")

if __name__=="__main__":
    main()
