import requests,sys
from bs4 import BeautifulSoup
from datetime import datetime
import time

class proxy_runner:
    
    def __init__(self,proxies,url,scraper):
        self.proxies = (proxy for proxy in proxies)
        self.proxy = next(self.proxies)
        self.url = url
        self.scraper = scraper
        self.exectime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        
    def next_proxy(self):
        ''' Fetch the next proxy. Once empty raise an Exeption to end the process.'''
        try:
            next_proxy = next(self.proxies)
            self.proxy = next_proxy
        
        except:
            self.proxy = None
    
    def make_request(self,**kwargs):
        ''' Make a Request. If unsuccesful try the next proxy.'''

        if self.proxy!=None:
            try:
                response = requests.request(**kwargs)
                return response

            except requests.exceptions.ProxyError as e:
                print('\t Couldn\'t connect to proxy. Moving onto next proxy...')
                self.next_proxy()
                return None
            
            # Catch Timeout Errors and iterate proxy forward, otherwise raise an error.
            except requests.exceptions.Timeout as e:
                print('\t Proxy Timed out. Moving onto next proxy...')
                self.next_proxy()
                return None
            
            
    def run(self):
        
        scrape = True

        while scrape:

            t_request = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            print(f'[{t_request}] Sending Request with proxy {self.proxy}... ')

            response = self.make_request(method='get',url=self.url,proxies={'https':self.proxy},timeout=10)
            
            if response is not None:
                if response.status_code==200:
                
                    soup = BeautifulSoup(response.content, 'html.parser')
                    self.scraper(soup,self.exectime)

                    print('\t Success Sleeping for 15min now..')
                    time.sleep(900)
                else:
                    print(response)