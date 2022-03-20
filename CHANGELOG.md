# Change Log
Arquivo para documentação das mudanças realizadas ao longo do projeto. O formato desse arquivo é baseado no [Keep a Changelog](http://keepachangelog.com/)
e o presente projeto adota o [Semantic Versioning](http://semver.org/).

## [0.7.0] - 2021-11-16
- [COT-248](https://ecoanalytics.atlassian.net/browse/COT-248)
### Adicionado
- Sobrescrito a função `image_downloaded` do objeto `ImagesPipeline` para garantir a persistência de apenas imagens que ainda não estão salvas no storage.
## [0.6.0] - 2021-11-02
- [COT-307](https://ecoanalytics.atlassian.net/browse/COT-307)
### Adicionado
- Adicionado as spiders `MazeJordanSpider` e `MazeNikeSpider`
- Adicionado `ItemCountMonitor` aos monitores das spiders.
### Removido
- Removido a persistência das imagens em dimensões 800x600.
### Alterado
- Alterado o código da spider `MazeAdidasSpider`

## [0.5.0] - 2021-10-29
 - [COT-293](https://ecoanalytics.atlassian.net/browse/COT-293)
### Alterado
- Alterado o parâmetro `SPIDERMON_VALIDATION_DROP_ITEMS_WITH_ERRORS` para False.
### Excluído
- Retirado o Monitor `Item validation`.

## [0.4.0] - 2021-10-09
 - [COT-200](https://ecoanalytics.atlassian.net/browse/COT-200)
### Alterado
- Alterado o parâmetro `IMAGES_THUMBS` para coletar imagens de 400x400.

## [0.3.0] - 2021-10-04
 - [COT-152](https://ecoanalytics.atlassian.net/browse/COT-152)
### Adicionado
- Adicionado camada de monitoramento via [sentry](https://sentry.io/) ao projeto.
- Adicionados novos monitores: `FinishReasonMonitor`, `UnwantedHTTPCodesMonitor`, `ErrorCountMonitor`.

## [0.2.0] - 2021-10-03
 
- [COT-145](https://ecoanalytics.atlassian.net/browse/COT-143)
### Adicionado
- Adicionado camada de monitoramento via [spidermon](https://github.com/scrapinghub/spidermon) ao projeto.
- Envio de mensagem ao Discord em caso de url de produto sem sku.