import os

from scrapy.pipelines.files import FilesPipeline


class NamedFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, item=None):
        name = None
        if item:
            name = item.get("filename")
        if name:
            return str(os.path.basename(name))
        return super().file_path(request, response=response, info=info, item=item)
