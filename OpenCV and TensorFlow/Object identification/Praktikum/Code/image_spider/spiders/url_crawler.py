import scrapy
import scrapy.exceptions
import os
desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")


class UrlSpider(scrapy.Spider):
    # name of the spider, for starting it
    name = "base"
    # how many times the spider jumps to website
    hop_count = 6
    # a list of all visited pages
    list_visited_links = []
    # a list of all json bases
    base_links = []

    # when following links which domains are allowed
    allowed_domains = ["unsplash.com"]
    base = "https://unsplash.com/napi/search/photos?query=bicycle&xp=&per_page=20&page=%s"
    # to make sure the spider ends in time you need to limit the number of links the spider follows
    # to not get bombarded with log messages, set the Log_Level to 'Error'
    # only Errors will be displayed
    custom_settings = {'DEPTH_LIMIT': 100,
                       'LOG_LEVEL': 'ERROR'}
    # words = ["bicycle", "Bicycle", "Bike", "bike", "cycling", "Cycling", "Cycle", "cycle", "Cyclist", "cyclist"]

    # the url the spider start on
    start_urls = ["https://unsplash.com/s/photos/bicycle"]

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

    # this function is working with the responses
    def parse(self, response):
        # list of links where one will get chosen after its URL
        # if certain keywords are contained
        list_of_links = []
        try:
            # get every link from the website
            for href in response.xpath("//a/@href").getall():
                # append each URL
                list_of_links.append(href)
            # check if there are even links on this web page
            max_index = list_of_links.__len__() - 1
            if max_index == 0 or max_index == -1:
                return

            # iterates through the list of links to look for URLs that contain certain keywords
            href = list_of_links[0]
            for i in range(max_index):
                href = list_of_links[i]
                x = str(href)
                if x.__contains__("bi") or x.__contains__("Bi") or x.__contains__("cyc") or x.__contains__("Cyc"):
                    if self.list_visited_links.__contains__(href) or str(href).__contains__("mailto:"):
                        print("Already visited")
                    else:
                        break

            # for debugging
            print("chosen link : " + str(href))
            print("hop count " + str(self.hop_count))

            # save the base of the json file in an external file
            # so, that the other spider can use it
            self.savebase()
            splitted = href.split("/")
            # we use a static approach, we know that this isn't the final solution, but it is better than nothing
            # we tried for a day and a half to get the URL of the json file, but it isn't possible on this website
            self.base = "https://unsplash.com/napi/search/photos?query=" + splitted[len(splitted)-1] + "&xp=&per_page" \
                                                                                                       "=20&page=%s"

            # check and change the hop count
            if self.hop_count > 0:
                self.list_visited_links.append(href)
                self.hop_count = self.hop_count - 1
                yield response.follow(href, callback=self.parse)

        except scrapy.exceptions.NotSupported:
            reason = "Response content isn't text"
            print(reason + " - spider is getting closed")
            raise scrapy.exceptions.CloseSpider(reason=reason)

        except scrapy.exceptions:
            reason = "Sorry Something went wrong"
            print("Sorry Something went wrong")
            raise scrapy.exceptions.CloseSpider(reason=reason)

    def savebase(self):
        path = desktop + "/darkflow-master/saved-data/base.txt"
        path = os.path.abspath(path)

        # removes the file, where the base to json files will be stored
        # to ensure that no other links will be scraped
        if len(self.base_links) == 0 and os.path.exists(path):
            os.remove(path)

        print("Contained: " + str(self.base_links.__contains__(self.base)))
        # if we already have this base, we do not need to write it in the file
        if self.base_links.__contains__(self.base):
            print("Base has already been written!")
        else:
            with open(path, 'a') as f:
                f.write(self.base + "\n")
                # to ensure that no base will be twice or more
                self.base_links.append(self.base)
                print(self.base + " appended")
