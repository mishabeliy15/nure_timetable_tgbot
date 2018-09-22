import imgkit
import os.path
import time
import datetime

pzpi18_5_id = 7195531  # PZPI 18-5

nure_api_url1 = "http://cist.nure.ua/ias/app/tt/WEB_IAS_TT_GNR_RASP.GEN_GROUP_POTOK_RASP?ATypeDoc=1&Aid_group="
nure_api_url2 = "&Aid_potok=0&ADateStart=01.09.2018&ADateEnd=31.12.2018"



def get_url(id_group=7195531):
    temp_url = nure_api_url1 + str(id_group) + nure_api_url2
    print(temp_url)
    return temp_url

def get_img_name(id_group=7195531):
    return "Group_PZPI_" + str(id_group) + ".jpg"

def update_with_cashe(id_group=7195531):
    file_name = get_img_name(id_group)
    if (os.path.exists(file_name)):
        time_create = os.path.getctime(file_name)
        delta = time.time() - time_create
        if (delta / 60 > 30):
            update_photo(id_group)
    else:
        update_photo(id_group)

def update_photo(id_group):
    try:
        imgkit.from_url(get_url(id_group), get_img_name(id_group))
    except Exception:
        logging("Error update_photo(with access)")

def logging(str):
    now = datetime.datetime.now()
    filename = now.date().__str__() + ".log"
    f = open(filename, "a")
    temp_str = "[{0}] {1}\n".format(now.today(),str)
    f.write(temp_str)
    f.close()