# -*- coding: utf-8 -*-
import scrapy
import urlparse
from my_spider.items import CraiglistItem


def take_first(xpath, if_empty=None):
    l = xpath.extract()
    if not l:
        return if_empty
    return l[0]

class CraiglistSpider(scrapy.Spider):
    name = "craiglist"
    start_urls = (
        'http://www.craiglist.org/about/sites',
    )
    download_delay = 2

    def parse(self, response):
        country_region_node = response.xpath('//div[@class="colmask"]/div/h4')
        for node in country_region_node:
            country = take_first(node.xpath('text()'))
            area_nodes = node.xpath('following-sibling::ul[1]/li/a')

            for area_node in area_nodes:
                area = take_first(area_node.xpath('text()'))
                area_link = take_first(area_node.xpath('@href'))
                yield scrapy.Request(area_link,
                                     meta={'country': country,
                                           'area': area},
                                     callback=self.parse_area)

    def parse_area(self, response):
        category_nodes = response.xpath('//div[@class="cats"]/ul/li')
        for node in category_nodes:
            category = take_first(node.xpath('a/span/text()'))
            category_link = take_first(node.xpath('a/@href'))
            full_category_link = urlparse.urljoin(response.url, category_link)
            meta = {'category': category}
            meta.update(response.meta)
            yield scrapy.Request(full_category_link,
                                 meta=meta,
                                 callback=self.parse_category)

    def parse_category(self, response):
        item_nodes = response.xpath('//p[@data-pid]')
        next_url = take_first(response.xpath('//a[@class="button next"]/@href'))
        for node in item_nodes:
            item_link = take_first(node.xpath('span/span/a/@href'))
            full_item_link = urlparse.urljoin(response.url, item_link)
            item_title = take_first(node.xpath('span/span/a/text()'))
            meta = {'title': item_title}
            meta.update(response.meta)
            yield scrapy.Request(full_item_link, self.parse_item, meta=meta)

        if next_url:
            full_next_url = urlparse.urljoin(response.url, next_url)
            yield scrapy.Request(full_next_url,
                                 self.parse_category,
                                 meta=response.meta)

    def parse_item(self, response):
        meta = response.meta
        descr = take_first(response.xpath('//section[@id="postingbody"]/text()'))
        item = CraiglistItem(country=meta['country'],
                             area=meta['area'],
                             category=meta['category'],
                             title=meta['title'],
                             description=descr)
        yield item
