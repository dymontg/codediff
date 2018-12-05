"""
This file serves as a downloader for snap files from html links
are easily downloadable from Canvas.
"""
# TODO Automate this process as a part of running codediff on a folder of these html files.
import argparse
import logging
from src.scraper import scraperInstance
from src import logger
from src.utils import FileError, FileIOError, sdv

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('input_files', nargs='+',
                            help='input files for the file getter. Can be files and/or directories.')
    argparser.add_argument('-d', '--debug', help='Print debug statements for developers.',
                        action='store_const', dest='log_level', const=logging.DEBUG)
    args = argparser.parse_args()

    _logger = logger.init_logger(args.log_level or logging.INFO)

    # running the program
    try:
        _logger.debug('Creating HtmlParser instance.')
        scraper = scraperInstance(args.input_files)
        _logger.debug('Scraping files.')



    except (FileError, FileIOError) as e:
        argparser.error(str(e))
    except Exception as e:
        _logger.exception('Oh noes! :( An exception has occurred.')
