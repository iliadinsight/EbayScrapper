import requests, json, time, pandas as pd, os
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
    

def get_listings(soup,exectime):

    listings = soup.findAll('li',attrs={'class':'s-item s-item--watch-at-corner'})
    data = dict()
    data = defaultdict(list)

    for listing in listings:

        title = listing.find('h3',attrs={'class':'s-item__title'})
        title = str(title.find(text=True, recursive=False))
        data['Title'].append(title)

        listing_url = listing.find('a',attrs={'class':'s-item__link'}).get('href')
        data['url_link'].append(listing_url)

        price = find_item(listing,'span',{'class':'s-item__price'})
        data['price'].append(price)

        postage = find_item(listing,'span',{'class':'s-item__shipping s-item__logisticsCost'})
        data['postage'].append(postage)

        listing_date = find_item(listing,'span',{'class':'s-item__dynamic s-item__listingDate'})
        data['listing_date'].append(listing_date)

        country = find_item(listing,'span',{'class':'s-item__location s-item__itemLocation'})
        data['country'].append(country)

        buying_option = find_item(listing,'span',{'class':'s-item__purchase-options-with-icon'})
        data['buying_option'].append(buying_option)

        # Maybe link this to the get request instead of creating a timestamp here
        scraping_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['scraping_time'].append(scraping_time)
    
    # Savings outputs - slightly convoluted use of os package is needed so that this logic works in both windows and linux
    current_path = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(current_path,f'Data/{exectime}')

    filename = 'listings-'+ datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.csv'
    filepath = os.path.join(data_dir,filename)
    
    try:
        os.makedirs(data_dir)
        pd.DataFrame(data).to_csv(filepath)

    except OSError as e:
        pd.DataFrame(data).to_csv(filepath)


def save_json(obj,filename):
    with open(filename,'w') as file:
        json.dump(obj,file)