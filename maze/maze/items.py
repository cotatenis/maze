# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags, replace_escape_chars, strip_html5_whitespace
from scrapy.item import Item
from dataclasses import dataclass
from price_parser import parse_price

def get_price(text):
    return float(parse_price(text).amount)

def get_currency(text):
    return parse_price(text).currency

def does_have_products_in_stock(payload):
    stock_info = [v['Sku']['Stock'] for v in payload['Variations']]
    check_for_stock = [v for v in stock_info if v>0]
    if not check_for_stock:
        return False
    return True

def cleaning_html_text(text):
    raw = text.split(" ")
    text = [d for d in raw if d!=""]
    return text


def cleaning_description(text):
    return text.replace("\u00ae", " ").replace("\xa0", " ")

def parse_adidas_sku(sku):
    sku = sku.split(":")[-1].strip()
    return sku
    
class MazeItem(Item):
    brand = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, replace_escape_chars, strip_html5_whitespace
        ),
        output_processor=TakeFirst(),
    )
    product = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, replace_escape_chars, strip_html5_whitespace
        ),
        output_processor=TakeFirst(),
    )
    full_price = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, strip_html5_whitespace, get_price
        ),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, strip_html5_whitespace, get_price
        ),
        output_processor=TakeFirst(),
    )
    currency = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, strip_html5_whitespace, get_currency
        ),
        output_processor=TakeFirst(),
    )
    url = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace), output_processor=TakeFirst()
    )
    store_sku = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, replace_escape_chars, strip_html5_whitespace
        ),
        output_processor=TakeFirst(),
    )
    sku = scrapy.Field(
        input_processor=MapCompose(
            replace_escape_chars, strip_html5_whitespace, parse_adidas_sku
        ),
        output_processor=TakeFirst(),
    )
    stock_info = scrapy.Field()
    has_stock = scrapy.Field(input_processor=MapCompose(does_have_products_in_stock), output_processor=TakeFirst())
    description = scrapy.Field(
        input_processor=MapCompose(
            remove_tags, replace_escape_chars, strip_html5_whitespace
        ),
        output_processor=TakeFirst(),
    )
    timestamp = scrapy.Field()
    spider = scrapy.Field(output_processor=TakeFirst())
    spider_version = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    image_uris = scrapy.Field()