import requests
from bs4 import BeautifulSoup

#product url
url = "https://www.gamerhut.com.br/MLB-2778706911-jg-teenage-mutant-ninja-turtles-cowabunga-collection-switch-_JM#position=38&search_layout=grid&type=item&tracking_id=c43ce481-e766-441c-be5c-e616adc8f918"

#http request to know page content
headers = {"user-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

#verify if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    #price tag
    price_tag = soup.find("span", class_="andes-money-amount__fraction")
    name_tag = soup.find("h1", class_="ui-pdp-title")
    #image_tag = soup.find("img", class_="ui-pdp-image ui-pdp-gallery__figure__image")

    if price_tag:
        price = price_tag.get_text(strip=True)
        name = name_tag.get_text(strip=True)
        print(f"{name}: R$ {price}")
    else:
        print("Price not found")

    #identify name and price product tag
    #print(soup.prettify()) #to see html page
else:
    print("Access page error")
