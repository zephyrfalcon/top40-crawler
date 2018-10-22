#!/usr/bin/env python3

import argparse
import io
import os
import ssl
import sys
import urllib.request, urllib.parse
#
from bs4 import BeautifulSoup
import requests
#
from OrderedSet import OrderedSet


DOMAIN_URL = "https://www.top40.nl"
BASE_URL = "https://www.top40.nl/top40/{year}/week-{week}"
YOUTUBE_DL_URL = "ydl '{url}'"  # replace with your own
PDF_DEFAULT_DIR = "pdf-{year}"
VIDEO_DEFAULT_DIR = "videos-{year}"

DEBUG = False

class Top40Crawler:
    
    def __init__(self, year, week=None):
        self.year = year
        self.week = week

        self.youtube_urls = OrderedSet()  # YouTube URLs collected

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

    def ensure_dir_exists(self, dir):
        try:
            os.makedirs(dir)
        except OSError:
            # TODO: distinguish between "directory already exists" and other
            # exceptions
            pass

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
            except Exception as e: 
                sio = io.StringIO()
                import traceback; traceback.print_exc(file=sio)
                last_line = sio.getvalue().split('\n')[-2].strip()
                print("!", last_line)
                print("Could not download PDF")

        # write YouTube URLs we found
        if self.week:
            url_filename = 'urls-%04d-%02d.txt' % (self.year, self.week)
        else:
            url_filename = 'urls-{year}.txt'.format(year=self.year)
        with open(url_filename, 'w') as f:
            for url in self.youtube_urls:
                print(url, file=f)
        print(len(self.youtube_urls), "YouTube URLs collected in", url_filename)

    def download_pdf_from(self, url, year):
        # slurp HTML
        with urllib.request.urlopen(url, timeout=30) as u:
            data = u.read()

        # parse HTML
        soup = BeautifulSoup(data, 'html.parser')

        if DEBUG:
            with open('blah.html', 'w') as f:
                f.write(soup.prettify())

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

        youtube_urls = [a.get('href') for a in a_tags
                        if a.get('href') and 'youtube' in a.get('href')
                        and not '/channel/' in a.get('href')]
        if youtube_urls:
            for url in youtube_urls:
                self.youtube_urls.add(url)

    def download_to(self, url, dir):
        self.ensure_dir_exists(dir)
        print("Downloading", url, "to", dir)
        with urllib.request.urlopen(url) as u:
            data = u.read()

        result = urllib.parse.urlparse(url)
        url_path = result.path
        parts = os.path.split(url_path)
        filename = parts[-1]
        target_path = os.path.join(dir, filename)
        with open(target_path, 'wb') as f:
            f.write(data)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("grabtop40.py", 
             description="Download PDFs and/or videos from top40.nl")

    parser.add_argument('year', metavar='year', type=int, 
                        help="The year to be downloaded")
    parser.add_argument('--week', metavar='week', type=int,
                        help="Only download the given week")

    args = parser.parse_args()

    crawler = Top40Crawler(year=args.year, week=args.week)
    crawler.download_pdfs()

