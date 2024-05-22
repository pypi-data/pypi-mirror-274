import re
import requests


class KyoceraMajor:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.headers = {'Cookie': 'rtl=0; css=0', 'Referer': f"http://{self.ip_address}/startwlm/Start_Wlm.htm"}
        self._page_info = self._get_config_page()
        self._page_toner = self._get_toner_page()
        self._page_counter = self._page_counter()

    def _get_config_page(self):
        url_info = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvcconfig/DvcConfig_Config.model.htm'
        page_code_info = requests.get(url_info, headers=self.headers)
        return page_code_info.text

    def _get_toner_page(self):
        url_toner = f'http://{self.ip_address}/js/jssrc/model/startwlm/Hme_Toner.model.htm'
        page_code_toner = requests.get(url_toner, headers=self.headers)
        return page_code_toner.text

    def _page_counter(self):
        url_counter = f'http://{self.ip_address}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
        page_code_counter = requests.get(url_counter, headers=self.headers)
        return page_code_counter.text

    def mac(self):
        mac_address = re.findall(r".*macAddress = '(.*)'", self._page_info)[0]
        return mac_address

    def host_name(self):
        host_name = re.findall(r".*hostName = '(.*)'", self._page_info)[0]
        return host_name

    def model(self):
        model = re.findall(r".*model = '(.*)'", self._page_info)[0]
        return model

    def toner(self):
        toner_lvl = 'Error'
        try:
            data_toner = re.findall(r".*parseInt\('(\d*)',10\)\)", self._page_toner)  # получить остаток тонера
            toner_lvl = int(data_toner[0])
        except (ValueError, IndexError):
            pass
        finally:
            return toner_lvl

    def prints_count(self):
        printed_total = re.findall(r".*printertotal = \('(\d*)'\)", self._page_counter)[0]  # получить оттиски
        copy_total = re.findall(r".*copytotal = \('(\d*)'\)", self._page_counter)[0]        # получить сканы
        prints_count = int(printed_total) + int(copy_total)                                 # получить cумму
        return prints_count


if __name__ == "__main__":
    ip = '192.168.1.39'
    print(KyoceraMajor(ip).prints_count())
