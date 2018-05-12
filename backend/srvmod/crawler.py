# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
from backend.srvmod.dbs import Database
import re
import urllib3
import time
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

class Crawler:
    Cookie = {"yhl":"ALF=1526464649; SUB=_2A2530APZDeRhGeNL41IW9ivEwz-IHXVVOq2RrDV8PUJbkNANLWPakW1NSMu2liOurCegJQMIKsMmoT_A6cpoWPu1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V3jnHpzZ7.JaoXWzWPRC05JpX5oz75NHD95QfSKn7S0qf1hn0Ws4Dqcjci--fi-zRiKn0i--ciKLhiK.Ni--4iKnpiKnNi--Xi-zRiKyWi--ciKnfiK.fi--ciK.ci-8s; _s_tentry=-; Apache=6577064438761.935.1523875261930; SINAGLOBAL=6577064438761.935.1523875261930; ULV=1523875262029:1:1:1:6577064438761.935.1523875261930:; _T_WM=6627dda88e1190d79146f6451d440ea8; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; wvr=6; YF-V5-G0=9717632f62066ddd544bf04f733ad50a; YF-Page-G0=0acee381afd48776ab7a56bd67c2e7ac",
              "yyz":"_T_WM=e64e798330efa851d765145cd3c315ea; SUB=_2A2539gmaDeRhGeVM41EZ9CbKzzmIHXVVGJfSrDV6PUJbkdAKLVHCkW1NTPWVTIs_HQx28DCZ_P3i3TB_6uaAzwbG; SUHB=0pHBR6DEgbvh-n; SCF=AuECFNbCuS3Iv7iNbzNghcyzUFwHUZntezQy3yz6yQgMlZI95KuXirF2mtOWCcVXAvTbwgCvsEALKT3Tnbm2y8o.; SSOLoginState=1525840330"}
    UA = {"normal":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
          "wap":"Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
    Headers = {"user-agent":UA["wap"],
               "cookie":Cookie["yyz"],
               "accept-language":"en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
               "accept-encoding":"gzip, deflate, br",
               "cache-control":"no-cache",
               "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "host":"weibo.cn"}

    @staticmethod
    def get_followers():
        url = "https://weibo.com/p/1006062968634427/follow?page="

        ids = []
        names = []
        attentions = []
        fans = []
        blogs = []

        for x in range(1, 6):
            resp, bs = Crawler.request_data(url + str(x))

            for each in re.findall(r"info_name.*?<\\/div>", resp.text):
                if "usercard" in each:
                    ids += [re.findall(r"id=([0-9]+)", each)[0]]
                    names += [re.findall(r"refer_flag=[0-9]+_\\\" >(.*?)<\\/a>\\r\\n\\t\\t", each)[0]]

            for allinfo in re.findall(r"info_connect.*?<\\/div>", resp.text):
                tmp = re.findall(r'>([0-9]+?)<', allinfo)
                if len(tmp) == 0:
                    continue

                attentions += [tmp[0]]
                fans += [tmp[1]]
                blogs += [tmp[2]]

            time.sleep(random.randint(5, 10))

        f = open("result.txt", "w", encoding="utf-8")
        for x in range(len(ids)):
            f.write("{}\t{}\t{}\t{}\t{}\n".format(ids[x], names[x], attentions[x], fans[x], blogs[x]))

    @staticmethod
    def get_weibo_ids():
        dbs = Database()
        url = "https://weibo.cn/smartisan"
        for page_cnt in range(1, 150):
            print("------------------------------")
            print("Start fetching page: {}".format(page_cnt))
            Crawler.__parse_weibo_ids(url, dbs, page_cnt)
            slp_tm = random.randint(15, 120)
            print("Will sleep for {} secs".format(slp_tm))
            time.sleep(slp_tm)

    @staticmethod
    def __parse_weibo_ids(base_url, dbs, cur_page):
        if cur_page == 1:
            url = base_url
        else:
            url = "{}?page={}".format(base_url, cur_page)

        resp, bs = Crawler.request_data(url)
        for each in bs.find_all("a"):
            if "转发" in each.text and "原文" not in each.text:
                id_ = re.findall(r"https://weibo\.cn/repost/(\w+)\?", each["href"])[0]
                dbs.add_weibo_id(id_)
                print("Added weibo id: {}".format(id_))


    @staticmethod
    def get_repost_list():
        dbs = Database()
        weibo_ids = dbs.get_weibo_ids()
        for each in weibo_ids:
            url = "https://weibo.cn/repost/{}?uid=2968634427".format(each)
            cur_page = 1
            while True:
                print("------------------------------")
                print("Start fetching {} page: {}".format(each, cur_page))
                if not Crawler.__parse_repost_list(url, each, dbs, cur_page):
                    print("Move to the next target")
                    break
                cur_page += 1
                slp_tm = random.randint(15, 120)
                print("Sleep for {} secs to next page".format(slp_tm))
                time.sleep(slp_tm)

    @staticmethod
    def __parse_repost_list(base_url, weibo_id, dbs, cur_page):
        if cur_page == 1:
            url = base_url
        else:
            url = "{}&&page={}".format(base_url, cur_page)

        resp, bs = Crawler.request_data(url)
        for each in bs.find_all("div", class_="c"):
            if not each.find_all("span", class_="cc"):
                continue
            dbs.add_repost_name(weibo_id, each.a.text)
            print("Added {} to {}'s repost list".format(each.a.text, weibo_id))

        np_div = bs.find_all("div", class_="pa")
        if np_div:
            np_div = np_div[0]
            if "上页" in np_div.form.div.a.text:
                return False # has reached the last page
            else:
                return True
        else:
            return False

    @staticmethod
    def get_star_list():
        dbs = Database()
        weibo_ids = dbs.get_weibo_ids()
        for each in weibo_ids:
            url = "https://weibo.cn/attitude/{}?".format(each)
            cur_page = 1
            while True:
                print("------------------------------")
                print("Start fetching {} page: {}".format(each, cur_page))
                if not Crawler.__parse_star_list(url, each, dbs, cur_page):
                    print("Move to the next target")
                    break
                cur_page += 1
                slp_tm = random.randint(15,90)
                print("Sleep for {} secs to next page".format(slp_tm))
                time.sleep(slp_tm)

    @staticmethod
    def __parse_star_list(base_url, weibo_id, dbs, cur_page):
        if cur_page == 1:
            url = base_url
        else:
            url = "{}&page={}".format(base_url, cur_page)

        resp, bs = Crawler.request_data(url)
        for each in bs.find_all("div", class_="c"):
            if not each.find_all("span", class_="ct"):
                continue
            dbs.add_star_name(weibo_id, each.a.text)
            print("Added {} to {}'s star list".format(each.a.text, weibo_id))

        np_div = bs.find_all("div", class_="pa")
        if np_div:
            np_div = np_div[0]
            if "上页" in np_div.form.div.a.text:
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def get_comment_list():
        dbs = Database()
        weibo_ids = dbs.get_weibo_ids()
        for each in weibo_ids:
            url = "https://weibo.cn/comment/{}?".format(each)
            cur_page = 1
            while True:
                print("------------------------------")
                print("Start fetching {} page: {}".format(each, cur_page))
                if not Crawler.__parse_comment_list(url, each, dbs, cur_page):
                    print("Move to the next target")
                    break
                cur_page += 1
                slp_tm = random.randint(15, 120)
                print("Sleep for {} secs to next page".format(slp_tm))
                time.sleep(slp_tm)

    @staticmethod
    def __parse_comment_list(base_url, weibo_id, dbs, cur_page):
        if cur_page == 1:
            url = base_url
        else:
            url = "{}&page={}".format(base_url, cur_page)

        resp, bs = Crawler.request_data(url)
        for each in bs.find_all("div", class_="c"):
            if not each.find_all("span", class_="cc"):
                continue

            dbs.add_comment_name(weibo_id, each.find_all("a")[0].text)
            print("Added {} to {}'s comment list".format(each.a.text, weibo_id))

        np_div = bs.find_all("div", class_="pa")
        if np_div:
            np_div = np_div[0]
            if "上页" in np_div.form.div.a.text:
                return False  # has reached the last page
            else:
                return True
        else:
            return False

    @staticmethod
    def request_data(url, payload=None):
        resp = requests.get(url, params=payload, headers=Crawler.Headers, verify=False)
        bs = BeautifulSoup(resp.text, "lxml")
        return resp, bs

    @staticmethod
    def debug(resp, filename=None):
        if filename is None:
            filename = "debug.txt"

        f = open(filename, "w", encoding="utf-8")

        f.write(resp.text)
        f.close()