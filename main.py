from ProxyRunner import proxy_runner
from ScrapeFuncs import get_proxies,get_listings
import sys

if __name__=='__main__':

    #sys.stdout = open('./Data/logs/logs.txt', 'w')

    proxies = get_proxies()

    runner = proxy_runner(proxies=proxies,
        url="https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=warhammer&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=warhammer+40k",
        scraper=get_listings)

    # runner = proxy_runner(proxies=proxies,
    #     url="https://www.google.com",
    #     scraper=get_listings)
    
    runner.run()

    #sys.stdout.close()