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
        
    def next_proxy(self):
        ''' Fetch the next proxy. Once empty raise an Exeption to end the process.'''
        try:
            next_proxy = next(self.proxies)
            self.proxy = next_proxy
            return next_proxy
        
        except:
            self.proxy = None
    
    def make_request(self,**kwargs):
        ''' Make a Request. If unsuccesful try the next proxy.'''
        while self.proxy!=None:
            try:
                response = requests.request(**kwargs)
                return response
            
            # Catch Timeout Errors and print all others to console
            except requests.exceptions.Timeout as e:
                print('Failed. Moving onto next proxy...')
                self.next_proxy()

            except Exception as e:
                raise Exception(e)
            
            
    def run(self):
        
        scrape = True
        
        counter = 0
        while scrape:
            
            next_proxy = False
            counter+=1
            
            print(f'Sending Request with proxy {self.proxy}... ')
            
            try:
                response = self.make_request(method='get',url=self.url,proxies={'https':self.proxy},timeout=5)
                
                if response.status_code==200:
                    #print("Success!")
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    output_df,name = self.scraper(soup)
                    filename = name+'-'+datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                    output_df.to_json(f'{filename}.json',orient='records')
                    
                    print('Success Sleeping for 30min now..')
                    return soup
                    break
                    # Sleep for 30 minutes before next request
                    time.sleep(1800)
                else:
                    next_proxy=True

            except Exception as e:
                print(f'\t failed with Error code \"{e}\"')
                next_proxy=True
                
            if next_proxy:
                try:
                    check = self.next_proxy()
                except:
                    scrape = False
                    print("Tried all proxies. Now exiting.")
                    
            time.sleep(1)