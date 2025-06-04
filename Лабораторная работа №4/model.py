import requests
from xml.etree import ElementTree


class CurrencyRates:
    """
    Класс для работы с курсами валют ЦБ РФ.
    Реализует паттерн Singleton.
    """
    _instance = None
    _currencies = ["USD", "EUR"]  # Валюты по умолчанию
    _rates = {}  # Кэш текущих курсов

    def __new__(cls):
        """Реализация паттерна Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def fetch_rates(self):
        """
        Получение курсов валют с API ЦБ РФ
        Возвращает словарь {код валюты: курс}
        """
        try:
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
            response = requests.get(url)
            response.raise_for_status()  # Проверка на ошибки HTTP

            root = ElementTree.fromstring(response.content)
            self._rates = {}

            for currency in root.findall("Valute"):
                code = currency.find("CharCode").text
                if code in self._currencies:
                    value = currency.find("Value").text.replace(",", ".")
                    nominal = int(currency.find("Nominal").text)
                    self._rates[code] = round(float(value) / nominal, 4)

            return self._rates
        except Exception as e:
            print(f"Ошибка при получении курсов: {e}")
            return {}

    @property
    def currencies(self):
        """Геттер для списка валют"""
        return self._currencies

    @currencies.setter
    def currencies(self, new_currencies):
        """Сеттер для списка валют"""
        if all(len(c) == 3 for c in new_currencies):
            self._currencies = new_currencies
        else:
            raise ValueError("Коды валют должны состоять из 3 символов")

    @property
    def rates(self):
        """Геттер для текущих курсов"""
        return self._rates