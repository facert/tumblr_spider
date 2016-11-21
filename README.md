# tumblr_spider
汤不热 python 多线程爬虫

#### install
> pip install -r requirements.txt


#### run
> 修改 queue.put(`username`) 的 usename 为你喜欢的一个热门博主的 usename

> python tumblr.py


#### result
> `user.txt` 是爬取的博主用户名， `source.txt` 是视频地址集

## snapshoot
![](https://raw.githubusercontent.com/facert/tumblr_spider/master/snapshoots/results.png)

#### 原理
> queue.put(`username`), 填上你喜欢的一个热门博主的 usename, 脚本自动会获取博主转过文章的其他博主的 username，并放入爬取队列中。

#### 申明
> 这是一个正经的爬虫（严肃脸），爬取的资源跟你第一个填入的 username 有很大关系，另外由于某些原因，导致 tumblr 被墙，所以最简单的方式就是用国外 vps 去跑。
