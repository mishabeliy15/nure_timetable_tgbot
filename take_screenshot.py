import requests

url_nure="http://cist.nure.ua/ias/app/tt/f?p=778:201:3267822060372525:::201:P201_FIRST_DATE,P201_LAST_DATE,P201_GROUP,P201_POTOK:01.09.2018,31.12.2018,7195531,0:"
url = "http://mini.s-shot.ru/1920/1280/jpeg/?"+url_nure

def update_photo():
    p = requests.get(url)
    out = open("img.jpg", "wb")
    out.write(p.content)
    out.close()