from scraper import *
from searcher import *
from converter import *

# TODO: create git repo for project


def main():
    # scrape spotify playlist
    runScraper()

    # download songs from youtube
    runDownloader()

    # convert mp4 videos to mp3
    runConverter()


if __name__ == '__main__':
    main()
