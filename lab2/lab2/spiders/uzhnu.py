from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lab2.items import *
from bs4 import BeautifulSoup


class UzhnuSpider(CrawlSpider):
    name = "uzhnu"
    allowed_domains = ["www.uzhnu.edu.ua"]
    start_urls = ["https://www.uzhnu.edu.ua/uk/cat/faculty"]
    rules = [Rule(LinkExtractor(allow='^.*(faculty-)([a-z])*$'), callback='parse', follow=True)]

    def parse(self, response):
        page = BeautifulSoup(response.body, "html.parser")

        img = "https://www.uzhnu.edu.ua/" + page.find(id="flexslide-block-slide1").img["src"]

        yield {
            'image_urls': [img]
        }

        for news in page.select("#yw2 > div.items > div.anounce.compact"):
            item = News()

            day = news.find(class_="day").text
            month = news.find(class_="month").text
            a = news.a.text.strip()
            href = news.a["href"]

            item["date"] = f"{day} {month}"
            item["title"] = a
            item["url"] = href

            yield item
