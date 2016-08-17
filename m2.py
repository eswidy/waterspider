import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://club.autohome.com.cn/bbs/forum-o-200028-1.html']
    base_url= 'http://club.autohome.com.cn'

    def parse(self, response):
        #get all the post url in the page
        # for url in response.css('.a_topic').xpath('./@href'):
        #     print("------------------------------")
        #     print(self.base_url + url.extract())
        #     yield scrapy.Request(self.base_url + url.extract(), self.parse_posts)
        #get the next page url
        xurl = response.xpath('//a[@class="afpage"]/@href').extract()[0]
        print('----------------------------')
        print(self.base_url+xurl)
    def parse_posts(self, response):
        # get the post context
        # for context in  response.css('.conttxt').xpath('//p/text()'):
        #     yield {'context': context}
        # get the post title
        for title in response.css('.rtitle').xpath('//div/[@class="maxtitle"]'):
            yield {'title': title}
        # get the post time
        # for date in response.css('#F0').xpath('//span[@xname="date"]'):
        #     yield {'post_date': date}


