#Python Crawler Facebook

##Function

Crawl the [Facebook](https://www.facebook.com) user's public picture

##Setting

If you want to run the cralwer.Follew the setting and you can run the program

 * Install lib [requests](http://docs.python-requests.org/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 * Set your facebook username and password(line 16 and 17)
	 ```python
		USER_ACCOUNT = 'your login username'
		USER_PASSWORD = 'your login password'
		DOWNLOAD_PATH = 'picture save path in your computer'
	 ```
 * Set save path in your computer(line 18)
	```
		DOWNLOAD_PATH = 'picture save path in your computer'
	```

##Crawl Strategy

  * From user id equel 100010625445795 start and every times minus 1
  * Useing thread improve work efficiency
 
##Trouble
  * It's hard to analysis Facebook's html page structure.
  * Many data use Ajax.

##Exist problem(Bug?)
  * Some user crawl fail and I don't kown why.(玄学)

##Star
If you like the crawler or it can help you,give me a star.<br>
Thank you.