import posixpath

from scrapy.pipelines.files import FilesPipeline


class NamedFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        if item:
            course_dir = item.get("course_dir", "")
            chapter_dir = item.get("chapter_dir", "")
            filename = item.get("filename", "")
            if filename:
                return posixpath.join(course_dir, chapter_dir, filename)
        return super().file_path(request, response=response, info=info, item=item)
