#!/usr/bin/env python3

import argparse
import ssl
import sys
import urllib.request
#
from bs4 import BeautifulSoup
import requests


DOMAIN_URL = "https://www.top40.nl"
BASE_URL = "https://www.top40.nl/top40/{year}/week-{week}"
YOUTUBE_DL_URL = "ydl '{url}'"  # replace with your own
PDF_DEFAULT_DIR = "pdf-{year}"
VIDEO_DEFAULT_DIR = "videos-{year}"


class Top40Crawler:
    
    def __init__(self, year, week=None):
        self.year = year
        self.week = week

        # work around hairy SSL certificate issue
        # see: https://stackoverflow.com/a/39779918/27426
        if sys.platform == 'darwin':
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                # Legacy Python that doesn't verify HTTPS certificates by default
                pass
            else:
                # Handle target environment that doesn't support HTTPS verification
                ssl._create_default_https_context = _create_unverified_https_context

    def download_pdfs(self):
        if self.week is not None:
            weekrange = range(self.week, self.week+1)
        else:
            weekrange = range(1, 54)

        # try weeks 1-52 and 53 just in case it exists in some years
        for week in weekrange:
            url = BASE_URL.format(year=self.year, week=week)
            print(url)
            try:
                self.download_pdf_from(url, self.year)
            except: # FIXME: be more specific
                import traceback; traceback.print_exc()
                print("Could not download PDF")

    def download_pdf_from(self, url, year):
        # slurp HTML
        with urllib.request.urlopen(url, timeout=30) as u:
            data = u.read()

        # parse HTML
        soup = BeautifulSoup(data, 'html.parser')

        a_tags = soup.find_all('a')
        stuff = [a for a in a_tags 
                if a.get('href') and a.get('href').lower().endswith('.pdf')]
        if stuff:
            href = stuff[0].get('href')
            url = DOMAIN_URL + href
            dir = PDF_DEFAULT_DIR.format(year=year)
            self.download_to(url, dir)
        else:
            print("No PDF link was found for:", url)

    def download_to(self, url, dir):
        print("Downloading", url, "to", dir)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("grabtop40.py", 
             description="Download PDFs and/or videos from top40.nl")

    parser.add_argument('year', metavar='year', type=int, 
                        help="The year to be downloaded")
    parser.add_argument('--week', metavar='week', type=int,
                        help="Only download the given week")

    args = parser.parse_args()
    print(args)

    crawler = Top40Crawler(year=args.year, week=args.week)
    crawler.download_pdfs()

