from getpass import getpass
from pathlib import Path
from uuid import uuid4

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_crawl(
    start_url: str,
    sessionid: str | None,
    course_dir: str | None,
) -> None:
    settings = get_project_settings()
    course_dir = course_dir or "course"
    feed_dir = Path(settings.get("FILES_STORE", "downloads")) / course_dir
    feed_dir.mkdir(parents=True, exist_ok=True)
    settings.set("FEEDS", {str(feed_dir / "output.json"): {"format": "json"}})
    process = CrawlerProcess(settings=settings)
    process.crawl(
        "maktabkhooneh",
        start_url=start_url,
        sessionid=sessionid,
        course_dir=course_dir,
    )
    process.start()


def main():
    start_url = input("Start URL: ").strip()
    if not start_url:
        raise SystemExit("Start URL is required.")

    random_id = uuid4().hex[:8]
    course_dir = (
        input("Course folder name(optional): ").strip() or f"course_{random_id}"
    )

    sessionid = getpass("sessionid (hidden): ").strip() or None
    run_crawl(start_url=start_url, sessionid=sessionid, course_dir=course_dir)


if __name__ == "__main__":
    main()
