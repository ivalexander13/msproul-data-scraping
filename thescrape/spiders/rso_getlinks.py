import scrapy
import json
import math

class RsoLinksSpider(scrapy.Spider):
    name = "rso-links"

    start_urls = [ 
        'file:///home/ivalexander13/msproul-local/ms-scraping/thescrape/thescrape/rso_htmls/all-cut.html',
    ]

    def parse(self, response):
        all_links = response.css('div div a::attr(href)').getall()
        fname = 'all-links.txt'
        with open(fname, 'w') as f:
            for a in all_links:
                f.write(a + '\n')
            f.close()        
        