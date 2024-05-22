import requests
import re
#
# # def get():
# #     s = requests.Session()
# #     # url = 'http://192.168.2.42/status/consumables.dhtml'
# #
# #     url = 'http://192.168.2.42/properties/generalSetup/billingCounters/billing_info.dhtml'
# #     cookies = {'Cookie': 'SESSION_ID=1'}
# #     total_r = r"Total Impressions:\n.*\n.*\n...(\d*)"
# #     total = re.findall(r"Total Impressions:\n.*\n.*\n...(\d*)", total_r)[0]
# #     print(total)
# #     print(s.get(url, cookies=cookies).text)
#
# def get_counts(ip_address):
#     url = f'http://{ip_address}/properties/generalSetup/billingCounters/billing_info.dhtml'
#     cookies = {'Cookie': 'SESSION_ID=1'}
#     r = requests.get(url, cookies=cookies).text
#     total_counts = re.findall(r"Total Impressions:\n.*\n.*\n...(\d*)", r)[0]
#     return total_counts
#
#
# def get_toner(ip_address):
#     url = f'http://{ip_address}/status/consumables.dhtml'
#     cookies = {'Cookie': 'SESSION_ID=1'}
#     r = requests.get(url, cookies=cookies).text
#
# def get():
#     url = 'http://192.168.2.145/properties/generalSetup/configuration/configuration.dhtml'
#     cookies = {'Cookie': 'SESSION_ID=1'}
#     r = requests.get(url, cookies=cookies)
#     print(r.text)


class XeroxMajor:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.headers = {'Cookie': 'SESSION_ID=1'}
        self._page_info = self._get_config_page()
        self._page_toner = self._get_toner_page()
        self._page_counter = self._page_counter()

    def _get_config_page(self):
        url_info = f'http://{self.ip_address}/properties/generalSetup/configuration/configuration.dhtml'
        page_code_info = requests.get(url_info, headers=self.headers)
        return page_code_info.text

    def _get_toner_page(self):
        url_toner = f'http://{self.ip_address}/status/consumables.dhtml'
        page_code_toner = requests.get(url_toner, headers=self.headers)
        return page_code_toner.text

    def _page_counter(self):
        url_counter = f'http://{self.ip_address}/properties/generalSetup/billingCounters/billing_info.dhtml'
        page_code_counter = requests.get(url_counter, headers=self.headers)
        return page_code_counter.text

    def mac(self):
        mac_address = re.findall(r"MAC Address:[\r\n].*[\r\n].*[\r\n].*[\r\n]....(.*).{3}", self._page_info)[0]
        return mac_address

    def host_name(self):
        host_name = re.findall(r"Device Name:[\r\n].*[\r\n].*[\r\n].*[\r\n]....(.*).{2}", self._page_info)[0]
        return host_name

    def model(self):
        model = 'MODEL'
        return model

    def toner(self):
        total_toner = re.findall(r'tonerLife...."(.*)"', self._page_toner)[0]
        return total_toner

    def prints_count(self):
        total_counts = re.findall(r"Total Impressions:\n.*\n.*\n...(\d*)", self._page_counter)[0]
        return total_counts


if __name__ == "__main__":
    ip = '192.168.2.145'
    print(XeroxMajor(ip).mac)
