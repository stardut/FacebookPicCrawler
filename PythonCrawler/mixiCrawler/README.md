#Python Crawler Mixi

##Funtion

Crawl the [mixi](https://www.facebook.com) 's(Japanese social network site)user public picture.

##Crawl Strategy

  * From user id equel 1 start and every times plus 1
  * Useing thread improve work efficiency
 
##Trouble
The site have access restriction and stringent visit times.
(该网站的抓取效率非常的感人)

##Database Setting

Before start you need create a database and a table.

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

##Exist problem

1. The database's encode have some error when use Chinese
3. When runing the program you need use proxy IP,otherwise the speed will very slow. 

