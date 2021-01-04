import requests, json, time, pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict

def get_proxies(proxy_url=None):
    
    proxy_url = 'https://www.sslproxies.org/'
    r = requests.get(proxy_url)

    soup = BeautifulSoup(r.content, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')
    
    proxies = list()
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append(row.find_all('td')[:2])
    f = lambda x: 'http:' + x[0].string + ':' + x[1].string

    return list(map(f,proxies))


def send_request(url,proxy):
    
    proxy_name = f'http://{proxy}'
    proxy = {'https':proxy_name}
    
    try:
        response = requests.get(url,proxies=proxy,timeout=3)
    except Exception:
        print("Ooops there was an error")
        return None
    
    if not response.ok:
        print('Server Response:',response.status_code)
    else:
        soup = BeautifulSoup(response.content,'html.parser')
    return soup


def find_item(listing,find_key,find_attrs):
    try:
        item = listing.find(find_key,attrs=find_attrs)
        item = str(item.find(text=True, recursive=True))
    except:
        item = None
    return item
    
    
def ScrapeNewListing(soup):
    
    data_dict = defaultdict(list)
    listings = soup.findAll('li')
    
    for listing in listings:
        prod_name=" "
        prod_price = " "
        for name in listing.find_all('h3', attrs={'class':"s-item__title"}):
            if(str(name.find(text=True, recursive=False))!="None"):
                prod_name=str(name.find(text=True, recursive=False))
                #item_name.append(prod_name)

                data_dict['listing name'].append(prod_name)

        if(prod_name!=" "):
            price = find_item(listing,'span',{'class':'s-item__price'})
            data_dict['price'].append(price)

            postage = find_item(listing,'span',{'class':'s-item__shipping s-item__logisticsCost'})
            data_dict['postage'].append(postage)

            listing_date = find_item(listing,'span',{'class':'s-item__dynamic s-item__listingDate'})
            data_dict['listing_date'].append(listing_date)

            country = find_item(listing,'span',{'class':'s-item__location s-item__itemLocation'})
            data_dict['country'].append(country)

            buying_option = find_item(listing,'span',{'class':'s-item__purchase-options-with-icon'})
            data_dict['buying_option'].append(buying_option)

            # Maybe link this to the get request instead of creating a timestamp here
            scraping_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_dict['scraping_time'].append(scraping_time)
            
    return pd.DataFrame(data_dict),'new-listings'

def save_json(obj,filename):
    with open(filename,'w') as file:
        json.dump(obj,file)