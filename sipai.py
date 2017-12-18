# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# 请求函数
def getpage():
    # 初始化浏览器对象
    browser = webdriver.Chrome()
    browser.get('https://sf.taobao.com/item_list.htm?spm=a213w.3064813.a214dqe.3.ZH7dnc&category=50025969')

    time.sleep(5)
    # 获取html
    html = browser.page_source
    # 调用解析函数
    listpage(html)
    # 死循环点击下一页
    page_num = 2
    while True:
        browser.find_element_by_class_name('next').click()
        print("正在解析第%s页" % str(page_num))
        time.sleep(3)
        html = browser.page_source
        listpage(html)
        page_num += 1
        # 点到最后一页停止
        if 'next unavailable' in browser.page_source:
            break
# 解析函数
def listpage(html):
    # print('正在解析．．．')
    html = BeautifulSoup(html,'lxml')
    shop_list = html.select('div.sf-item-list ul.sf-pai-item-list li')
    with open('taobao.xls', 'a') as f:
        excel_list = []
        for i in shop_list:
            # image = i.select('div.header-section .pic')[0].text
            title = i.select('div.header-section p.title')[0].text
            print(title)
            current_price = i.select('div.info-section p.price-todo span.value')[0].text
            print(current_price)
            price_assess = i.select('div.info-section p.price-assess span.value')
            if len(price_assess) > 0:
                price_assess = price_assess[0].text
            else:
                price_assess = 'non-existent'
            print(price_assess)
            bid_tips = i.select('span.bid-tips em.pai-xmpp-bid-count')[0].text.strip()
            print(bid_tips)
            viewer_count = i.select('div.footer-section p.num-auction')[0].text
            print(viewer_count)
            apply_num = i.select('div.footer-section p.num-apply')[0].text
            print(apply_num)
            start_time = i.select('p.time-todo span.value')[0].text
            end_time = i.select('p.time-doing span.value')[0].text
            excel_list.append(','.join([title,current_price,price_assess,bid_tips, viewer_count,apply_num,start_time,end_time])+'\n')
            f.writelines(excel_list)

if __name__ == '__main__':
    getpage()
