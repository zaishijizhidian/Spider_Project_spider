# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from copy import deepcopy

import time
from requests import request

from baidu_music.items import BaiduMusicItem


class BdmusicSpider(scrapy.Spider):
    name = 'BDMusic'
    # allowed_domains = ['music.baidu.com','tingapi.ting.baidu.com','yinyueshiting.baidu.com']
    allowed_domains = ['baidu.com']
    start_urls = ['http://music.baidu.com/tag/%E6%96%B0%E6%AD%8C']

    def parse(self, response):
        item = BaiduMusicItem()
        temp_url = "http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&songid={}"
        sid_list = response.xpath("//span[@class='song-title']/a[1]/@href").extract()
        # print(type(sid_list))
        for sid in sid_list:

            song_id = sid.split('/')[-1]
            # print(song_id)
            item["url"] = temp_url.format(song_id)
            print(item["url"])
            yield scrapy.Request(
                item["url"],
                callback=self.parse_url,
                meta={"item": deepcopy(item)}
            )

            # item["img_list"] = div.xpath("./a/@href").extract_first()
            #获取下一页链接
            # time.sleep(10)
            temp_next_url = response.xpath("//a[@class='page-navigator-next']/@href").extract_first().strip()
            if temp_next_url is not None:
                next_url ="http://music.baidu.com" + temp_next_url
                yield scrapy.Request(next_url, callback=self.parse)
            #

    def parse_url(self,response):
        item = response.meta["item"]
        #采用xpath 获取item信息,但是无法获取下载音乐的链接
        # div_list = response.xpath("//div[@class='song-item clearfix']")
        # song_list = response.xpath("//span[@class='song-title']")
        # for div in div_list:

            # item["name"] = div.xpath("./span[@class='song-title']/a/text()").extract_first()
            # item["singer"] = div.xpath("./span[@class='singer']/span/@title").extract_first()
            # item["album"] = div.xpath("./span[@class='album-title']/a/text()").extract_first()
        # item = response.meta["item"]
        json_content = requests.get(item["url"]).text
        # print(json_content)
        content = json.loads(json_content)
        # print(content)
        item["name"] = content['songinfo']['title']
        item["singer"] = content['songinfo']['author']
        item["album"] = content['songinfo']["album_title"]
        item["href"] = content['bitrate']['show_link']
        # print(item["href"])
        yield scrapy.Request(
            item["href"],
            callback=self.parse_json,
            meta={"item": deepcopy(item)}
                    )
    def parse_json(self,response):
        item = response.meta["item"]
        print(item)
        with open(item["name"]+".mp3","wb") as f:
            f.write(response.body)
            print("%s 保存成功" % item["name"])

