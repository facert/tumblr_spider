# tumblr_spider
汤不热 python 多线程爬虫

#### install
> pip install -r requirements.txt


#### run
> python tumblr.py username (usename 为任意一个热门博主的 usename)

## snapshoot
![](https://raw.githubusercontent.com/facert/tumblr_spider/master/snapshoots/results.png)


#### 爬取结果
> `user.txt` 是爬取的博主用户名结果， `source.txt` 是视频地址集

#### 原理
> 根据一个热门博主的 usename, 脚本自动会获取博主转过文章的其他博主的 username，并放入爬取队列中，递归爬取。

#### 申明
> 这是一个正经的爬虫（严肃脸），爬取的资源跟你第一个填入的 username 有很大关系，另外由于某些原因，导致 tumblr 被墙，所以最简单的方式就是用国外 vps 去跑。
