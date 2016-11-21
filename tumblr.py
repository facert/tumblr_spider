# -*- coding:utf-8 -*-

import requests
import threading
import Queue
import time
from bs4 import BeautifulSoup

mutex = threading.Lock()


class Tumblr(threading.Thread):

    def __init__(self, queue):
        self.user_queue = queue
        self.total_user = []
        self.total_url = []

        self.f_user = open('user.txt', 'a+')
        self.f_source = open('source.txt', 'a+')

        threading.Thread.__init__(self)

    def download(self, url):
        res = requests.get(url)

        source_list = []
        soup = BeautifulSoup(res.text)
        iframes = soup.find_all('iframe')
        tmp_source = []
        for i in iframes:
            source = i.get('src', '').strip()
            if source and source.find('https://www.tumblr.com/video') != -1 and source not in self.total_url:
                source_list.append(source)
                tmp_source.append(source)
                print u'新增链接:' + source

        tmp_user = []
        new_users = soup.find_all(class_='reblog-link')
        for user in new_users:
            username = user.text.strip()
            if username and username not in self.total_user:
                self.user_queue.put(username)
                self.total_user.append(username)
                tmp_user.append(username)
                print u'新增用户:' + username

        mutex.acquire()
        self.f_user.write('\n'.join(tmp_user)+'\n')
        self.f_source.write('\n'.join(tmp_source)+'\n')
        mutex.release()

    def run(self):
        while True:
            user = self.user_queue.get()
            url = 'http://%s.tumblr.com/' % user
            self.download(url)
            time.sleep(2)


def main():
    NUM_WORKERS = 100
    queue = Queue.Queue()
    queue.put('darevilhk')

    for i in range(NUM_WORKERS):
        tumblr = Tumblr(queue)
        tumblr.start()
    for i in range(NUM_WORKERS):
        tumblr.join()


if __name__ == '__main__':
    main()
