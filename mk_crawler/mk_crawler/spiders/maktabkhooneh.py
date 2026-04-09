import scrapy


class MaktabkhoonehSpider(scrapy.Spider):
    name = "maktabkhooneh"
    allowed_domains = ["maktabkhooneh.org"]
    start_urls = ["https://maktabkhooneh.org"]

    def parse(self, response):
        pass
