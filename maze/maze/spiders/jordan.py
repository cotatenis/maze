from maze.spiders.nike import MazeNikeSpider
from math import ceil
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

class MazeJordanSpider(MazeNikeSpider):
    name = "maze-jordan"
    start_urls = ["https://www.maze.com.br/categoria/tenis/nike"]
    brand = 'Jordan'

    def middle(self, response):
        total_products = 0
        number_of_products = response.xpath("//input[@name='JORDAN']/../label/text()").re(r"\d+")
        if number_of_products:
            total_products = int(number_of_products[0])

        if total_products:
            number_of_pages = ceil(total_products/48)
            url = "https://www.maze.com.br/product/getproductscategory/?path=%2Fcategoria%2Fnike%2Fjordan&viewList=g&pageNumber=1&pageSize=48&order=&brand=&category=124814&group=&keyWord=&initialPrice=&finalPrice=&variations=&idAttribute=&idEventList=&idCategories=&idGroupingType="
            yield Request(url=url, cb_kwargs={"number_of_pages" : number_of_pages, "first_landing" : True}, callback=self.pagination)

    def pagination(self, response, number_of_pages, first_landing):
        product_details = LinkExtractor(restrict_xpaths="//a[@class='ui image fluid attached']")
        for link in product_details.extract_links(response):
            yield Request(url=link.url, callback=self.parse)
        if first_landing:
            for page in range(2, number_of_pages+1):
                url = f"https://www.maze.com.br/product/getproductscategory/?path=%2Fcategoria%2Fnike%2Fjordan&viewList=g&pageNumber={page}&pageSize=48&order=&brand=&category=124814&group=&keyWord=&initialPrice=&finalPrice=&variations=&idAttribute=&idEventList=&idCategories=&idGroupingType="
                yield Request(url=url, method='GET', callback=self.pagination, cb_kwargs={"number_of_pages" : number_of_pages, "first_landing" : False})


