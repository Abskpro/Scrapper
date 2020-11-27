#!/usr/bin/env python3

import re
import names
import random
import string
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pymongo


link = input("Enter a link:")
myclient = pymongo.MongoClient("mongodb+srv://absk2:yl9iVpqA2BYRieyH@cluster0.6eycv.mongodb.net/project?retryWrites=true&w=majority")


mydb = myclient["project"]
mycol = mydb["rooms"]


page_url = link

#request connection to url
uClient = uReq(page_url)

#read the data from website and parse it as html
page_soup = soup(uClient.read(), "html.parser")
# uClient.close()

#select and retrive datas
description = page_soup.find("div",{"class":"comment"}).get_text()
# title = page_soup.find("div")
location = page_soup.find("ul",{"class":"ht-facilities"}).find("li").get_text()
price = page_soup.find("div",{"class":"deal-pricebox"}).find("div").find("h3").get_text()
details = page_soup.find("div",{"class":"main-list"}).find("ul").findAll("li")

#since no email exists this module creates a dummy email
def random_char(y):
           return ''.join(random.choice(string.ascii_letters) for x in range(y))

#triming the price and removing any characters and symbol
price_trim = price[3:].replace(',','')
details_trim = []
#remove unused character from description by slicing string and remove space from right side
description_trim = str(description[4:]).rstrip()
location_trim = location[1:]
#generate random email
email_random = random_char(7).lower() + "@gmail.com"
# print(email_random)
print(''.join(location))


#triming details 
for li in details:
    m = str(li.get_text())
    details_trim.append(int(m[-2:]))

#since facilities were not being able to select creating own facilities array and selecting random facilities
facilitiesArr = ["CableTv","Internet","Water-Supply","Parking"]
#generate random number to select facilities
rnd_facilities =random.sample(range(0,4),3)

#since option of furnished does'nt exists creating random choices
furnished = ["Not Furnished", "Semi Furnished", "Fully Furnished"]
rnd_furnished = random.randint(0,2)
# print("this is " , rnd_furnished)


#createing a json object to store data to mongodb
eObj = {
    "name":names.get_full_name(),
    "title":str(f'Room at {location}'),
    "number":9841743567,
    "email":email_random,
    "location":location_trim,
    "description":description_trim,
    "price":int(price_trim),
    "coordinates":{
        "latitude":0,
        "longitude":0
    },
    "rooms":{
        "bedroom":details_trim[0],
        "livingRoom":details_trim[1],
        "kitchen":details_trim[2],
        "toilet":details_trim[3],
    },
    "facilities":[facilitiesArr[rnd_facilities[0]],facilitiesArr[rnd_facilities[1]],facilitiesArr[rnd_facilities[2]]],
    "furnished":furnished[rnd_furnished],
}

print(eObj)


# x = mycol.insert_one(eObj)
