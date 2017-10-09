# -*- coding: utf-8 -*-
# @Date  : 2017-10-06 23:46:09
# @Author: Alan Lau (rlalan@outlook.com)

import re
import time
import json
import random
import requests
from TB_model import Wires
from TB_model import Wiresdetails
from bs4 import BeautifulSoup
from pprint import pprint as p
from datetime import datetime as dt
from selenium import webdriver as wb


# proxies = {
#     'http': 'http://112.86.229.24:3128'
#     # 'https': 'http://10.10.1.10:1080',
# }


class GetTBComments:

    def __init__(self, commentsdict, url, pid, uid, cpage):
        self.url = url
        self.pid = pid
        self.uid = uid
        self.cpage = cpage
        self.commentsdict = commentsdict

    def tpBuildheader(self):
        # comrqurl = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' + \
        #     str(self.pid) + '&currentPageNum=' + str(self.cpage)
        comrqurl = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' + str(self.pid) + '&userNumId=' + str(self.uid) + '&currentPageNum=' + str(
            self.cpage) + '&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=099%23KAFEzYEpEBMEIETLEEEEE6twSXyqG6PTZXvID6PqS9lMD6NJDca4S6twDXy7n6gFN7FETcZdt9E9E7EFEE1CbOdTEEx6zIywTGFETrZtt3illW4TEHIT7svmi1A0DYAB6OT2qNXRZTzezSKrhmN7JxcGkL0BxYP05cfo3MD6%2BmN7VmGbkfMcma2O0HeqmGP05cfo3MD6%2BmN7VmGbkfMqma2O0HeqmGP0J7FE1cZdt2%2FJOj8XOGFETrWdt%2F97DpSTE1LP%2F3iSlllP%2FcZdd29lludgsyaAzlllsOaP%2F3hvlll%2FBrZdd09llutcgGFEZETebOpdCwUQrjDt9ynKbOMBcYe6PPXnHshnwBZtCypZHai3wXr1qzW28vdEVtq0vKr29ssC4a2SOa4Rxsn0vO10OstuV6Fo8euM%2FOs%2BZK%2BMhTzu3rnMh0GfKSwsVPc%2B8VI0lGwYAj82I0Os3rh48VI084p1doc2JTrx3%2FujzzI08%2BF1uuyiIxqf8GUlsMW2qLhol%2FuGSsI2qiRu3uwMh0YAqbwub6IA8LFi1bZtQLUVbRhqwR168puybwdEPQICq0CMldrnSgUAqzYl%2FuaX8wFCJ3sRPPx2q25TEE7EYRpC&_ksTS=1507305780613_2081&callback=jsonp_tbcrate_reviews_list'
        rql = "GET /feedRateList.htm?auctionNumId=" + str(self.pid) + "&userNumId=" + str(self.uid) + "&currentPageNum=" + str(self.cpage) + "&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=099%23KAFEzYEpEBMEIETLEEEEE6twSXyqG6PTZXvID6PqS9lMD6NJDca4S6twDXy7n6gFN7FETcZdt9E9E7EFEE1CbOdTEEx6zIywTGFETrZtt3illW4TEHIT7svmi1A0DYAB6OT2qNXRZTzezSKrhmN7JxcGkL0BxYP05cfo3MD6%2BmN7VmGbkfMcma2O0HeqmGP05cfo3MD6%2BmN7VmGbkfMqma2O0HeqmGP0J7FE1cZdt2%2FJOj8XOGFETrWdt%2F97DpSTE1LP%2F3iSlllP%2FcZdd29lludgsyaAzlllsOaP%2F3hvlll%2FBrZdd09llutcgGFEZETebOpdCwUQrjDt9ynKbOMBcYe6PPXnHshnwBZtCypZHai3wXr1qzW28vdEVtq0vKr29ssC4a2SOa4Rxsn0vO10OstuV6Fo8euM%2FOs%2BZK%2BMhTzu3rnMh0GfKSwsVPc%2B8VI0lGwYAj82I0Os3rh48VI084p1doc2JTrx3%2FujzzI08%2BF1uuyiIxqf8GUlsMW2qLhol%2FuGSsI2qiRu3uwMh0YAqbwub6IA8LFi1bZtQLUVbRhqwR168puybwdEPQICq0CMldrnSgUAqzYl%2FuaX8wFCJ3sRPPx2q25TEE7EYRpC&_ksTS=1507305780613_2081&callback=jsonp_tbcrate_reviews_list HTTP/1.1"
        if str(self.cpage) != '1':
            comrqurl = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' + str(self.pid) + '&userNumId=' + str(self.uid) + '&currentPageNum=' + str(
                self.cpage) + '&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hvu9vWvRhvUvCkvvvvvjiPP2SW6jiEPF5hsjljPmPwAjlhR2Fp0j3nPFMp6jtb9phv2nsG3VuSzYswMjpW7uwCvvBvpvpZ2QhvC26wT9yCvpvVphhvvvvvmphvLhPStpmFdcWKNB3rt8Trwo1%2BEbFCKdyIvjEb1RoXVznVayqyiCOyf3glBuV9eEB%2BEVgJlw66HjHOfvDrt8TJfx1%2Bju2WH3D%2BmB%2Bka4oivpvUphvhJcdHh6mEvpvVp6WUCEIfKphv8hCvvvvvvhCvphvWbpvvp%2BtvpCBXvvC2p6CvHHyvvh89phvWcpvvpuZtvpvhphvvvUwCvvBvppvvdphvmZCCoBpjvhCUMFyCvvBvpvvv&_ksTS=1507341442541_2042&callback=jsonp_tbcrate_reviews_list'
            rql = "GET /feedRateList.htm?auctionNumId=" + str(self.pid) + "&userNumId=" + str(self.uid) + "&currentPageNum=" + str(
                self.cpage) + "&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hvu9vWvRhvUvCkvvvvvjiPP2SW6jiEPF5hsjljPmPwAjlhR2Fp0j3nPFMp6jtb9phv2nsG3VuSzYswMjpW7uwCvvBvpvpZ2QhvC26wT9yCvpvVphhvvvvvmphvLhPStpmFdcWKNB3rt8Trwo1%2BEbFCKdyIvjEb1RoXVznVayqyiCOyf3glBuV9eEB%2BEVgJlw66HjHOfvDrt8TJfx1%2Bju2WH3D%2BmB%2Bka4oivpvUphvhJcdHh6mEvpvVp6WUCEIfKphv8hCvvvvvvhCvphvWbpvvp%2BtvpCBXvvC2p6CvHHyvvh89phvWcpvvpuZtvpvhphvvvUwCvvBvppvvdphvmZCCoBpjvhCUMFyCvvBvpvvv&_ksTS=1507341442541_2042&callback=jsonp_tbcrate_reviews_list HTTP/1.1"
        # headers = {
        #     "(Request-Line)": "GET /feedRateList.htm?auctionNumId=530438194280&currentPageNum=" + str(self.cpage) + " HTTP/1.1",
        #     "Host": "rate.taobao.com",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Cookie": "t=8966aee822149b85d84705559be96692; l=AhwcrF8lfNVVPJ1BWO4B/jd17DDOn8C/; isg=ApOTxsEyzmKEh4POrnyOKME3Ixd94CcD05-i_UWwYrLlxLJmzRk2W69WiA9U; cna=C0UYENE7MyECAXTgN0walRwa; miid=287202153718186299; _cc_=UIHiLt3xSw%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; um=A502B1276E6D5FEFDF7E79595098237104987D4008A97066941EB4050DD9C4321FA30A7834CA1148CD43AD3E795C914CEEBDF4280F46E5357CB83BB2EDE926A0; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; cookie2=6b5b70519904ab50b9fae8cdd56c24e0; _tb_token_=e33e1e9501ae3; mt=ci=0_0; v=0; uc1=cookie14=UoTcCDyQKMJjVg%3D%3D; linezing_session=K2FCVKxm5Q620oXou6RMtkmE_15073362011835NZs_1",
        #     "Connection": "keep-alive",
        #     "Upgrade-Insecure-Requests": "1",
        #     "Cache-Control": "max-age=0"
        # }
        # data = {
        #     'auctionNumId': int(self.pid),
        #     'currentPageNum': int(self.cpage)
        # }
        headers = {
            "(Request-Line)": rql,
            "Host": "rate.taobao.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": self.url,
            "Cookie": "t=8966aee822149b85d84705559be96692; l=AhwcrF8lfNVVPJ1BWO4B/jd17DDOn8C/; isg=AqeniFnmsmlsBDcS8tjirFVbN9uxhHsH50M2QXkUpzZdaMYqgf3eXlUu_FOI; cna=C0UYENE7MyECAXTgN0walRwa; miid=287202153718186299; tracknick=alanconstantine; _cc_=UIHiLt3xSw%3D%3D; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; um=A502B1276E6D5FEFDF7E79595098237104987D4008A97066941EB4050DD9C4321FA30A7834CA1148CD43AD3E795C914C0EC76D63C33688F634F93B26BF72B9EF; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; cookie2=6b5b70519904ab50b9fae8cdd56c24e0; v=0; _tb_token_=e33e1e9501ae3; uc1=cookie14=UoTcCDyVBv%2FbqQ%3D%3D",
            "Connection": "keep-alive"
        }
        data = {
            "auctionNumId": str(self.pid),
            "userNumId": str(self.uid),
            "currentPageNum": str(self.cpage),
            "pageSize": "20",
            "rateType": "",
            "orderType": "sort_weight",
            "attribute": "",
            "sku": "",
            "hasSku": "false",
            "folded": "0",
            "ua": "099#KAFEzYEpEBMEIETLEEEEE6twSXyqG6PTZXvID6PqS9lMD6NJDca4S6twDXy7n6gFN7FETcZdt9E9E7EFEE1CbOdTEEx6zIywTGFETrZtt3illW4TEHIT7svmi1A0DYAB6OT2qNXRZTzezSKrhmN7JxcGkL0BxYP05cfo3MD6+mN7VmGbkfMcma2O0HeqmGP05cfo3MD6+mN7VmGbkfMqma2O0HeqmGP0J7FE1cZdt2/JOj8XOGFETrWdt/97DpSTE1LP/3iSlllP/cZdd29lludgsyaAzlllsOaP/3hvlll/BrZdd09llutcgGFEZETebOpdCwUQrjDt9ynKbOMBcYe6PPXnHshnwBZtCypZHai3wXr1qzW28vdEVtq0vKr29ssC4a2SOa4Rxsn0vO10OstuV6Fo8euM/Os+ZK+MhTzu3rnMh0GfKSwsVPc+8VI0lGwYAj82I0Os3rh48VI084p1doc2JTrx3/ujzzI08+F1uuyiIxqf8GUlsMW2qLhol/uGSsI2qiRu3uwMh0YAqbwub6IA8LFi1bZtQLUVbRhqwR168puybwdEPQICq0CMldrnSgUAqzYl/uaX8wFCJ3sRPPx2q25TEE7EYRpC",
            "_ksTS": "1507305780613_2081",
            "callback": "jsonp_tbcrate_reviews_list"
        }
        return comrqurl, headers, data

    def rqCom(self):
        comrqurl, headers, data = self.tpBuildheader()
        print('requesting...')
        rc = requests.get(url=comrqurl, headers=headers, data=data, timeout=10)
        rcjson = json.loads((rc.text).replace(
            'jsonp_tbcrate_reviews_list', '').strip().strip('()'))
        curtotal = rcjson['total']
        maxpage = rcjson['maxPage']
        topcomments = rcjson['comments']
        for tcom in topcomments:
            usrinfo = tcom['user']
            username = usrinfo['nick']
            self.commentsdict[username] = tcom['content']
        return self.commentsdict, curtotal, maxpage, rcjson


class TaoBao:

    def __init__(self, url, page, uid):
        self.url = url
        self.page = page
        self.pid = 0
        self.uid = uid

    def getPid(self):
        # print
        getid = re.findall(r'id=[0-9]+', self.url)
        if len(getid) != 0:
            self.pid = getid[0].replace('&', '').replace(',', '').replace(
                'id', '').replace('=', '')
        # else:
        #     getid = re.findall(r'id=[0-9]+', self.url)

    # def getcoms(self, driver, page):
    #     comrqurl = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=' +
    #         str(self.pid) + '&currentPageNum=' + str(page)
    #     driver.get(comrqurl)
    #     # print(str(driver.page_source))
    #     rcjson = json.loads(str(driver.page_source).replace(
    #         '</body></html>', '').replace('<html><head></head><body>{', '').strip())
    #     p(rcjson)

    def tbparser(self, driver, soup, result):
        attlist = soup.find('ul', class_='attributes-list')
        attributes = []
        atli = attlist.find_all('li')
        for at in atli:
            attributes.append(at.get_text())
        detail = {}
        detail['details'] = attributes

        div_description = soup.find(
            'div', class_='J_DetailSection tshop-psm ke-post')
        if str(type(div_description)) != "<class 'NoneType'>":
            if div_description.get_text().strip() != '':
                detail['description'] = div_description.get_text().strip()
        result['basicdetail'] = detail

        get_comets = soup.find('em', class_='J_ReviewsCount')
        if str(type(get_comets)) == "<class 'NoneType'>":
            result['comments_num'] = '0'
            result['comments'] = 'no comments'
            return result
        else:
            result['comments_num'] = int(get_comets.get_text())
            commentsdict = {}
            # if result['comments_num']
            if result['comments_num'] > 20:

                commentsdict, curtotal, maxpage, rcjson = GetTBComments(commentsdict,
                                                                        self.url, self.pid, self.uid, 1).rqCom()
                # p(commentsdict)
                spt = random.uniform(30, 50)
                print("comment's page 1 done, sleep:%s..." %
                      round(spt, 4))
                time.sleep(spt)
                maxpage = int(maxpage)
                print('got %s comment pages.' % maxpage)

                for page in range(2, maxpage + 1):
                    commentsdict, curtotal, mp, rcjson = GetTBComments(commentsdict,
                                                                       self.url, self.pid, self.uid, page).rqCom()
                    spt = random.uniform(30, 50)
                    print("comment's page %s done, sleep:%s..." %
                          (page, round(spt, 4)))
                    time.sleep(spt)
                result['comments_num'] = str(result['comments_num'])
                result['comments'] = commentsdict
            else:
                commentsdict, curtotal, maxpage, rcjson = GetTBComments(commentsdict,
                                                                        self.url, self.pid, self.uid, 1).rqCom()
                print("comment's page 1 done...")
                result['comments_num'] = str(result['comments_num'])
                result['comments'] = commentsdict
                print(rcjson)
                # self.getcoms(driver, 1)
            if result['comments_num'] == '0':
                result['comments'] = 'no comments'
            return result

    def reqweb(self, result):
        driver = wb.Ie()
        # driver = wb.Chrome()
        # driver = wb.PhantomJS()
        driver.get(self.url)
        driver.set_window_size(0, 0)
        if len(re.findall(r'id=[0-9]+', self.url)) != 0:
            self.getPid()
        else:
            self.url = driver.current_url
            self.getPid()
        print(self.url[:60])
        print(self.pid)
        # self.getPid()
        if self.pid != 0:
            # result = {}
            try:
                driver.set_page_load_timeout(100)
            # driver.set_window_size(0, 0)
                pagecontent = driver.page_source
                soup = BeautifulSoup(pagecontent, "html.parser")

                result = self.tbparser(driver, soup, result)
                driver.close()
            except Exception as e:
                print(e)
                with open(r'errorlist.txt', 'a', encoding='utf8') as f:
                    f.write(str(result['url']) + '\t' + str(e) + '\n')
                driver.quit()
                time.sleep(120)
                pass
            return result
        else:
            driver.quit()
            print('no pid')
            with open(r'errorlist.txt', 'a', encoding='utf8') as f:
                f.write(str(result['url']) + '\t' + 'no pid' + '\n')
            return result
            pass


class Tmall:

    def __init__(self, url):
        self, url = url

    def buildheader(self):
        pass


def main():
    # url = 'https://click.simba.taobao.com/cc_im?p=%B5%E7%C0%C2%CF%DF&s=878109219&k=525&e=mt5HIluviEdllIXfrF%2BhICB6uWSHNdgzBd5ypZDHPxAwUkFqIgSsG2sgcdeuLmC2x2J1rXa%2FZbwtJgo95rAhWycQXdibhWstmfD3a45ZzPaAMiyPD42ffxOtw77WghKuATKWItUKSmt3%2FK%2Bzfb0Gg3m83X5ilU8L4jhklu8XGDQ7De69lgcXrzdxP38rIXr3Gk01d%2BpeD9w13%2FzK%2B9kOs11BePoDhy9vieeO0sd0B8JZTbIjHg3QeaC7qj1%2BhZ3%2BdAsWAsPJwpVZ4xC9IFb82A0sNGVLHXWFGutVwf5q%2FPbtyMNTwNHSed7EcPqXTol3lvsfSdV8xiXLURkmjhqkNpcnyMQ9k2oTIex3oWVEEpIFDQiH%2BPgpPFKilgRMlgpXpFgE0GpDtU2Bq11nkg2Tsg4oDxVNGAyr0QZo6c8I4U4S9auKbjORcILEkIrIL8O4Dmj3%2FijmS7UTRkCUXBcBPHSR0tBVKg74GADPXMMkuO%2BsBrF3XGywWHQ5gdsqm8uefOdJzWAK1ks%3D#detail'
    # # 644965041
    # # url = 'https:' + '//item.taobao.com/item.htm?id=556906684839&ns=1&abbucket=19#detail'
    # # 105795562

    # tb = TaoBao(url=url, page=2, uid='644965041').reqweb()
    id = len(Wiresdetails.select())
    data = Wires.select()
    print(len(data))
    for datum in data[1501:1901]:
        if '//detail.tmall.com' in datum.url:
            continue
        result = {}
        id += 1
        url = datum.url
        if 'https:' not in datum.url:
            url = 'https:' + datum.url
        result['url'] = url
        result['page'] = datum.page
        result['title'] = datum.title
        result['price'] = datum.price
        result['user_id'] = str(datum.user_id)
        slpt = random.uniform(5, 10)
        print('No:%s, Page:%s, url:%s, sleep:%s' %
              (id, result['page'], (result['url'])[:50], round(slpt, 4)))
        print((result['title'])[:50])
        result = TaoBao(url=result['url'], page=result['page'],
                        uid=result['user_id']).reqweb(result)
        if len(result) == 5:
            with open(r'errorlist.txt', 'a', encoding='utf8') as f:
                f.write(str(result['url']) + '\t' + 'no detail' + '\n')
            time.sleep(slpt)
            continue
        else:
            Wiresdetails.create(**result)
            print('sleep 30s...')
            time.sleep(25)


if __name__ == '__main__':
    ts = dt.now()
    main()
    te = dt.now()
    tdif = te - ts
    print('[%s]' % tdif)
