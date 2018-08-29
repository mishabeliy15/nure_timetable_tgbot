import requests
import os.path
import time

pzpi18_5_id = 7195531  # PZPI 18-5

nure_api_url1 = "http://cist.nure.ua/ias/app/tt/WEB_IAS_TT_GNR_RASP.GEN_GROUP_POTOK_RASP?ATypeDoc=1&Aid_group="
nure_api_url2 = "&Aid_potok=0&ADateStart=01.09.2018&ADateEnd=31.12.2018"

img_api = "http://mini.s-shot.ru/1920/1280/jpeg/?"


def get_url(id_group=7195531):
    return img_api + nure_api_url1 + str(id_group) + nure_api_url2

def get_img_name(id_group=7195531):
    return "Group_PZPI_" + str(id_group) + ".jpg"

def update_photo(id_group=7195531):
    p = requests.get(get_url(id_group))
    out = open(get_img_name(id_group), "wb")
    out.write(p.content)
    out.close()


def update_with_cashe(id_group=7195531):
    file_name = get_img_name(id_group)
    if (os.path.exists(file_name)):
        time_create = os.path.getctime(file_name)
        delta = time.time() - time_create
        if (delta / 60 > 30):
            update_photo(id_group)
    else:
        update_photo(id_group)
