import os
import posixpath

from scrapy.pipelines.files import FilesPipeline


class NamedFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        name = None
        course_dir = None
        if item:
            name = item.get("filename")
            course_dir = item.get("course_dir")
            base = os.path.basename(name) if name else None
            if base:
                return posixpath.join(course_dir, base)
        return super().file_path(request, response=response, info=info, item=item)
