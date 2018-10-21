### What is this?

A simple script to download PDFs from the Dutch Top 40 site, one year at a time, or for a special year/week. 

(The site also has links to YouTube videos of songs; these are of dubious value, since they often link to videos that are no longer there, or unavailable from a certain location. Even so, the script collects and stores the URLs to these videos in a file. It does **not** download the videos themselves.)

### Requirements

* Python 3.6 (other versions of 3.x might work as well)
* whatever libraries are listed in `requirements.txt`, including [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/) and [requests](https://github.com/requests/requests).

### How to use

To download the PDFs for a single year, use:

```
$ python3 grabtop40.py <year>
```    
e.g.

```
$ python3 grabtop40.py 1988
```

To grab only a single week, use the `--week` option:

```
python3 grabtop40.py --week=2 1988
```

As noted above, YouTube URLs are collected and stored as well. When downloading for a year, these are stored (one URL per line) in a file called `urls-{year}.txt`, e.g. `urls-1988.txt`. When doing a single week, they are stored in e.g. `urls-1988-02.txt`.

### What to do with the video URLs?

Other than visiting them, you could use a tool like `youtube-dl` to download the videos. I of course in no way endorse this. ;-) 

### Disclaimer

As always, I knocked this together in an evening, so don't expect top code quality. Do expect bugs. ;-) Also do expect the script to stop working at some point in time, as sites often change their layout.

It is recommended not to abuse this script, because `top40.nl` might just decide to block your IP address if you hammer their site... I don't know.

### What's the reason for writing the script?

I like to be able to look up old top 40s, mostly for nostalgic reasons... this information wasn't always available online, and might not be in the future, the way things are going. In any case, it's useful to have your own copy.

### Will you do a similar script for the TROS/Mega Top 100?

Nog in geen honderd jaar.
