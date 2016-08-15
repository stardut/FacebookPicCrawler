#Python Crawler Facebook

##Function

Crawl the [Facebook](https://www.facebook.com) user's public picture

##Setting

If you want to run the cralwer.Follew the setting and you can run the program

 * Install [Python2.7](https://www.python.org/)
 * Install lib [requests](http://docs.python-requests.org/en/master/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 * Set your facebook username and password:
 
	 ```python
		USER = [
      {
        'email' : 'xxxxxxxxxx',
        'pass' : 'xxxxxxx'
      },
    ]

	 ```
  or use mulitple account:

  ```python
    USER = [
      {
        'email' : 'xxxxxxxxxx',
        'pass' : 'xxxxxxx'
      },
      {
        'email' : 'xxxxxxxxxx',
        'pass' : 'xxxxxxx'
      },
      {
        'email' : 'xxxxxxxxx',
        'pass' : 'xxxxxxxx'
      },
    ]

  ```

 * Set save path in your computer:
 
	```python
		DOWNLOAD_PATH = 'picture save path in your computer'
	```

##Run

  `python main.py`

##Crawl Strategy

  * From user id equel `100010625445795` start and every times minus 1
  * Useing thread improve work efficiency
 
##Trouble
  * It's hard to analysis Facebook's html page structure.
  * Many data use Ajax.

##Exist problem(Bug?)
  * Some user crawl fail and I don't kown why.(玄学)

##Star
If you like the crawler or it can help you,give me a star.<br>
Thank you.