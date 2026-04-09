import os

from scrapy.pipelines.files import FilesPipeline


class NamedFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        name = None
        course_dir = None
        if item:
            name = item.get("filename")
            course_dir = item.get("course_dir")
            return f"{course_dir}/{os.path.basename(name)}"
        return super().file_path(request, response=response, info=info, item=item)
