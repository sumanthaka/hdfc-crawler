# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import unidecode


class HdfccrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        fields = adapter.field_names()
        for field in fields:
            if field != 'reward':
                value = adapter.get(field)
                if type(value) == list:
                    adapter[field] = " ".join(value)

        value = adapter.get("reward")
        if value != 'NA':
            if value[1] != 100:
                value[0] = value[0] / value[1]
                value[1] = 100
                value[0] *= 100
            adapter["reward"] = value[0]

        fields = ['lounge', "milestone", "fees"]
        for field in fields:
            value = adapter.get(field)
            adapter[field] = unidecode.unidecode(value).strip()

        return item
