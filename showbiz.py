import scrapy

from datetime import datetime
import json
name_list = []
OUTPUT_FILENAME = 'D:/PycharmProjects/VnExpress/tutorial/vnExpress/vnExpress/spiders/Output/showbiz/showbiz{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
class ShowbizSpider(scrapy.Spider):
    name = 'showbiz'
    allowed_domains = ['https://nguoinoitieng.tv/']
    start_urls = ['https://nguoinoitieng.tv/nghe-nghiep/ca-si']
    CRAWLED_COUNT = 0

    def parse(self, response):
        print('Crawling from:', response.url)
        title = response.css('title::text').get()
        name = response.css('a.tennnt::text').getall()
        for i in name:
            with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
                f.write(json.dumps(i, ensure_ascii=False))
                f.write('\n')
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)
        next_page = response.css('link[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
            print(next_page)