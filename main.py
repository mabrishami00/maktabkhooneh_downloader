from getpass import getpass

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_crawl(*, start_url: str, sessionid: str | None) -> None:
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    process.crawl("maktabkhooneh", start_url=start_url, sessionid=sessionid)
    process.start()


def main():
    start_url = input("Start URL: ").strip()
    if not start_url:
        raise SystemExit("Start URL is required.")

    sessionid = getpass("sessionid (hidden): ").strip() or None
    run_crawl(start_url=start_url, sessionid=sessionid)


if __name__ == "__main__":
    main()
