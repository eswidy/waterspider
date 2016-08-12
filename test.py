# encoding=utf8
import scrapy,mysql.connector

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    # start_urls = ['http://club.autohome.com.cn/bbs/thread-o-200028-34537139-1.html']
    start_urls = ['http://club.autohome.com.cn/bbs/thread-o-200028-37396734-1.html']
    base_url= 'http://club.autohome.com.cn'
    sql_prefix = 'insert into autousers(context,post_title,reg_date,post_date,author_loc,nickname,userid,car,verfied) values('
    sql_suffix = ')'
    default_encode = 'utf8'
    src = 'autohome'
    conn = mysql.connector.connect(host='127.0.0.1', user='root', passwd='root@mysql', db='cardb', port=3306)
    cursor = conn.cursor()
    f = open(r'content1.txt', 'wb')

    def parse(self, response):
        # get the post context  encode with utf8
        sql = ''
        obj = []
        conext = response.xpath('//div[@class="conttxt"]').xpath('./div[@class="w740"]').extract()[0].strip('\'')
        obj.append(conext)
        print(unicode(conext, 'UTF-8').encode('UTF-8'))
        # self.write_comp(conext,'conext')
        # get the post title
        post_title = response.css('.maxtitle::text').extract()[0];
        obj.append(post_title)
        sql = conext + '|' + post_title
        sql2 = self.add_str('\''+conext+'\'',post_title)
        # self.write_comp(post_title, 'post_title')

        # # get the post time
        post_date = response.xpath('//div[@id="F0"]/div').xpath('./div/span[@xname="date"]/text()').extract()[0]
        obj.append(post_date)
        sql = sql + '|' + post_date
        sql2 = self.add_str(sql2, post_date)
        # self.write_comp(post_date, 'post_date')

        # # get the author register time
        reg_date = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[5]/text()').extract()[0]
        obj.append(reg_date)
        sql = sql + '|' + reg_date
        sql2 = self.add_str(sql2, reg_date)
        # self.write_comp(reg_date,'reg_date')

        #  get the author location
        author_loc = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[6]/a[1]/text()').extract()[0]
        obj.append(author_loc)
        sql = sql + '|' + author_loc
        sql2 = self.add_str(sql2, author_loc)
        # self.write_comp(author_loc,'author_loc')

        #
        # # get the author nickname
        nickname = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="maxw"]/li[1]/a/text()').extract()[0]
        obj.append(nickname)
        sql = sql + '|' + nickname
        sql2 = self.add_str(sql2, nickname)
        # self.write_comp(nickname,'nickname')
        # get userid
        userid = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li/p/a[1]/@href').re(r'\/[0-9]{1,}\/')[0]
        obj.append(userid)
        sql = sql + '|' + userid.strip('/')
        sql2 = self.add_str(sql2, userid.strip('/'))
        # self.write_comp(userid.strip('/'),'userid')

        #  get the verified authors'car
        car = ''
        author_car = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[7]/a[2]/@title').extract()
        if(len(author_car) ==0):
            car = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="leftlist"]/li[7]/a[1]/@title').extract()[0]
        else:
            car = author_car[0]
        sql = sql + '|' + car
        obj.append(car)
        sql2 = self.add_str(sql2, car)
        # self.write_comp(car,'car')

         # get the verfied mark
        verfied = '0'
        owner = response.xpath('//div[@id="F0"]/div').xpath('./ul[@class="maxw"]/li[1]/a[2]/@title').extract()
        if( len(owner) != '0'):
            verfied = '1'
        sql = sql + '|' + verfied
        obj.append(verfied)
        sql2 = self.add_str(sql2, verfied)
        # self.write_comp(verfied,'verfied')
        self.write_comp(sql2,'sql')
        self.insert_db(self.cursor,obj)
        self.conn.close()
        self.f.close()


    def write_comp(self,comp,key):
        if(comp.strip() != ''):
            self.f.write(key.encode(self.default_encode))
            self.f.write(bytes(':', 'UTF-8'))
            self.f.write(comp.encode(self.default_encode))
            self.f.write(bytes('\n', 'UTF-8'))
    def add_str(self,old,zz):
        # x = old +','+ '\''  +str+'\''
        s2 = '测试'
        s4 = 12.3
        print(unicode(zz,'UTF-8').encode('UTF-8'))
        return  s2
    def insert_db(self,cursor,obj):
        sql =  'insert into autousers(context,post_title,reg_date,post_date,author_loc,nickname,userid,car,verfied)'
        sql = sql + 'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        # cursor.execute(sql,(obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6],obj[7],obj[8]))















