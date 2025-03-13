import scrapy
import re
import redis
from database.mongodb_handler import MongoDBHandler


class BatdongsanSpider(scrapy.Spider):
    name = "batdongsan"
    allowed_domains = ["homedy.com"]
    start_urls = ["https://homedy.com/du-an-can-ho"]

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_failed = False
        self.mongodb_handler = MongoDBHandler(
            uri="mongodb://hieutrungmc:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@cluster0-shard-00-00.0bbrp.mongodb.net:27017,cluster0-shard-00-01.0bbrp.mongodb.net:27017,cluster0-shard-00-02.0bbrp.mongodb.net:27017/?ssl=true&replicaSet=atlas-4lkfbx-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0",
            db_name="batdongsan",
            collection_name="thongtin",
        )
        try:
            self.redis_client = redis.StrictRedis(
                host="redis", port=6379, password="password", decode_responses=True
            )
    # Test connection
            self.redis_client.ping()
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
    # Log the Redis connection error and set the failure flag
            self.logger.warning(
                f"Redis connection failed: {str(e)}. Redis operations will be skipped."
            )
            self.redis_failed = True

    def parse(self, response):
        for item in response.css("div.tab-content div.item"):

            data = self.extract_item_data(item)
            if not self.redis_failed:
                if self.redis_client.sismember("crawled_urls", data["title"]):
                    self.logger.info(f"Nhà {data['title']} đã được crawl. Bỏ qua.")
                    continue
                self.redis_client.sadd("crawled_urls", data["title"])
            self.mongodb_handler.save_data(data)

    def extract_item_data(self, item):
        item_data = {}

        title_element = item.css("h2.name::text").get()
        item_data["title"] = (
            re.sub(r"\s+", " ", title_element).strip() if title_element else "N/A"
        )

        price_element = item.css("span.price::text").get()
        item_data["price"] = price_element if price_element else "N/A"

        address_element = item.css("div.address::text").get()
        item_data["address"] = address_element.strip() if address_element else "N/A"

        area_element = item.css("span.name-item::text").get()
        item_data["area"] = area_element.strip() if area_element else "N/A"

        image_element = item.css("div.thumb-image img.lazy::attr(data-src)").get()
        item_data["image_url"] = image_element if image_element else "N/A"

        print(item_data)
        return item_data
