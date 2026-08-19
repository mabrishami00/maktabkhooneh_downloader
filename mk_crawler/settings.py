BOT_NAME = "mk_crawler"

SPIDER_MODULES = ["mk_crawler.spiders"]
NEWSPIDER_MODULE = "mk_crawler.spiders"

ADDONS = {}


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
)


ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 3

ITEM_PIPELINES = {
    "mk_crawler.pipelines.NamedFilesPipeline": 300,
}

FILES_STORE = "downloads"

FILES_EXPIRES = 365000

FEED_EXPORT_ENCODING = "utf-8"
