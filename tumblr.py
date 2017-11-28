# -*- coding:utf-8 -*-
import signal
import sys
import requests
import threading
import queue
import time
from bs4 import BeautifulSoup

mutex = threading.Lock()
is_exit = False


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
                print (u'新增链接:' + source)

        tmp_user = []
        new_users = soup.find_all(class_='reblog-link')
        for user in new_users:
            username = user.text.strip()
            if username and username not in self.total_user:
                self.user_queue.put(username)
                self.total_user.append(username)
                tmp_user.append(username)
                print (u'新增用户:' + username)

        mutex.acquire()
        if tmp_user:
            self.f_user.write('\n'.join(tmp_user)+'\n')
        if tmp_source:
            self.f_source.write('\n'.join(tmp_source)+'\n')
        mutex.release()

    def run(self):
        global is_exit
        while not is_exit:
            user = self.user_queue.get()
            url = 'http://%s.tumblr.com/' % user
            self.download(url)
            time.sleep(2)
        self.f_user.close()
        self.f_source.close()


def handler(signum, frame):
    global is_exit
    is_exit = True
    print ("receive a signal %d, is_exit = %d" % (signum, is_exit))
    sys.exit(0)


def main():

    if len(sys.argv) < 2:
        print ('usage: python tumblr.py username')
        sys.exit()
    username = sys.argv[1]

    NUM_WORKERS = 10
    q = queue.Queue()
    # 修改这里的 username
    q.put(username)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    threads = []
    for i in range(NUM_WORKERS):
        tumblr = Tumblr(q)
        tumblr.setDaemon(True)
        tumblr.start()
        threads.append(tumblr)

    while True:
        for i in threads:
            if not i.isAlive():
                break
        time.sleep(1)


if __name__ == '__main__':
    main()
