# run this spider with the command scrapy crawl speed or run the run_spider.py file

from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import twisted.internet.error
from Code.image_spider.spiders.image_crawler3 import Spider
from Code.image_spider.spiders.url_crawler import UrlSpider
import os
import shutil

desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")

configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(UrlSpider)
    yield runner.crawl(Spider)
    reactor.stop()


# converts an str to int
def parse(num):
    try:
        return int(num)
    except ValueError:
        return None


# delete Folders and creates new one to delete old pictures
def newdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


# starts the Crawl Process
process = CrawlerProcess()

# no user input needed
"""print("Welcome to your spider: \n 0 for starting the spider \n -1 to quit")
number = input("enter number: ")
number = parse(number)"""
number = 0
# When the user a wrong value:
while number is None or (number != -1 and number != 0):
    print("Sorry wrong input try again \n enter 0 or 1 \n 0 for starting the spider \n 1 to quit")
    number = input("enter number: ")
    number = parse(number)

if number == 0:
    #yolo_path = desktop + "/darkflow-master/saved-data/images-yolo"
    #cropped_path = desktop + "/darkflow-master/saved-data/images-yolo-cropped"
    #resized_path = desktop + "/darkflow-master/saved-data/images-yolo-resized"
    #org_path = desktop + "/darkflow-master/saved-data/images-original"

    # delete every folder
    #newdir(org_path)
    #newdir(yolo_path)
    #newdir(cropped_path)
    #newdir(resized_path)

    # User enters the number of pages the Spider should crawl
    hop_count = 10  # input("Enter the hop count:")
    hop_count = parse(hop_count)

    # When the user a wrong value:
    while hop_count > 50 or hop_count < -1 or hop_count is None:
        hop_count = input("Ups, please enter a valid Hop Count between 0 and 10: \n or enter -1 to quit ")
        hop_count = parse(hop_count)

    if hop_count == -1:
        print("You chose to quit. Have a good day!")
        exit()

    # Set the number of  of pages the Spider should crawl
    UrlSpider.set_hop_count(hop_count)
    # run spider
    try:
        crawl()
        reactor.run()  # the script will block here until the last crawl call is finished
    except twisted.internet.error.ReactorNotRestartable:
        print("You have already started the spider once, sorry a second time isn't allowed")
        exit()

elif number == -1:
    exit()

else:
    print("Sorry, something went wrong - try to restart the program")
    exit()
