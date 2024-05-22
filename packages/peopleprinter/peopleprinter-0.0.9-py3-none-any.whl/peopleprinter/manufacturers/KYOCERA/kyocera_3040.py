import time
import requests
import re


# def get_3040(ip_address):
#     url = f'http://{ip_address}/dvcinfo/dvcconfig/DvcConfig_Config.htm'
#
#     headers = {'Cookie': 'rtl=0; css=0',
#                'Referer': f"http://{ip_address}/startwlm/Start_Wlm.htm"}
#
#
#
#     page_code_info = requests.get(url, headers=headers)
#     print(page_code_info.text)
#     mac = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[175\]\+" :",(".{17}")', page_code_info.text)[0]
#     model = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[0\].*"(.*)","w272px"', page_code_info.text)[0]                # получть Модель
#     host_name = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[1\].*"(.*)","w272px"', page_code_info.text)[0]         # получить HostName



class Kyocera3040:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.headers = {'Cookie': 'rtl=0; css=0', 'Referer': f"http://{self.ip_address}/esu/DeepSleepApply.htm"}
        self._main_page = self._get_main_page()
        self._page_info = self._get_info_page()
        self._page_toner = self._get_toner_page()
        self._page_counter = self._page_counter()

    def _get_main_page(self):
        main_page = requests.get(f'http://{self.ip_address}/').text
        if 'DeepSleep.htm' in main_page:
            self._awakening()
        else:
            return main_page

    def _awakening(self):
        url = f'http://{self.ip_address}/esu/set.cgi'
        data = 'submit001=%D0%9F%D1%83%D1%81%D0%BA&okhtmfile=DeepSleepApply.htm&func=wakeup'
        requests.post(url, headers=self.headers, data=data)
        time.sleep(5)
        self._get_main_page()

    def _get_info_page(self):
        url_config = f'http://{self.ip_address}/dvcinfo/dvcconfig/DvcConfig_Config.htm'
        page_code_info = requests.get(url_config, headers=self.headers)
        return page_code_info.text

    def _get_toner_page(self):
        url_toner = f'http://{self.ip_address}/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.htm'
        page_code_toner = requests.get(url_toner, headers=self.headers)
        return page_code_toner.text

    def _page_counter(self):
        url_counter = f'http://{self.ip_address}/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.htm'
        page_code_counter = requests.get(url_counter, headers=self.headers)
        return page_code_counter.text

    def mac(self):
        mac = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[175\]\+" :",(".{17}")', self._page_info)[0]
        return mac

    def host_name(self):
        host_name = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[1\].*"(.*)","w272px"', self._page_info)[0]
        return host_name

    def model(self):
        model = re.findall(r'ComnAddLabelProperty\(\'2\'\,mes\[0\].*"(.*)","w272px"', self._page_info)[0]
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
        printed_total = re.findall(r"counterBlackWhite.0....(\d*)", self._page_counter)[0]  # получить оттиски
        copy_total = re.findall(r"counterBlackWhite.1....(\d*)", self._page_counter)[0]  # получить сканы
        prints_count = int(printed_total) + int(copy_total)  # получить cумму
        return prints_count


if __name__ == "__main__":
    ip = '192.168.1.33'
    print(Kyocera3040(ip))