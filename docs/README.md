# EbayScrapper

Proxy runner works as follows:
1. Initialise the proxy runner with a list opf proxies to use, a scraping function, a url to be scraped  
2. the proxy runner will then start scraping the url webpage with the provided function every 15min
3. if any of the requests fails then the proxy runner tries the again with a different proxy
4. Once the list of proxies is expended the proxy runner will exit

As well as proxy rotation we will also need to consider UserAgent rotation. UserAgent tells the website what type of browser,os etc that the request came from. In the case of python request it'll look something like:

{'headers': {'Accept': '*/*',
             'Accept-Encoding': 'gzip, deflate',
             'Host': 'httpbin.org',
             'User-Agent': 'python-requests/2.23.0',
             'X-Amzn-Trace-Id': 'Root=1-5ee7a417-97501ac8e10eb62866e09b9c'}}
             
This immediately suggests to ebay that we're scraping so we may want to rotate this to prevent the proxy requests being blocked earlier than needs be.

https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
