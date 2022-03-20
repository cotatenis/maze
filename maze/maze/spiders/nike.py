from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from maze.items import MazeItem
from scrapy.loader import ItemLoader
import json
from scrapy.utils.project import get_project_settings
from math import ceil
from scrapy import Request
class MazeNikeSpider(Spider):
    settings = get_project_settings()
    name = "maze-nike"
    version = settings.get("VERSION")
    allowed_domains = ["www.maze.com.br"]
    start_urls = ['https://www.maze.com.br/categoria/tenis/nike']
    sku_pattern = r"\s?Ref:\s+[A-Z0-9]+-[A-Z0-9]+|\s+?Refer[ê|e]ncia:\s+?[A-Z0-9]+-[A-Z0-9]+|\s?REFER[Ê|E]NCIA:\s+?[A-Z0-9]+-[A-Z0-9]+"
    brand = 'Nike'
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, method='GET', callback=self.middle)
    
    def middle(self, response):
        total_products = 0
        number_of_products_1 = response.xpath("//input[@name='NIKE NSW']/../label/text()").re(r"\d+")
        if number_of_products_1:
            total_products += int(number_of_products_1[0])
        number_of_products_2 = response.xpath("//input[@name='JORDAN']/../label/text()").re(r"\d+")
        if number_of_products_2:
            total_products += int(number_of_products_2[0])
        number_of_products_3 = response.xpath("//input[@name='NIKE SB']/../label/text()").re(r"\d+")
        if number_of_products_3:
            total_products += int(number_of_products_3[0])
        if total_products:
            #number_of_products = int(number_of_products[0])
            number_of_pages = ceil(total_products/48)
            url = "https://www.maze.com.br/product/getproductscategory/?path=%2Fcategoria%2Ftenis%2Fnike&viewList=&pageNumber=1&pageSize=48&order=&brand=30385&category=124682&group=&keyWord=&initialPrice=&finalPrice=&variations=&idAttribute=&idEventList=&idCategories=&idGroupingType=&priceFilter="
            yield Request(url=url, cb_kwargs={"number_of_pages" : number_of_pages, "first_landing" : True}, callback=self.pagination)
    
    def pagination(self, response, number_of_pages, first_landing):
        product_details = LinkExtractor(restrict_xpaths="//a[@class='ui image fluid attached']")
        for link in product_details.extract_links(response):
            yield Request(url=link.url, callback=self.parse)
        if first_landing:
            for page in range(2, number_of_pages+1):
                url = f"https://www.maze.com.br/product/getproductscategory/?path=%2Fcategoria%2Ftenis%2Fnike&viewList=&pageNumber={page}&pageSize=48&order=&brand=30385&category=124682&group=&keyWord=&initialPrice=&finalPrice=&variations=&idAttribute=&idEventList=&idCategories=&idGroupingType=&priceFilter="
                yield Request(url=url, method='GET', callback=self.pagination, cb_kwargs={"number_of_pages" : number_of_pages, "first_landing" : False})

    def parse(self, response):
        if response.url in self.start_urls:
            return None
        else:
            sku = response.xpath("//div[@class='row desc_info']").re(self.sku_pattern)
            try:
                sku = sku[0].split(":")[-1].strip()
            except IndexError:
                pass
            else:
                images = [f"https:{d}" for d in response.xpath("//div[@class='row detalhes produto']//img/@src").getall() if d.startswith("//maze")]
                image_uris = [f"{self.settings.get('IMAGES_STORE')}{sku}_{filename.split('/')[-1]}" for filename in images]
                product_container = response.xpath("//div[@class='type-grid']|//div[@class='ui grid stackable produto']")
                i = ItemLoader(item=MazeItem(), selector=product_container)
                i.add_value("brand", self.brand)
                i.add_xpath("product", "//h1[@class='nomeProduto']")
                i.add_xpath("full_price", "//span[@id='preco-antigo']")
                i.add_xpath("price", "//span[@itemprop='price']")
                i.add_xpath("currency", "//span[@itemprop='price']")
                i.add_value("url", response.url)
                i.add_xpath("store_sku", "//h6[@class='codProduto']")
                i.add_value("sku", response.xpath("//div[@class='row desc_info']").re(self.sku_pattern))
                i.add_value("stock_info", json.loads(response.xpath("//input[@id='json-detail']/@value").get()))
                i.add_value("has_stock", json.loads(response.xpath("//input[@id='json-detail']/@value").get()))
                i.add_xpath("description", "//div[@class='row desc_info']")
                i.add_value("image_urls", images)
                i.add_value("image_uris", image_uris)
                i.add_value("spider_version", self.version)
                i.add_value("spider", self.name)
                yield i.load_item()