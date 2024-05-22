import re
import requests
from bs4 import BeautifulSoup


class HPMajor:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self._page_with_info = self._get_info_page()
        self._page_toner = self._get_toner_page()

    def _get_info_page(self):
        url_info = f'''http://{self.ip_address}/info_configuration.html?tab=Home&menu=DevConfig'''
        page_code_info = requests.get(url_info).text
        bs_code_info = BeautifulSoup(page_code_info, "html.parser")
        return bs_code_info

    def _get_toner_page(self):
        url_toner = f'''http://{self.ip_address}/info_suppliesStatus.html?tab=Home&menu=SupplyStatus'''  # page with toner
        page_code_toner = requests.get(url_toner).text
        bs_code_toner = BeautifulSoup(page_code_toner, "html.parser")
        return bs_code_toner

    def mac(self):
        td = self._page_with_info.find("td", string='Аппаратный адрес:')
        td_parent = td.find_parent('tr')
        mac_address_unsorted = td_parent.find(class_='itemFont').text
        mac_address = (re.findall(r"(\w\w.*\w\w)", mac_address_unsorted)[0]).upper()
        return mac_address

    def host_name(self):
        td = self._page_with_info.find("td", string='Имя хоста:')
        td_parent = td.find_parent('tr')
        host_name_unsorted = td_parent.find(class_='itemFont').text
        host_name = (re.findall(r"(\w\w.*\w\w)", host_name_unsorted)[0]).upper()
        return host_name

    def model(self):
        td = self._page_with_info.find("td", string='Название продукта:')
        td_parent = td.find_parent('tr')
        model = td_parent.find(class_='itemFont').text
        return model

    def toner(self):
        data_toner = self._page_toner.find(class_='SupplyName width35 alignRight')
        toner_lvl = (re.findall(r"(\d+)", data_toner.text)[0])
        return toner_lvl

    def prints_count(self):
        td = self._page_with_info.find("td", string='Всего оттисков:')
        td_parent = td.find_parent('tr')
        prints_count = td_parent.find(class_='itemFont').text
        return prints_count

    # def full_info(self):
    #     return {'ip_address': self.ip_address, 'mac_address': self.mac, 'host_name': self.host_name, 'prod': self.prod,
    #             'model': self.model, 'locate': self.locate, 'toner_lvl': self.toner, 'prints_count': self.prints_count,
    #             'status': 'Done'}


if __name__ == "__main__":
    ip = '192.168.2.104'
    print(HPMajor(ip).mac)
