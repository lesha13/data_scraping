# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector
from lab2.items import *


class Lab2Pipeline:
    def process_item(self, item, spider):
        if isinstance(item, News):
            item["title"] = item.get("title") + "."
            item["url"] = "www.uzhnu.edu.ua" + item.get("url")
        return item


class SQLPipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="scrapy"
        )
        self.cursor = self.connection.cursor()
        spider.logger.info("Connected to MySQL ")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS 
        items (
            id INT AUTO_INCREMENT,
            PRIMARY KEY (id),
            date VARCHAR(64),
            title VARCHAR(1024),
            url VARCHAR(1024)
        );
        """)
        spider.logger.info("DB is ready ")

    def close_spider(self, spider):
        self.connection.close()
        spider.logger.info("Disconnected from MySQL ")

    def process_item(self, item, spider):
        if isinstance(item, News):
            self.cursor.execute(
                "INSERT INTO items (date, title, url) VALUES (%s, %s, %s);",
                [item.get("date"), item.get("title"), item.get("url")]
            )
            self.connection.commit()
        return item
