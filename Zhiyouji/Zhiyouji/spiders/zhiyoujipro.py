# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from Zhiyouji.items import ZhiyoujiItem
import scrapy
import time
import re


class ZhiyoujiproSpider(CrawlSpider):
    name = 'zhiyoujipro'
    allowed_domains = ['jobui.com']
    start_urls = ['https://www.jobui.com/company/1501781/']

    rules = (
        # 匹配https://www.jobui.com/company/10689096/
        Rule(LinkExtractor(allow=r'https://www.jobui.com/company/\d+/$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['area'] = response.xpath('//*[@id="city-name"]/@value').extract_first()
        item['area_code'] = response.xpath('//*[@id="areaCode"]/@value').extract_first()
        item['url'] = response.url
        item['date'] = time.time()
        item['brief_name'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        print (item['brief_name'])
        try:
            item['view_num'] = response.xpath('//div[2]/div[@class="company-banner-segmetation"]/span/text()').extract_first().strip().split('\xa0/\xa0')[0].strip()
        except:
            item['view_num'] = 0
        try:
            item['eval_num'] = response.xpath('//div[2]/div[@class="company-banner-segmetation"]/span/text()').extract_first().strip().split('\xa0/\xa0')[1].strip()
        except:
            item['eval_num'] = 0
        try:
            item['focur_num'] = response.xpath('//div[2]/div[@class="company-banner-segmetation"]/span/text()').extract_first().strip().split('\xa0/\xa0')[2].strip()
        except:
            item['focur_num'] = 0
        try:
            item['brief_intro'] = response.xpath('//div[@class="fl"]/div[3]/p/text()').extract_first().strip()
        except:
            item['brief_intro'] = 0
        item['admire_num'] = response.xpath('//div[@class="banner-praise-box"]/button[1]/span[3]/text()').extract_first().strip()
        item['negative_num'] = response.xpath('//span[@class="graise-general-num j-graise-general-num"]/text()').extract_first().strip()
        item['property'] = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[1]/text()').extract_first().strip()
        item['industry'] = response.xpath('//*[@id="cmp-intro"]/div/div/dl/dd[2]/a//text()').extract()
        try:
            item['full_name'] = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[3]/text()').extract_first().strip()
        except:
            item['full_name'] = 0
        try:
            item['detail_intro'] = response.xpath('//*[@id="textShowMore"]/text()').extract_first().strip()
        except:
            item['detail_intro'] = 0

        # 　获取社会评价信息
        ban_title = response.xpath('//div[3]/div[1]/div[1]/div[2]/div[1]/h2/text()').extract_first()
        if ban_title is not None:
            item['good_repu_level'] = response.xpath('//div[@class="company-how-comment-box"]/div[1]/div[1]/div[1]/text()').extract_first()
            honor_box = response.xpath('//div[@class="company-how-rank-box j-company-honor"]')
            # print(honor_box)
            item['honors'] = 0
            if len(honor_box) != 0:
                honor_list = []
                for i in range(1,len(honor_box.xpath('//div[@class="company-how-rank-box j-company-honor"]/div'))+1):
                    temp = {}
                    # honor = 'honor_%d'%i
                    honor = honor_box.xpath('./div[%d]/a/text()'%i).extract_first()
                    # print(honor)
                    temp[honor] = ''.join(honor_box.xpath('./div[%d]/span/text()'%i).extract())
                    # print (temp[honor])
                    honor_list.append(temp)
                item['honors'] = honor_list
            # print (item['honors'])


        # 获取招聘概况
        ban_title1 = response.xpath('//*[@class="job-per-year-title-box"]').extract_first()
        # print (ban_title1)
        # 判断有没有这个模块在页面上
        if ban_title1 is not None:
            try:
                item['jobs_address'] = 'https://www.jobui.com' + response.xpath('//*[@class="m-more s-color"]/@href').extract()[0]
            except:
                item['jobs_address'] = 0
             # print(item['jobs_address'])
            recruit_box = response.xpath('//*[@class="job-overview-area"]')
            # print(recruit_box)
            # print('-'*30)
            item['city_recruit_nums'] = 0
            # 判断有没有这个类型的数据，获取各个城市的招聘人数
            if len(recruit_box) != 0:
                temp = {}
                for i in response.xpath('.//div[@class="job-overview-area"]/a'):
                    city = i.xpath('./span[1]/text()').extract_first()
                    # print(city+'-'*30)
                    temp[city] = i.xpath('./span[2]/text()').extract_first()
                    # print(temp[city]+'-'*30)
                item['city_recruit_nums'] = temp
        #     #     print (item['city_recruit_nums'])

        #     # 判断有没有柱状表
            recruit_box1 = response.xpath('.//div[@class="job-overview-area-box"]/div[2]/div[2]')
        #     # print(recruit_box1)
            if len(recruit_box1) != 0:
                item['rec_up_down_info'] = ''.join(recruit_box1.xpath('./div[1]/span/text()').extract())
                # print(recruit_box1.xpath('./div[1]/span/text()').extract())
                diagram = recruit_box1.xpath('./div[2]/div/span')
                temp = {}
                for i in diagram:
                    # print(i.xpath('./em[1]/text()'))
                    year = i.xpath('./em[1]/text()').extract_first()
                    temp[year] = i.xpath('./em[2]/text()').extract_first()
                try:
                    item['year_recruit_nums'] = temp
                except:
                    item['year_recruit_nums'] = 0
        #     # print(item['year_recruit_nums'])
        #     # print(temp) ../div[@="class"]/following-sibling::div[1]


        # 获取薪资状况
        ban_title2 = response.xpath('//*[@class="company-salary-analysis-box"]')
        # print(len(ban_title2))
        if ban_title2 is not None:
            try:
                item['payment_analysis_url'] = 'https://www.jobui.com' + response.xpath('//*[@class="m-more s-color"]/@href').extract()[-1]
            except:
                item['payment_analysis_url'] = 0
            temp = {}
            for i in response.xpath('//div[@class="company-salary-analysis-box"]/div'):
                key = i.xpath('./span[1]/text()').extract_first().strip()
                temp[key] =''.join([x.strip().replace(' ','') for x in i.xpath('./span[2]//text()').extract()])
            item['payment_analysis'] = temp
            # print(item['payment_analysis'])

            # 判断有没有柱状表
            payment_box1 = response.xpath('//*[@class="salary-analysis-table"]')
            # print(recruit_box1)
            if len(payment_box1) != 0:
                item['payment_up_down_info'] = ''.join(response.xpath('//*[@class="salary-analysis-desc"]/span/text()').extract())
                # print(recruit_box1.xpath('./div[1]/span/text()').extract())
                diagram = response.xpath('//*[@class="salary-analysis-table"]/span')
                temp = {}
                try:
                    for i in diagram:
                        # print(i.xpath('./em[1]/text()'))
                        pay_level = i.xpath('./em[2]/text()').extract_first().replace('.',',')
                        temp[pay_level] = i.xpath('./em[1]/text()').extract_first()
                        item['payment_nums'] = temp
                except:
                    item['payment_nums'] = 0
            # print(item['payment_nums'])
            # print(temp)


        # 获取地址联系信息
        ban_title3 = response.xpath('//*[@class="edit-address"]/text()')
        if ban_title3 is not None:
            try:
                item['address'] = response.xpath('//*[@class="edit-address"]/text()').extract_first()
            except:
                item['address'] = 0

            try:
                item['company_url'] = response.xpath('//*[@class="edit-webstie"]/@href').extract_first()
            except:
                item['company_url'] =0


        # 获取工商信息
        page_code = re.findall(r'\d+',response.url)[0]

        ind_com_url = 'https://www.jobui.com/async/company_info_businessInfo/'+page_code+'&isPc.html'
        item['ind_com_url'] = ind_com_url
        # yield scrapy.Request(url=ind_com_url, callback=self.parse_ind_com)

        return item

