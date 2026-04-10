from urllib.parse import parse_qs, unquote, urlparse

import scrapy

from mk_crawler.loaders import MaktabkhoonehUnitLoader


class MaktabkhoonehSpider(scrapy.Spider):
    name = "maktabkhooneh"
    allowed_domains = ["maktabkhooneh.org"]


    async def start(self):
        start_url = getattr(self, "start_url", None)
        sessionid = getattr(self, "sessionid", None)
        cookies = {"sessionid": sessionid} if sessionid else None
        yield scrapy.Request(start_url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        sessionid = getattr(self, "sessionid", None)
        course_dir = getattr(self, "course_dir", None)
        cookies = {"sessionid": sessionid} if sessionid else None


        unit_hrefs = response.xpath(
            "//a[contains(concat(' ', normalize-space(@class), ' '), ' desktop-unit-nav__unit ')]/@href"
        ).getall()
        if not unit_hrefs:
            unit_hrefs = response.xpath(
                "//a[contains(@class,'unit-nav__unit')]/@href"
            ).getall()

        unit_urls = []
        seen = set()
        for href in unit_hrefs:
            url = response.urljoin(href)
            if url in seen:
                continue
            seen.add(url)
            unit_urls.append(url)

        if not unit_urls:
            self.logger.warning("No unit links found on %s", response.url)

        for idx, url in enumerate(unit_urls, start=1):
            yield scrapy.Request(
                url,
                callback=self.parse_unit,
                meta={"unit_index": idx, "course_dir": course_dir},
                cookies=cookies,
            )

    def parse_unit(self, response):
        idx = int(response.meta["unit_index"])
        course_dir = response.meta["course_dir"]
        title = response.xpath("normalize-space(//title/text())").get()

        mp4_url = response.xpath(
            "(//source[contains(concat(' ', normalize-space(@class), ' '), ' js-player__source ') "
            "and contains(@src,'.mp4') and contains(@src,'/videos/hq')]/@src)[1]"
        ).get()
        if not mp4_url:
            mp4_url = response.xpath(
                "(//source[contains(concat(' ', normalize-space(@class), ' '), ' js-player__source ') "
                "and contains(@src,'.mp4')]/@src)[1]"
            ).get()
        if not mp4_url:
            mp4_url = response.xpath("(//meta[@property='og:video']/@content)[1]").get()
        if mp4_url:
            mp4_url = response.urljoin(mp4_url)

        filename = None
        if mp4_url:
            parsed = urlparse(mp4_url)
            qs = parse_qs(parsed.query)
            name_from_query = (qs.get("name") or [None])[0]
            if name_from_query:
                base = unquote(name_from_query)
            else:
                base = unquote((parsed.path or "").rstrip("/").split("/")[-1])
            if base:
                filename = f"{idx}-{base}"

        loader = MaktabkhoonehUnitLoader(response=response)
        loader.add_value("index", idx)
        loader.add_value("title", title)
        loader.add_value("page_url", response.url)
        loader.add_value("mp4_url", mp4_url)
        loader.add_value("filename", filename)
        loader.add_value("course_dir", course_dir)
        loader.add_value("file_urls", [mp4_url] if mp4_url else [])
        yield loader.load_item()
