import scrapy,re,time


class CarsSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://club.autohome.com.cn/bbs/forum-o-200028-1.html']
    base_url = 'http://club.autohome.com.cn'
    TAG_RE = re.compile(r'<[^>]+>')
    f = open(r'content1.txt', 'ab')
    default_encode = 'utf8'

    def parse(self, response):
        # get all the post url in the page
        for url in response.css('.a_topic').xpath('./@href'):
            # decrease the  affect of network flow or the antiCrawler
            time.sleep(2)
            print("---------------"+self.base_url + url.extract())
            yield scrapy.Request(self.base_url + url.extract(), self.parse_posts)

        # get the next page url
        xurl = response.xpath('//a[@class="afpage"]/@href').extract()[0]
        if (xurl != ''):
            print("###########" + self.base_url + xurl)
            self.parse(self.base_url + xurl)
            yield scrapy.Request(self.base_url + xurl, self.parse)
            self.f.flush()
        else:
            self.f.close()

    def parse_posts(self, response):
        # get the post context  encode with utf8
        conext = self.get_post(response)
        # get the post title
        post_title = response.css('.maxtitle::text').extract()[0]
        sql2 = self.add_str(conext, post_title)

        # # get the post time
        post_date = response.xpath('//div[@id="F0"]/div').xpath('./div/span[@xname="date"]/text()').extract()[0]
        sql2 = self.add_str(sql2, post_date)

        # # get the author register time
        reg_date = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[5]/text()').extract()[0]
        sql2 = self.add_str(sql2, reg_date)
        # self.write_comp(reg_date,'reg_date')

        #  get the author location
        author_loc = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[6]/a[1]/text()').extract()[
            0]
        sql2 = self.add_str(sql2, author_loc)

        #
        # # get the author nickname
        nickname = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="maxw"]/li[1]/a/text()').extract()[0]
        sql2 = self.add_str(sql2, nickname)
        # get userid
        userid = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li/p/a[1]/@href').re(r'\/[0-9]{1,}\/')[
                0]
        sql2 = self.add_str(sql2, userid.strip('/'))
        # self.write_comp(userid.strip('/'),'userid')

        #  get the verified authors'car
        car = ''
        author_car = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[7]/a[2]/@title').extract()
        if (len(author_car) == 0):
            car = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[7]/a[1]/@title').extract()[0]
        else:
            car = author_car[0]
        sql2 = self.add_str(sql2, car)

        # get the verfied mark
        verfied = '0'
        owner = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="maxw"]/li[1]/a[2]/@title').extract()
        if (len(owner) != '0'):
            verfied = '1'
        sql2 = self.add_str(sql2, verfied)
        # print(sql2)
        self.f.write(sql2.encode(self.default_encode))
        self.f.write('\n')
        # time.sleep(5)

    def add_str(self, old, zz):
        x = old + '|' + zz
        return x

    # remove the  html tag in the post content
    def remove_tags(self, text):
        return self.TAG_RE.sub('', text)

    # get the post context
    def get_post(self, response):
        conext = response.xpath('//div[@xname="content"]').xpath('./div[@class="w740"]').extract()[0].strip('\'')
        conext = conext.replace('\r\n', '').replace('|', '')
        conext = self.remove_tags(conext)
        return conext
