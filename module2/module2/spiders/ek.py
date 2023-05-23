import scrapy
from module2.items import Module2Item
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class EkSpider(scrapy.Spider):
    name = "ek"
    allowed_domains = ["ek.ua"]
    start_urls = ["https://ek.ua/ua/list/298/"]

    def __init__(self):
        self.driver = webdriver.Chrome('/path/to/chromedriver')

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     ".model-shop-name .sn-div")
                ),
            )

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()

        soup = BeautifulSoup(response.text, 'html.parser')

        laptops = soup.find(id="list_form1").find_all(class_="model-short-div list-item--goods-group ms-grp")

        for laptop in laptops:
            model = laptop.find(class_="u").getText()
            img_url = laptop.find("img")["src"]

            price = laptop.find(class_="model-conf-title").findAll("span")
            price_low, price_high = price[-2::]
            price_low = int(price_low.getText().replace("\xa0", ""))
            price_high = int(price_high.getText().replace("\xa0", ""))

            configs = laptop.find(class_="conf-div-short").findAll("u")

            i = 1
            for config in configs:
                config = config.getText()
                yield Module2Item(
                    model=model,
                    img_url=img_url,
                    price_low=price_low,
                    price_high=price_high,
                    config=config,
                )

                i += 1
                if i > 7:
                    break

    def close(self, reason):
        self.driver.quit()


class SeleniumRequest(scrapy.Request):
    def __init__(self, wait_time=None, wait_until=None, screenshot=False, script=None, execute=None, *args, **kwargs):

        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script
        self.execute = execute

        super().__init__(*args, **kwargs)
