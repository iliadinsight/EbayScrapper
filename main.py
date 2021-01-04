from ProxyRunner import proxy_runner
from ScrapeFuncs import get_proxies,ScrapeNewListing


if __name__=='__main__':

    proxies = get_proxies()

    runner = proxy_runner(proxies=proxies,
        url="https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=warhammer&_sacat=0&LH_BIN=1",
        scraper=ScrapeNewListing)

    runner.run()