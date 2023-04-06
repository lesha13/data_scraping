from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lab2.items import News
from bs4 import BeautifulSoup


class UzhnuSpider(CrawlSpider):
    name = "uzhnu_xpath"
    allowed_domains = ["www.uzhnu.edu.ua"]
    start_urls = ["https://www.uzhnu.edu.ua/uk/cat/faculty"]
    rules = [Rule(LinkExtractor(allow='^.*(faculty-)([a-z])*$'), callback='parse', follow=True)]

    def parse(self, response):
        items = response.xpath('//*[@id="yw2"]/div[2]/div').getall()
        for _ in items:
            _ = BeautifulSoup(_)

            day = _.find(class_="day").text
            month = _.find(class_="month").text
            a = _.a.text.strip()
            href = _.a["href"]

            item = News()
            item['date'] = f"{day} {month}"
            item['title'] = a
            item['url'] = href

            yield item
