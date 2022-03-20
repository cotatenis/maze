from schematics.models import Model
from schematics.types import URLType, StringType, ListType, FloatType, DateTimeType, BooleanType, ModelType, IntType

class VariationsSku(Model):
    Color = StringType()
    DisplayOrder = IntType()
    ExternalId = StringType()
    IdReference = StringType()
    IdVariation = IntType()
    Image = StringType()
    Name = StringType()
    QuantityOfProduct = StringType()
    reference_externalId = StringType()

class InstallmentMax(Model):
    Description = StringType()
    MaxNumber = IntType()
    Value = FloatType()

class Sku(Model):
    CrossDocking = StringType()
    Cubing = StringType()
    EventList = StringType()
    ExternalId = StringType()
    Gtin = StringType()
    IdSku = IntType()
    InstallmentMax = ModelType(InstallmentMax)
    ManufacturerCode = StringType()
    Metadata = StringType()
    PartNumber = StringType()
    Price = FloatType()
    PricePromotion = FloatType()
    PricePromotionCA = FloatType()
    SkuCode = StringType()
    Standard = BooleanType()
    Stock = IntType()
    Variations = ListType(ModelType(VariationsSku))
    Visible = BooleanType()
    Weight = FloatType()

class Variations(Model):
    Color = StringType()
    DisplayOrder = IntType()
    IdVariation = IntType()
    IdVariationFather = StringType()
    Image = StringType()
    Name = StringType()
    Sku = ModelType(Sku)
    SubTreeReference = StringType()


class StockInfo(Model):
    IdReference = IntType()
    Name = StringType()
    OrdinationOfReferences = IntType()
    ReferenceType = IntType()
    Variations = ListType(ModelType(Variations))


class MazeItem(Model):
    brand = StringType()
    product = StringType()
    full_price = FloatType()
    price = FloatType(required=True)
    currency = StringType()
    url = URLType(required=True)
    store_sku = StringType()
    sku = StringType(required=True)
    stock_info = ListType(ModelType(StockInfo))
    has_stock = BooleanType()
    description = StringType()
    image_urls = ListType(URLType)
    image_uris = ListType(StringType, required=True)
    spider_version = StringType(required=True)
    spider = StringType(required=True)
    timestamp = DateTimeType(required=True)


