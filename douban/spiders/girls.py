# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from items import GirlItem

class GirlsSpider(scrapy.Spider):
    name = 'girls'
    allowed_domains = ['www.douban.com']
    start_urls = ['https://www.douban.com/group/641424/discussion?start=25']

    # 重写start_requests方法
    # def start_requests(self):
    #     # 浏览器用户代理
    #     headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    #     return [scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=headers)]


    def parse(self, response):
        
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        # print("开始打印soup")
        # print(soup)
        table = soup.table
        tr_arr = table.find_all("tr")

        

        for tr in tr_arr:
            item = GirlItem()

            tds = tr.find_all('td')
            item['title'] = tds[0].get_text().replace('\n','').replace(' ', '')
            item['author'] = tds[1].get_text().replace('\n','').replace(' ', '')
            item['lastTime'] = tds[3].get_text().replace('\n','')
            try:
                item['url'] = tds[0].find('a',href=True)['href']
                # 根据内页地址爬取
                yield scrapy.Request(item['url'], meta={'item': item}, callback=self.detail_parse)

            except:
                item['url'] = ""
            
        #找到下一个链接，也就是翻页
        next_url = soup.find(name='div', attrs={"class":"paginator"}).find(name='span', attrs={"class":"next"}).find(name='link')['href']
        if next_url:
            print("开始下一页")
            yield scrapy.Request(next_url, callback=self.parse)


    def detail_parse(self, response):
        # 接收上级已爬取的数据
        item = response.meta['item']
        try:
            item['detail_time'] = response.xpath('//*[@id="topic-content"]/div[2]/h3/span[2]/text()').extract()[0]
        except BaseException as e:
            print(e)
            item['detail_time'] = ""
        try:
            item['detail_report'] = response.xpath('//*[@id="link-report"]').extract()[0].replace('\n','')
        except BaseException as e:
            print(e)
            item['detail_report'] = ""
            
        write_to_file('E:/douban-detail.txt', item)
        # return item

def write_to_file (file_name, txt):
        # print("正在存储文件" + str(file_name))
        # w 如果没有这个文件将创建这个文件
        '''
        'r'：读
        'w'：写
        'a'：追加
        'r+' == r+w（可读可写，文件若不存在就报错(IOError)）
        'w+' == w+r（可读可写，文件若不存在就创建）
        'a+' ==a+r（可追加可写，文件若不存在就创建）
        '''
        f = open(file_name, 'a', encoding='utf-8')
        f.write(str(txt))
        f.close()   


