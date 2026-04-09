from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

from mk_crawler.items import MaktabkhoonehUnitItem


def _strip_or_none(v):
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return v


class MaktabkhoonehUnitLoader(ItemLoader):
    default_item_class = MaktabkhoonehUnitItem
    default_input_processor = MapCompose(_strip_or_none)
    default_output_processor = TakeFirst()

    file_urls_in = Identity()
    file_urls_out = Identity()

    course_dir_in = Identity()
    course_dir_out = Identity()
