#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pymongo


link = input("Enter a link:")
myclient = pymongo.MongoClient("Your mongodb uri")

mydb = myclient["project"]
mycol = mydb["houses"]

page_url = link

uClient = uReq(page_url)


page_soup = soup(uClient.read(), "html.parser")
uClient.close()


description = page_soup.find("div",{"class":"property-page__detail-content"}).find("p").get_text()

title = page_soup.find("div",{"class":"property-page__information"}).find("h1").findAll("span")[0].get_text()

details = page_soup.find("div",{"class":"detail-area"}).find("ul").findAll("li")

facilities = page_soup.find("ul",{"class":"checklist"}).findAll("li")

number = int(page_soup.find("a",{"class":"contact-phones"}).get_text())

name = page_soup.find("div",{"class":"owner-detail"}).find("ul").find("li").find("strong").get_text()

price = page_soup.find("div",{"class":"amount"}).find("h2").get_text()

default_detail = ["beds","kitchen","living","Bathrooms", "Floors", "price"]

facilities_arr = []

detail_dic = {}
price = ''.join(re.findall(r'\d+',price))
des = ' '.join(str(description).split())

for li in details:
    key = str(li.get_text()).split(':')[0]
    value = str(li.find("strong").get_text())
    detail_dic[key[1:]] = value


for li in facilities:
    facilities_arr.append(' '.join(str(li.get_text())[4:].split()))


eObj = {
    "name":str(name),
    "title":str(title),
    "location":str(title.split(' ')[2]),
    "description":des,
    "number":int(number),
    "facilities":facilities_arr,
    "details":detail_dic,    
    "price":int(price)
}


print(eObj)

#send data to mongodb cloud
x = mycol.insert_one(eObj)
