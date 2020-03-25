import requests
from bs4 import BeautifulSoup
import json
import pprint

def get_bang(keyword):
    url = "https://apis.zigbang.com/search/all?q={}&type=oneroom".format(keyword)
    r = requests.get(url)
    result = json.loads(r.text)
    if result["success"]:
        lat = result["items"][0]["lat"]
        lng = result["items"][0]["lng"]

    south = lat - 0.03370855171711
    north = lat + 0.0335695291371
    west = lng - 0.0319765406923
    east = lng + 0.0320013566581

    url = "https://apis.zigbang.com/v3/items2?lat_south={}&lat_north={}&lng_west={}&lng_east={}&room=[01,02,03,04,05]".format(south, north, west, east)
    r = requests.get(url)
    result = json.loads(r.text)
    item_ids = []
    for item in result["list_items"]:
        item_ids.append(item["simple_item"]["item_id"])

    url = "https://apis.zigbang.com/v3/items?detail=true&item_ids={}".format(item_ids[0:60])
    r = requests.get(url)
    result = json.loads(r.text)

    bang_lists = []

    for i in result["items"]:
        title = i["title"]
        it = i["item"]
        addr1 = it["address1"]
        addr2 = it["address2"]
        addr3 = it["address2"]
        deposit = it["deposit"]
        rent = it["rent"]
        size = it["size"]
        size_m2 = it["size_m2"]
        s_title = it["title"]

        bang_lists.append((title, addr1, addr2, addr3, deposit, rent, size, size_m2, s_title))

    return bang_lists

for i in get_bang("서울시 종로구"):
    print(i)