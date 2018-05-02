import requests
import os
import random
import time

API_KEY = "API КЛЮЧ ВАШЕГО СООБЩЕСТВА"
GROUP_ID = 000000000 # id ваше сообщества

API_URL = "https://api.vk.com/method/"
API_VERSION = "5.69"

def make_request(method: str, params: dict):
    """ Метод для выполнения запроса к VK
    """
    params["v"] = API_VERSION
    params["access_token"] = API_KEY
    url = "%s%s" % (API_URL, method)
    return requests.post(url, params)

def gel_all_photos():
    """ Функция для получения фотографий из папки
    """
    return os.listdir("./photos")

def get_random_photo():
    """ Функция получения рандомной фотографии из папки
    """
    try:
        photos = gel_all_photos()
        rand_file_index = random.randint(0, len(photos) - 1)
        return './photos/' + photos[rand_file_index]
    except IndexError:
        print("Фото не найдены")

def get_server_for_upload_cover():
    """ Получает сервер для загрузки обложки
    """
    try:
        r = make_request("photos.getOwnerCoverPhotoUploadServer", {
            "group_id": GROUP_ID,
            'crop_x': 0,
            'crop_y': 0,
            'crop_x2': 1590,
            'crop_y2': 440
        }).json()

        return r["response"]["upload_url"]
    except IndexError:
        print(r)

def upload_files_to_server(server_for_upload: str, files: dict) -> dict:
    """ Загружает файлы на сервер вк
    """
    r = requests.post(server_for_upload, files=files)
    return r.json()

def save_uploades_photo(hash: str, photo: str):
    """ Сохраняет обложку
    """ 
    params = {
        "hash": hash,
        "photo": photo
    }

    make_request('photos.saveOwnerCoverPhoto', params)

def main():
    server_for_upload = get_server_for_upload_cover()
    photo = get_random_photo()

    if server_for_upload and photo:
        files = {
            'file': open(photo, 'rb')
        }

        r = upload_files_to_server(server_for_upload, files)

        if "hash" in r:
            save_uploades_photo(r["hash"], r["photo"])

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)