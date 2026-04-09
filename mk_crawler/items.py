import scrapy


class MaktabkhoonehUnitItem(scrapy.Item):
    index = scrapy.Field()
    title = scrapy.Field()
    page_url = scrapy.Field()
    mp4_url = scrapy.Field()
    filename = scrapy.Field()
    course_dir = scrapy.Field()
    file_urls = scrapy.Field()
