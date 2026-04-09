from getpass import getpass
from uuid import uuid4

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_crawl(
    start_url: str,
    sessionid: str | None,
    course_name: str | None,
) -> None:
    settings = get_project_settings()
    settings.set("FEEDS", {"output.json": {"format": "json"}})
    process = CrawlerProcess(settings=settings)
    process.crawl(
        "maktabkhooneh",
        start_url=start_url,
        sessionid=sessionid,
        course_name=course_name,
    )
    process.start()


def main():
    start_url = input("Start URL: ").strip()
    if not start_url:
        raise SystemExit("Start URL is required.")

    random_id = uuid4().hex[:8]
    course_name = (
        input("Course folder name(optional): ").strip() or f"course_{random_id}"
    )

    sessionid = getpass("sessionid (hidden): ").strip() or None
    run_crawl(start_url=start_url, sessionid=sessionid, course_name=course_name)


if __name__ == "__main__":
    main()
