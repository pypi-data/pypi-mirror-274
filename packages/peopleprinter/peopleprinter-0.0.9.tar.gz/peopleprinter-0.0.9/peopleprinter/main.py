import requests
import re
from manufacturers.KYOCERA.major_kyocera import KyoceraMajor
from manufacturers.HP.major_hp import HPMajor
from manufacturers.PANTUM.major_pantum import PantumMajor
from manufacturers.Xerox.major_xerox import XeroxMajor


class UnknownManufacturerError(Exception):
    """Кастомное исключение для неизвестного производителя."""
    pass


class PeoplePrinter:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.main_page = self.__get_main_page_printer()
        self.locate = self.__find_locate(ip_address)
        self.prod = self.__get_prod_printer()

    @staticmethod
    def __find_locate(ip_address):
        """Определяет локацию принтера по IP адресу."""
        locate_uid = re.findall(r"\d*.\d*.(\d*)\d.\d*", ip_address)[0]
        locates = {
            '0': 'Неизветно',
            '1': 'Olimp',
            '2': 'Sunmarinn',
            '4': 'Aurum',
            '6': 'Corudo'
        }
        if locate_uid in locates.keys():
            return locates.get(locate_uid)
        else:
            return locates.get(0)

    def __get_main_page_printer(self):
        """Получает главную страницу принтера по IP """
        detect_refresh = r'(http-equiv="refresh")'   # регулярное выражение на refresh redirect
        redirect_url = r'url=(.*)"'                  # read new url
        url = f'http://{self.ip_address}/'
        cookies = {'Cookie': 'SESSION_ID=1'}
        try:
            rq = requests.get(url, cookies=cookies, timeout=2).text
            if re.findall(detect_refresh, rq):
                re_url = re.findall(redirect_url, rq)[0]
                new_url = url + re_url
                rq = requests.get(new_url).text      # получение страницы после редиректа
                return rq
        except requests.exceptions.ConnectionError:
            return 'ConnectTimeout'
        return rq

    def __get_prod_printer(self):
        """Определяет производителя принтера по содержимому его главной страницы."""
        prod = 'Неопределен'
        factory = ['KYOCERA', 'HP', 'PANTUM', 'XEROX']
        for x in factory:
            if x in self.main_page.upper():
                prod = x
                break
        return prod

    def info(self):
        """Получает информацию о принтере в зависимости от производителя."""
        manufacturers = {
            'KYOCERA': KyoceraMajor,
            'HP': HPMajor,
            'PANTUM': PantumMajor,
            'XEROX': XeroxMajor
        }

        printer_class = manufacturers.get(self.prod)
        if not printer_class:
            raise UnknownManufacturerError(f"Производитель '{self.ip_address}' неизвестен.")

        return self.__work(printer_class(self.ip_address))

    def __work(self, printer):
        """Возвращает словарь с информацией о принтере."""
        return {
            'ip_address': self.ip_address,
            'mac_address': printer.mac(),
            'host_name': printer.host_name(),
            'prod': self.prod,
            'model': printer.model(),
            'locate': self.locate,
            'toner_lvl': printer.toner(),
            'prints_count': printer.prints_count()
        }


if __name__ == "__main__":
    ip = '10.12.21.87'
    try:
        printer = PeoplePrinter(ip)
        print(printer.info())
    except UnknownManufacturerError as e:
        print(e)
