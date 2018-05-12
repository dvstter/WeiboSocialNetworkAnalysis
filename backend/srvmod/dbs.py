#-*- coding:utf-8 -*-
import redis

class Database:
    Pool = None
    Init = False

    def __init__(self, host="127.0.0.1", port=6379):
        if not type(self).Init:
            try:
                type(self).Pool = redis.BlockingConnectionPool(host=host, port=port)
                type(self).Init = True
            except redis.exceptions.ConnectionError as _:
                print("Exception: Cannot create connection pool, please check database address and port.")
                type(self).Init = False
        try:
            self.conn = redis.StrictRedis(connection_pool=type(self).Pool)
        except redis.exceptions.ConnectionError:
            print("Exception: Too many connection request, cannot get the connection.")
            self.conn = None

    """
    添加、获取所有的微博id
    
    :param weibo_id: 微博的id
    """
    def add_weibo_id(self, weibo_id):
        return self.__common_add("weiboids", weibo_id)

    def get_weibo_ids(self):
        return self.__common_fetch_all("weiboids")

    """
    添加转发、评论、点亮的昵称
    
    :param weibo_id: 微博的id
    :param name: 添加的昵称
    """
    def add_repost_name(self, weibo_id, name):
        return self.__common_add("repost:"+str(weibo_id), name)

    def add_comment_name(self, weibo_id, name):
        return self.__common_add("comment:"+str(weibo_id), name)

    def add_star_name(self, weibo_id, name):
        return self.__common_add("star:"+str(weibo_id), name)

    """
    获取转发、评论、点亮的所有昵称
    
    :param weibo_id: 微博的id
    """
    def get_repost_names(self, weibo_id):
        return self.__common_fetch_all("repost:" + str(weibo_id))

    def get_comment_names(self, weibo_id):
        return self.__common_fetch_all("comment:" + str(weibo_id))

    def get_star_names(self, weibo_id):
        return self.__common_fetch_all("star:" + str(weibo_id))

    """
    获取转发、评论、点亮的所有微博id
    """
    def get_all_repost_ids(self):
        return self.__common_keys("repost:*")

    def get_all_comment_ids(self):
        return self.__common_keys("comment:*")

    def get_all_star_ids(self):
        return self.__common_keys("star:*")

    """
    添加关注的人的信息
    
    :param person_id: 用户的id
    :param name/attentions/fans/blogs: 用户的昵称、关注数、粉丝数、博客数
    """
    def add_name(self, person_id, name):
        return self.__common_set("name:"+str(person_id), name)

    def add_attentions(self, person_id, attentions):
        return self.__common_set("attentions:"+str(person_id), str(attentions))

    def add_fans(self, person_id, fans):
        return self.__common_set("fans:"+str(person_id), str(fans))

    def add_blogs(self, person_id, blogs):
        return self.__common_set("blogs:"+str(person_id), str(blogs))

    """
    获取关注的人的信息

    :param person_id: 用户的id
    :param name/attentions/fans/blogs: 用户的昵称、关注数、粉丝数、博客数
    """
    def get_name(self, person_id):
        return self.__common_get("name:"+str(person_id))

    def get_attentions(self, person_id):
        return int(self.__common_get("attentions:"+str(person_id)))

    def get_fans(self, person_id):
        return int(self.__common_get("fans:"+str(person_id)))

    def get_blogs(self, person_id):
        return int(self.__common_get("blogs:"+str(person_id)))

    """
    计算、获取关注的人的转发、评论、点亮率
    """
    def process_ratios(self):
        # get all the data needed
        reposts = {}
        comments = {}
        stars = {}
        users = {}

        r_ratio = {}
        c_ratio = {}
        s_ratio = {}

        for rid in self.get_all_repost_ids():
            rnames = self.get_repost_names(rid)
            reposts[rid] = rnames

        for cid in self.get_all_comment_ids():
            cnames = self.get_comment_names(cid)
            comments[cid] = cnames

        for sid in self.get_all_star_ids():
            snames = self.get_star_names(sid)
            stars[sid] = snames

        for uid in self.get_all_user_ids():
            uname = self.get_name(uid)
            users[uid] = uname

        # process the data
        for uid, uname in users.items():
            r_ratio[uid] = 0
            for _, rnames in reposts.items():
                if uname in rnames:
                    r_ratio[uid] += 1

            s_ratio[uid] = 0
            for _, snames in stars.items():
                if uname in snames:
                    s_ratio[uid] += 1

            c_ratio[uid] = 0
            for _, cnames in comments.items():
                if uname in cnames:
                    c_ratio[uid] += 1

        for p, cnt in r_ratio.items():
            r_ratio[p] = float(float(cnt) / len(reposts))
        for p, cnt in s_ratio.items():
            s_ratio[p] = float(float(cnt) / len(stars))
        for p, cnt in c_ratio.items():
            c_ratio[p] = float(float(cnt) / len(comments))

        # write to the database
        for p, r in r_ratio.items():
            self.__common_set("rratio:"+p, r)
        for p, r in s_ratio.items():
            self.__common_set("sratio:"+p, r)
        for p, r in c_ratio.items():
            self.__common_set("cratio:"+p, r)

    def get_star_ratio(self, person_id):
        return self.__common_get("sratio:"+person_id)

    def get_comment_ratio(self, person_id):
        return self.__common_get("cratio:"+person_id)

    def get_repost_ratio(self, person_id):
        return self.__common_get("rratio:"+person_id)

    """
    获取所有关注的人的id
    """
    def get_all_user_ids(self):
        return self.__common_keys("name:*")

    """
    保存、读取所有微博的信息
    
    :param filename: 文件名
    """
    def save_blogs_info(self, filename="resource/blogs.txt"):
        file = open(filename, "w", encoding="utf-8")
        for each_id in self.get_all_comment_ids():
            for each_name in self.get_comment_names(each_id):
                file.write("comment:{}&{}\n".format(each_id, each_name))

        for each_id in self.get_all_repost_ids():
            for each_name in self.get_repost_names(each_id):
                file.write("repost:{}&{}\n".format(each_id, each_name))

        for each_id in self.get_all_star_ids():
            for each_name in self.get_star_names(each_id):
                file.write("star:{}&{}\n".format(each_id, each_name))

        file.close()

    def restore_blogs_info(self, filename="resource/blogs.txt"):
        file = open(filename, "r", encoding="utf-8")
        for eachline in file.readlines():
            if ":" not in eachline:
                continue

            key, value = eachline.strip("\n").split("&")
            self.__common_add(key, value)

        file.close()

    """
        保存、读取所有关注用户的信息

        :param filename: 文件名
    """
    def save_users_info(self, filename="resource/users.txt"):
        file = open(filename, "w", encoding="utf-8")
        for each_id in self.get_all_user_ids():
            name = self.get_name(each_id)
            attentions = self.get_attentions(each_id)
            blogs = self.get_blogs(each_id)
            fans = self.get_fans(each_id)

            file.write("{}&{}&{}&{}&{}\n".format(each_id, name, attentions, blogs, fans))

        file.close()

    def restore_users_info(self, filename="resource/users.txt"):
        file = open(filename, "r", encoding="utf-8")
        for eachline in file.readlines():
            if "&" not in eachline:
                continue

            id_, name, attentions, blogs, fans = eachline.strip("\n").split("&")
            self.add_name(id_, name)
            self.add_attentions(id_, attentions)
            self.add_blogs(id_, blogs)
            self.add_fans(id_, fans)

        file.close()

    """
        保存、读取所有微博的id信息

        :param filename: 文件名
    """
    def save_blog_ids(self, filename="resource/blog_ids.txt"):
        file = open(filename, "w", encoding="utf-8")
        for each in self.get_weibo_ids():
            file.write("{}\n".format(each))
        file.close()

    def restore_blog_ids(self, filename="resource/blog_ids.txt"):
        file = open(filename, "r", encoding="utf-8")
        for eachline in file.readlines():
            id_ = eachline.strip("\n")
            if len(id_) < 2:
                continue
            self.add_weibo_id(eachline.strip("\n"))
        file.close()


    def __common_set(self, key, value):
        if not self.conn:
            return False

        self.conn.set(key, value)
        return True

    def __common_get(self, key):
        if not self.conn:
            return None

        return self.conn.get(key).decode("utf-8")

    def __common_add(self, key, value):
        if not self.conn:
            return False

        self.conn.rpush(key, value)
        return True

    def __common_fetch_all(self, key):
        if not self.conn:
            return None

        return [x.decode("utf-8") for x in self.conn.lrange(key, 0, -1)]

    def __common_keys(self, pattern):
        if not self.conn:
            return None

        return [x.split(":")[1] for x in [x.decode("ascii") for x in self.conn.keys(pattern)]]