# -*- coding: utf-8 -*-
# @Date  : 2017-10-06 10:04:06
# @Author: Alan Lau (rlalan@outlook.com)

import re
import ast
import json
import time
import random
import requests
from TB_model import Wires
from reader import writetxt as wt
from bs4 import BeautifulSoup
from datetime import datetime as dt


def buildheader(page):
    page = page * 22
    url = 'https://s.taobao.com/search?q=%E7%94%B5%E7%BC%86%E7%BA%BF&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20171006&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s=' + \
        str(page)
    headers = {
        "(Status-Line)": "HTTP/2.0 200 OK",
        "date": "Fri, 06 Oct 2017 02:03:21 GMT",
        "content-type": "text/html;charset=UTF-8",
        "vary": "Accept-Encoding",
        "set-cookie": "JSESSIONID=61CD25233F6CC5A9AB061BA15221CFDE; Path=/; HttpOnly",
        "content-language": "zh-CN",
        "content-encoding": "gzip",
        "server": "Tengine/Aserver",
        "eagleeye-traceid": "0b8c0b6a15072554007664775e017b",
        "strict-transport-security": "max-age=31536000",
        "timing-allow-origin": "*",
        "X-Firefox-Spdy": "h2"
    }
    data = {
        "q": "电缆线",
        "imgfile": "",
        "commend": "all",
        "ssid": "s5-e",
        "search_type": "item",
        "sourceId": "tb.index",
        "spm": "a21bo.50862.201856-taobao-item.1",
        "ie": "utf8",
        "initiative_id": "tbindexz_20171006",
        "bcoffset": "4",
        "ntoffset": "4",
        "p4ppushleft": "1,48",
        "s": str(page)
    }
    return url, headers, data


def reqweb(page):
    url, headers, data = buildheader(page)
    try:
        r = requests.get(headers=headers, url=url, data=data)
        r.encoding = 'utf-8'
        s = BeautifulSoup(r.text, 'html.parser')
        parser(page, s)
    except Exception as e:
        print(e)
        with open(r'errorlist.txt', 'a', encoding='utf8') as f:
            f.write('page:' + str(page) + '\t' +
                    'page error' + '\t' + str(e) + '\n')
        pass


def parser(page, s):
    scripts = s.find_all('script')
    sj = None
    global id
    for ss in scripts:
        if 'g_page_config = ' in ss.get_text():
            sj = ss.get_text().replace('g_page_config = ', '')
            print('get')
            sjson = sj[:-1]
            title = re.findall(r'"raw_title":"([^"]+)"', sjson, re.I)
            price = re.findall(r'"view_price":"([^"]+)"', sjson, re.I)
            detail_url = re.findall(r'"detail_url":"([^"]+)"', sjson, re.I)
            user_ids = re.findall(r'"user_id":"([^"]+)"', sjson, re.I)

            for i in range(len(detail_url)):
                goodsdetail = {}
                goodsdetail['title'] = title[i]
                goodsdetail['price'] = price[i]
                goodsdetail['url'] = detail_url[i].encode(
                    'utf-8').decode('unicode_escape')
                goodsdetail['page'] = page
                goodsdetail['user_id'] = user_ids[i]
                ifrepeat = Wires.select().where(
                    Wires.url == goodsdetail['url'])
                if len(ifrepeat) != 0:
                    continue
                else:
                    Wires.create(**goodsdetail)

            break
    # print(str(detail_url[0].encode('utf-8').decode('unicode_escape')))


# gurl =
# 'https://click.simba.taobao.com/cc_im?p=%B5%E7%C0%C2%CF%DF&s=878109219&k=525&e=mt5HIluviEdllIXfrF%2BhICB6uWSHNdgzBd5ypZDHPxAwUkFqIgSsG2sgcdeuLmC2x2J1rXa%2FZbwtJgo95rAhWycQXdibhWstmfD3a45ZzPaAMiyPD42ffxOtw77WghKuATKWItUKSmt3%2FK%2Bzfb0Gg3m83X5ilU8L4jhklu8XGDQ7De69lgcXrzdxP38rIXr3Gk01d%2BpeD9w13%2FzK%2B9kOs11BePoDhy9vieeO0sd0B8JZTbIjHg3QeaC7qj1%2BhZ3%2BdAsWAsPJwpVZ4xC9IFb82A0sNGVLHXWFGutVwf5q%2FPbtyMNTwNHSed7EcPqXTol3lvsfSdV8xiXLURkmjhqkNpcnyMQ9k2oTIex3oWVEEpIFDQiH%2BPgpPFKilgRMlgpXpFgE0GpDtU2Bq11nkg2Tsg4oDxVNGAyr0QZo6c8I4U4S9auKbjORcILEkIrIL8O4Dmj3%2FijmS7UTRkCUXBcBPHSR0tBVKg74GADPXMMkuO%2BsBrF3XGywWHQ5gdsqm8uefOdJzWAK1ks%3D#detail'


def main():
    for page in range(1, 101):
        reqweb(page)
        print('page:%s done...' % page)
        time.sleep(random.uniform(0.5, 2))


if __name__ == '__main__':
    ts = dt.now()
    main()
    te = dt.now()
    tdif = te - ts
    print('[%s]' % tdif)
