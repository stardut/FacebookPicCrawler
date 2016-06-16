#Python爬虫
------ 

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

* 因为之前一直在爬id，我将爬图片的代码注释掉了，取消掉注释就可以了，一共两处，我已经标记出来了
* 现在还存在的问题一： 还是存入数据库的编码问题
* 问题二：会出现 Max retries exceeded问题，不知道是ip代理（我购买的付费ip）的问题还是程序（不用代理的时候正常）的问题（也许是用代理的方法出错？）有时候会成功，应该是代理ip的问题
* 如果不使用代理，访问频率稍高就会被限制

Thanks！

