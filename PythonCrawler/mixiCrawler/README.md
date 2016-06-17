#Python爬虫/Python Crawler
---
---
##爬虫功能

爬取日本社交网站[mixi.jp](www.mixi.jp)的用户公开相册的照片

---
##爬虫爬行策略

 > * 从用户 id=1 开始依次抓取数据，并根据拿到的数据判断是否为公开相册。
 > * 利用多线程和代理ip实现爬行效率的提升
 
---
##遇到的问题
该网站对于同意ip在一段时间内对网站访问的次数有非常严格的限制，导致抓取数据的速度非常慢。同时，自己买的代理ip稳定性非常的差，会错过很多数据，因此，该网站的图片抓取效率非常的感人。

---
##数据库设置

运行之前要新建一个mysql的数据库，然后新建一个test的表, 在main中填入数据库各个参数 user，password，localhost

```sql
create table test(
	id char(8) not null,
	sex char(8),
	name char(30),
	address char(50),
	birthday char(20),
	birthplace char(50),
	age char(15),
	album smallint,
	photo smallint,
	primary key (id)
);
```
---
##存在的问题

1. 数据库编码问题
2. 会出现 Max retries exceeded问题，不知道是ip代理（我购买的付费ip）的问题还是程序（不用代理的时候正常）的问题（也许是用代理的方法出错？）有时候会成功，应该是代理ip的问题
3. 如果不使用代理，访问频率稍高就会被限制

