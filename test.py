# encoding=utf8
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    # start_urls = ['http://club.autohome.com.cn/bbs/thread-o-200028-34537139-1.html']
    start_urls = ['http://club.autohome.com.cn/bbs/thread-o-200028-37396734-1.html']
    base_url= 'http://club.autohome.com.cn'
    sql_prefix = 'insert into autousers(context,post_title,reg_date,post_date,author_loc,nickname,userid,car,verfied) values('
    sql_suffix = ')'
    default_encode = 'utf8'
    src = 'autohome'
    f = open(r'content1.txt', 'wb')

    def parse(self, response):
        # get the post context  encode with utf8
        conext = response.xpath('//div[@class="conttxt"]').xpath('./div[@class="w740"]').extract()[0].strip('\'')
        # get the post title
        post_title = response.css('.maxtitle::text').extract()[0];
        sql2 = self.add_str(conext,post_title)

        # # get the post time
        post_date = response.xpath('//div[@id="F0"]/div').xpath('./div/span[@xname="date"]/text()').extract()[0]
        sql2 = self.add_str(sql2, post_date)

        # # get the author register time
        reg_date = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[5]/text()').extract()[0]
        sql2 = self.add_str(sql2, reg_date)
        # self.write_comp(reg_date,'reg_date')

        #  get the author location
        author_loc = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[6]/a[1]/text()').extract()[0]
        sql2 = self.add_str(sql2, author_loc)

        #
        # # get the author nickname
        nickname = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="maxw"]/li[1]/a/text()').extract()[0]
        sql2 = self.add_str(sql2, nickname)
        # get userid
        userid = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li/p/a[1]/@href').re(r'\/[0-9]{1,}\/')[0]
        sql2 = self.add_str(sql2, userid.strip('/'))
        # self.write_comp(userid.strip('/'),'userid')

        #  get the verified authors'car
        car = ''
        author_car = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[7]/a[2]/@title').extract()
        if(len(author_car) ==0):
            car = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[7]/a[1]/@title').extract()[0]
        else:
            car = author_car[0]
        sql2 = self.add_str(sql2, car)

         # get the verfied mark
        verfied = '0'
        owner = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="maxw"]/li[1]/a[2]/@title').extract()
        if( len(owner) != '0'):
            verfied = '1'
        sql2 = self.add_str(sql2, verfied)
        print(sql2)

    def add_str(self,old,zz):
        x = old + '|'  +zz
        print(zz)
        return x














