#!/usr/bin/env python3

import argparse
import sys
import urllib.request
#
from bs4 import BeautifulSoup as BS

__usage__ = """\
Usage: grabtop40.py [options] year
"""

BASE_URL = "https://www.top40.nl/top40/{year}/week-{week}"
YOUTUBE_DL_URL = "ydl '{url}'"  # replace with your own
PDF_DEFAULT_DIR = "pdf-{year}"
VIDEO_DEFAULT_DIR = "videos-{year}"


class Top40Crawler:
    
    def __init__(self, year):
        self.year = year

    def download_pdfs(self):
        # try weeks 1-52 and 53 just in case it exists in some years
        for week in range(1, 54):
            url = BASE_URL.format(year=self.year, week=week)
            print(url)
            try:
                self.download_pdf_from(url)
            except: # FIXME: be more specific
                import traceback; traceback.print_exc()
                print("Could not download PDF")

    def download_pdf_from(self, url):
        return
        # slurp HTML
        with urllib.request.urlopen(url, timeout=30):
            data = urllib.read()
        # parse HTML
        soup = BeautifulSoup(data, 'html.parser')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("grabtop40.py", 
             description="Download PDFs and/or videos from top40.nl")

    parser.add_argument('year', metavar='year', type=int, 
                        help="The year to be downloaded")
    parser.add_argument('--week', metavar='week', type=int,
                        help="Only download the given week")

    args = parser.parse_args()
    print(args)

    crawler = Top40Crawler(year=args.year)
    crawler.download_pdfs()

