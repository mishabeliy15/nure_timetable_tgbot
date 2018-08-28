import imgkit

options = {
    'height':720,
    'crop-h': '720',
    'crop-w': '1800',
}

url = 'http://cist.nure.ua/ias/app/tt/f?p=778:201:3267822060372525:::201:P201_FIRST_DATE,P201_LAST_DATE,P201_GROUP,P201_POTOK:01.09.2018,31.12.2018,7195531,0:'

def update_photo():
    imgkit.from_url(url, 'out.jpg', options=options)