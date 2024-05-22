import requests
import re

url = 'http://192.168.1.88/index.html'
r1 = r'>(.*)%<'


class PantumMajor:
    def __init__(self, ip_address):
        self.ip_address = ip_address
    def get_toner(self):
        '''Парс CSS, получение списка содержищего значение заполения полоски тонера'''
        url_str = f'http://{self.ip_address}/css/style.css'
        r = requests.get(url_str).text
        value = re.findall(r".*width:.(.*)%;", r)[3]
        return value


# def get_toner(ip_address):
#         '''Парс CSS, получение списка содержищего значение заполения полоски тонера'''
#         url_str = f'http://{ip_address}/css/style.css'
#         r = requests.get(url_str).text
#         value = re.findall(r".*width:.(.*)%;", r)[3]
#         return value
#
#
# def get_info():
#     page = requests.get(url).text
#     toner = re.findall(r1, page)
#     return page
