from getpass import getpass
from pathlib import Path
from uuid import uuid4

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

VALID_QUALITIES = ["1080", "720", "480", "360", "240"]


def main():
    start_url = input("Start URL: ").strip()
    if not start_url:
        raise SystemExit("Start URL is required.")

    random_id = uuid4().hex[:8]
    course_dir = (
        input("Course folder name (optional): ").strip() or f"course_{random_id}"
    )

    sessionid = getpass("sessionid (hidden): ").strip() or None

    quality_input = input(
        f"Video quality ({'/'.join(VALID_QUALITIES)}) [default: 720]: "
    ).strip()
    if quality_input and quality_input not in VALID_QUALITIES:
        print(f"Invalid quality '{quality_input}', using 720.")
        quality_input = "720"
    quality = int(quality_input) if quality_input else 720

    run_crawl(
        start_url=start_url,
        sessionid=sessionid,
        course_dir=course_dir,
        quality=quality,
    )


def run_crawl(
    start_url: str,
    sessionid: str | None,
    course_dir: str | None,
    quality: int = 720,
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
        quality=quality,
    )
    process.start()


if __name__ == "__main__":
    main()
