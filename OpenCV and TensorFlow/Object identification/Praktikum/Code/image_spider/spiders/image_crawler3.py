from Code.image_spider.classes.picture_class import Picture
import scrapy
import scrapy.exceptions

import urllib.request
import urllib.error

from PIL import Image

import os
import json

desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")


class Spider(scrapy.Spider):
    # counter for name
    count = 0
    # name of the spider, for starting it
    name = "speed"
    # how many times the spider jumps to website
    hop_count = 6
    # a list of all visited pages
    list_visted_links = []

    # a number that shows the current page of json file
    next_page = 1
    # a counter which counts which line from file 'base.txt' it has to read
    line_counter = 0
    # a list of current page from all json files
    pages = []
    # number of json files
    max_line = len(open(os.path.abspath(desktop + "/darkflow-master/saved-data/base.txt")).readlines())
    # initialise list of current page from all json files bc every file begins at 1
    for i in range(max_line):
        pages.append(1)

    # to set the hop_count of the spider to specific value even when no Spider Object exists
    @classmethod
    def set_hop_count(cls, hops):
        if isinstance(hops, int):
            if 50 >= hops >= 0:
                cls.hop_count = hops
            else:
                pass
        else:
            pass

    # when following links which domains are allowed
    allowed_domains = ["unsplash.com"]

    # to make sure the spider ends in time you need to limit the number of links the spider follows
    # to not get bombarded with log messages, set the Log_Level to 'Error'
    # only Errors will be displayed
    custom_settings = {'DEPTH_LIMIT': 100,
                       'LOG_LEVEL': 'ERROR'}
    base = "https://unsplash.com/napi/search/photos?query=bicycle&xp=&per_page=20&page=%s"
    # the url the spider start on
    start_urls = [base % 1]  # ""https://unsplash.com/s/photos/bicycle""

    # this function is working with the resposnes
    def parse(self, response):
        try:
            # loads the data of the json file
            data = json.loads(response.body)
            # gets picture in the json file
            for item in data.get("results", []):
                # extracting the images URL!!!
                # Important: now we only have downloaded the url not the image it self!!
                img_url = item.get('urls', {}).get('regular')
                # get the description of said picture
                alt_description = item.get('alt_description')
                # for debugging
                print(img_url)
                print(alt_description)
                # calls function which downloads the picture
                self.count = downloadimg(alt_description=alt_description, img_url=img_url, count=self.count)

            # path where every base of the json file is stored
            path = desktop + "/darkflow-master/saved-data/base.txt"
            path = os.path.abspath(path)
            # every json file has got the attribute 'total_pages'
            # this attribute signals when we reached the end of the files
            # most of the time we set a limit, so we don't download all the pictures for debugging purposes
            if self.next_page < 2:# < data['total_pages']:
                # for debugging
                # Rohan time
                print(self.next_page)
                # increase the page counter to scrape the next json file next
                self.next_page += 1
                # for debugging
                print("increase: " + self.base)
                print(self.next_page)
                yield response.follow(self.base % self.next_page)

                # opens the file with every base for the json file
                # has been scraped by the other spider
                with open(path, 'r') as f:
                    lines = f.readlines()
                    # to ensure that the file is not empty
                    if len(lines) > 0:
                        # get next json-base
                        current_base = lines[self.line_counter]
                        # get next page of said json file
                        current_page = self.pages[self.line_counter]
                        self.base = current_base
                        self.next_page = current_page
                        # increase the page counter
                        self.pages[self.line_counter] += 1
                        # increase the line counter to read the next line the next time
                        # to not be stuck on the same base for ever
                        self.line_counter += 1
                        # max_line -> amount of lines in the file
                        # the line counter cannot be larger than the amount of lines
                        # other wise a exception will be thrown
                        if self.line_counter == self.max_line:
                            self.line_counter = 0
                        yield response.follow(self.base % self.next_page)
            else:
                # if we reached the last page of said json files
                # the base needs to be removed from the file
                with open(path, 'r') as f:
                    lines = f.readlines()
                # removes the file to ensure that the base will be removed
                if self.line_counter <= len(lines) - 1:
                    os.remove(path)
                    with open(path, 'w') as f:
                        for line in lines:
                            # only write the base of json files that haven't
                            # ended yet
                            if line != lines[self.line_counter]:
                                f.write(line)
                    # after removing one line, we have to make sure that the amount of lines has to decrease too
                    self.max_line -= 1
                    self.pages.pop(self.line_counter)

        except scrapy.exceptions.NotSupported:
            reason = "Response content isn't text"
            print(reason + " - spider is getting closed")
            raise scrapy.exceptions.CloseSpider(reason=reason)

        except scrapy.exceptions:
            reason = "Sorry Something went wrong"
            print("Sorry Something went wrong")
            raise scrapy.exceptions.CloseSpider(reason=reason)


def downloadimg(alt_description, img_url, count):
    try:
        # right now the object/photo is still stored locally on a later point they might be saved in a cloud
        # define where the object gets stored
        path = desktop + "/darkflow-master/saved-data/images-original/"
        path = os.path.abspath(path)
        name = path + "/photo" + str(count) + ".png"

        # here we downland the actual picture with the url we have figured out earlier
        urllib.request.urlretrieve(img_url, name)
        try:
            # open the image using Image from PIL
            img = Image.open(name)
            # find out the original height and width
            org_width, org_height = img.size
            # create an entry in the file info.txt about the original image
            # create a a Object of the class Picture
            pic = Picture(path=name, source=str(img_url), height=org_height, width=org_width, desc=alt_description)
            pic.save_info()
        except OSError:
            pass
        # make sure to add 1 to the counter so the name changes for the next picture
        count = count + 1

    # the object doesn't have the format jpg or png
    except ValueError:
        print("Picture not downloaded:" + str(img_url))

    # the Website doesn't allow downloading with a spider
    except urllib.error.HTTPError:
        print("HTTP error occurred with " + str(img_url))

    return count
