import os
from getpass import getpass
from pathlib import Path
from urllib.parse import unquote, urlsplit
from uuid import uuid4

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

VALID_QUALITIES = ["1080", "720", "480", "360", "240"]


def main():
    load_dotenv(Path(__file__).resolve().parent / ".env")

    start_url = input("Start URL: ").strip()
    if not start_url:
        raise SystemExit("Start URL is required.")
    start_url = normalize_course_url(start_url)

    random_id = uuid4().hex[:8]
    course_dir = (
        input("Course folder name (optional): ").strip() or f"course_{random_id}"
    )

    sessionid = prompt_sessionid()

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


def normalize_course_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    if parts.scheme not in {"http", "https"} or host != "maktabkhooneh.org":
        raise SystemExit("Start URL must be a maktabkhooneh.org course link.")

    segments = [unquote(segment) for segment in parts.path.split("/") if segment]
    slug = None
    if len(segments) >= 2 and segments[0] == "course":
        slug = segments[1]
    elif len(segments) >= 3 and segments[0] == "lms" and segments[1] == "course":
        slug = segments[2]

    if not slug:
        raise SystemExit(
            "Could not find a course in that URL. Use a course link like "
            "https://maktabkhooneh.org/course/<slug>/, or a unit link like "
            "https://maktabkhooneh.org/lms/course/<slug>/unit/<id>/."
        )

    course_url = f"https://maktabkhooneh.org/course/{slug}/"
    given_path = "/" + "/".join(segments) + "/"
    if given_path != f"/course/{slug}/":
        print(f"Using course URL: {course_url}")
    return course_url


def prompt_sessionid() -> str | None:
    saved = os.environ.get("SESSIONID", "").strip()
    if saved:
        entered = getpass("sessionid (hidden, Enter keeps the .env value): ").strip()
        return entered or saved
    return getpass("sessionid (hidden): ").strip() or None


if __name__ == "__main__":
    main()
