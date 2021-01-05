# EbayScrapper

Proxy runner works as follows:
-1 Initialise the proxy runner with a list opf proxies to use, a scraping function, a url to be scraped  
-2 the proxy runner will then start scraping the url webpage with the provided function every 15min
-3 if any of the requests fails then the proxy runner tries the again with a different proxy
-4 Once the list of proxies is expended the proxy runner will exit