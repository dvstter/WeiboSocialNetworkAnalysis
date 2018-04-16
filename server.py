from bs4 import BeautifulSoup
import requests
import re
import urllib3
import time
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIE = "ALF=1526464649; SUB=_2A2530APZDeRhGeNL41IW9ivEwz-IHXVVOq2RrDV8PUJbkNANLWPakW1NSMu2liOurCegJQMIKsMmoT_A6cpoWPu1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V3jnHpzZ7.JaoXWzWPRC05JpX5oz75NHD95QfSKn7S0qf1hn0Ws4Dqcjci--fi-zRiKn0i--ciKLhiK.Ni--4iKnpiKnNi--Xi-zRiKyWi--ciKnfiK.fi--ciK.ci-8s; _s_tentry=-; Apache=6577064438761.935.1523875261930; SINAGLOBAL=6577064438761.935.1523875261930; ULV=1523875262029:1:1:1:6577064438761.935.1523875261930:; _T_WM=6627dda88e1190d79146f6451d440ea8; YF-Ugrow-G0=9642b0b34b4c0d569ed7a372f8823a8e; wvr=6; YF-V5-G0=9717632f62066ddd544bf04f733ad50a; YF-Page-G0=0acee381afd48776ab7a56bd67c2e7ac"
URL = "https://weibo.com/p/1006062968634427/follow?page="
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"

def request_data(url, payload=None):
    headers = {"user-agent":USER_AGENT, "cookie":COOKIE}
    resp = requests.get(url, params=payload, headers=headers, verify=False)
    bs = BeautifulSoup(resp.text, "lxml")
    return resp, bs

def debug(resp, filename=None):
    if filename is None:
        filename = "debug.txt"

    f = open(filename, "w", encoding="utf-8")

    f.write(resp.text)
    f.close()


if __name__ == "__main__":
    ids = []
    names = []
    attentions = []
    fans = []
    blogs = []

    for x in range(1, 6):
        resp, bs = request_data(URL + str(x))
        debug(resp, "debug-"+str(x)+".txt")

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

    print("num of ids: " + str(len(ids)))
    print("num of names: " + str(len(names)))
    print("num of attentions: " + str(len(attentions)))
    print("num of fans: " + str(len(fans)))
    print("num of blogs: " + str(len(blogs)))

    f = open("result.txt", "w", encoding="utf-8")
    for x in range(len(ids)):
        f.write("{}\t{}\t{}\t{}\t{}\n".format(ids[x], names[x], attentions[x], fans[x], blogs[x]))
