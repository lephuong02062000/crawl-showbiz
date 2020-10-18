import scrapy

from datetime import datetime
import json
name_list = []
OUTPUT_FILENAME = 'D:/Phuonglt/Projects/PycharmProjects/showbiz_crawl/showbiz_crawl/spiders/Output/showbiz{}.json'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
class ShowbizSpider(scrapy.Spider):
    name = 'showbiz'
    allowed_domains = ['https://nguoinoitieng.tv/']
    start_urls = ['https://nguoinoitieng.tv/sinh-thang/1',
                  'https://nguoinoitieng.tv/sinh-thang/2',
                  'https://nguoinoitieng.tv/sinh-thang/3',
                  'https://nguoinoitieng.tv/sinh-thang/4',
                  'https://nguoinoitieng.tv/sinh-thang/5',
                  'https://nguoinoitieng.tv/sinh-thang/6',
                  'https://nguoinoitieng.tv/sinh-thang/7',
                  'https://nguoinoitieng.tv/sinh-thang/8',
                  'https://nguoinoitieng.tv/sinh-thang/9',
                  'https://nguoinoitieng.tv/sinh-thang/10',
                  'https://nguoinoitieng.tv/sinh-thang/11',
                  'https://nguoinoitieng.tv/sinh-thang/12'
                  ]
    CRAWLED_COUNT = 0

    def parse(self, response):
        link_profiles = response.css('a.tennnt::attr(href)').getall()
        for link_profile in link_profiles:
            link_profile = response.urljoin(link_profile)
            yield scrapy.Request(link_profile, callback=self.get, dont_filter=True)
        next_page = response.css('link[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
            print(next_page)

    def get(self, response):
        print('Crawling from:', response.url)
        text = response.css('div.motangan > p::text').getall()
        b = response.css('div.motangan > p > b::text').getall()
        data = {
            'name': response.css('div.motangan > h2::text').get(),
            'field': response.css('a.nganhhd::text').get(),
            'loc1': text[0],
            'dob_age': text[1],
            'log2': b[2],
            'microRank': response.css('span.starnumber::text').getall()[1],
            'macroRank': text[3],
            'fbLink': response.css('div.motangan > p > a[rel="nofollow"]::attr(href)').get()

        }
        print(data)
        with open(OUTPUT_FILENAME, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write('\n')
            self.CRAWLED_COUNT += 1
            self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
            print('SUCCESS:', response.url)