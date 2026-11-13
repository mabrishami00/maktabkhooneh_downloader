import json
import re
from urllib.parse import unquote

import scrapy

from mk_crawler.items import MaktabkhoonehUnitItem

AVAILABLE_QUALITIES = [1080, 720, 480, 360, 240]


class MaktabkhoonehSpider(scrapy.Spider):
    name = "maktabkhooneh"
    allowed_domains = ["maktabkhooneh.org"]

    async def start(self):
        slug = self._course_slug()
        api_url = f"https://maktabkhooneh.org/api/v1/courses/{slug}/chapters/"
        yield scrapy.Request(
            api_url, callback=self.parse_chapters, cookies=self._cookies()
        )

    def parse_chapters(self, response):
        data = json.loads(response.text)
        chapters = data.get("chapters", [])
        course_dir = getattr(self, "course_dir", "course")
        quality = int(getattr(self, "quality", 720))

        for ch_idx, chapter in enumerate(chapters, start=1):
            ch_title = self._sanitize_filename(
                chapter.get("title", f"chapter_{ch_idx}")
            )
            chapter_dir = f"{ch_idx:02d}-{ch_title}"

            unit_counter = 0
            for unit in chapter.get("units", []):
                if unit.get("type") != "lecture":
                    continue
                unit_counter += 1
                unit_id = unit["id"]
                unit_title = unit.get("title", f"unit_{unit_id}")
                video_api = (
                    f"https://maktabkhooneh.org/api/v1/lms/units/{unit_id}/video_url/"
                )
                yield scrapy.Request(
                    video_api,
                    callback=self.parse_video_url,
                    cookies=self._cookies(),
                    meta={
                        "course_dir": course_dir,
                        "chapter_dir": chapter_dir,
                        "unit_index": unit_counter,
                        "unit_title": unit_title,
                        "quality": quality,
                    },
                    dont_filter=True,
                )

    def parse_video_url(self, response):
        meta = response.meta
        data = json.loads(response.text)

        qualities = data.get("qualities", [])
        chosen = self._pick_quality(qualities, meta["quality"])

        if not chosen:
            self.logger.warning(
                "No video qualities for unit '%s', skipping", meta["unit_title"]
            )
            return

        download_url = chosen["download_url"]
        unit_title = self._sanitize_filename(meta["unit_title"])
        filename = f"{meta['unit_index']}-{unit_title}.mp4"

        yield MaktabkhoonehUnitItem(
            index=meta["unit_index"],
            title=meta["unit_title"],
            mp4_url=download_url,
            filename=filename,
            course_dir=meta["course_dir"],
            chapter_dir=meta["chapter_dir"],
            file_urls=[download_url],
        )

    def _cookies(self):
        sid = getattr(self, "sessionid", None)
        return {"sessionid": sid} if sid else None

    def _course_slug(self):
        url = unquote(getattr(self, "start_url", ""))
        match = re.search(r"/(?:lms/)?course/([^/?#]+)", url)
        if match:
            return match.group(1)
        return url.split("?", 1)[0].split("#", 1)[0].rstrip("/").split("/")[-1]

    def _sanitize_filename(self, name: str) -> str:
        return re.sub(r'[<>:"/\\|?*]', "_", name).strip().rstrip(".")

    def _pick_quality(self, qualities: list[dict], target: int) -> dict | None:
        if not qualities:
            return None
        by_res = {q["resolution"]: q for q in qualities}
        if target in by_res:
            return by_res[target]
        below = sorted([r for r in by_res if r < target], reverse=True)
        if below:
            return by_res[below[0]]
        above = sorted(r for r in by_res if r > target)
        if above:
            return by_res[above[0]]
        return qualities[0]
