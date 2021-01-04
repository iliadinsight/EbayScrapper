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
                print('\t Proxy Timed out. Moving onto next proxy...')
                self.next_proxy()

            except requests.exceptions.ProxyError as e:
                print('\t Couldn\'t connect to proxy. Moving onto next proxy...')
                self.next_proxy()

            except Exception as e:
                raise Exception(e)
            
            
    def run(self):
        
        scrape = True

        while scrape:
            
            print(f'Sending Request with proxy {self.proxy}... ')

            response = self.make_request(method='get',url=self.url,proxies={'https':self.proxy},timeout=5)
                
            if response.status_code==200:
                
                soup = BeautifulSoup(response.content, 'html.parser')
                output_df,name = self.scraper(soup)
                filename = name+'-'+datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
                output_df.to_json(f'./Data/{filename}.json',orient='records')
                
                print('Success Sleeping for 30min now..')
                return soup
                break
                # Sleep for 30 minutes before next request
                time.sleep(1800)
                    
            time.sleep(1)