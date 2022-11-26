from concurrent.futures import ThreadPoolExecutor
import time


urls = ["python-engineer.com",
        "twitter.com",
        "youtube.com"]

def scrape_site(url):
    res = f'{url} was scraped!'
    if url == "youtube.com":
        time.sleep(5)    
    return res

pool = ThreadPoolExecutor(max_workers=8)

results = pool.map(scrape_site, urls) # does not block

for res in results:
    print(res) # print results as they become available


print('Acabou as threads')

pool.shutdown()