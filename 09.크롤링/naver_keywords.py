import requests
from bs4 import BeautifulSoup
import time

def time_function(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time() - start_time
        print("{} {} time {}".format(f.__name__, args[1], end_time))
        return result
    return wrapper

@time_function
def r_fild_all(url, parser):
    r = requests.get(url)
    bs = BeautifulSoup(r.text, parser)
    lists = bs.find_all("li", {"class": "ah_item"})

    titles = []
    for li in lists:
        title = li.select("span.ah_k")[0].text
        titles.append(title)
    return titles

@time_function
def r_select(url, parser):
    r = requests.get(url)
    bs = BeautifulSoup(r.text, parser)
    lists = bs.select("li.ah_item")

    titles = []
    for li in lists:
        title = li.select("span.ah_k")[0].text
        titles.append(title)
    return titles
        
url = "https://www.naver.com"
r_fild_all(url, "html.parser")
r_select(url, "html.parser")

r_fild_all(url, "lxml")
r_select(url, "lxml")