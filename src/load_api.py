import requests
import os
from abc import ABC, abstractmethod


class LoadApi(ABC):

    @abstractmethod
    def load(self):
        pass


class HeadHunter_API(LoadApi):

    def __init__(self):
        self.url = 'https://api.hh.ru/'
        self.endpoint = 'vacancies'  # Указываем эндпоинт для запроса вакансий
        self.params = {'text': 'менеджер'}  #: 'менеджер'}  # , 'page': 1, 'per_page': 10}

        self.response = requests.get(f'{self.url}{self.endpoint}', params=self.params)

    def load(self):
        if self.response.status_code == 200:
            data = self.response.json()
            print(data)
        else:
            print(f"Error when requesting data. Status code: {self.response.status_code}")


class SuperJob_API(LoadApi):

    def __init__(self):
        self.sj_url = "https://api.superjob.ru/2.0/vacancies/"
        self.key = os.getenv("API_SuperJob")

        payload = {}
        headers = {
            "X-Api-App-Id": self.key,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.response = requests.request("GET", self.sj_url, headers=headers, data=payload)
    def load(self):
        if self.response.status_code == 200:
            data = self.response.json()
            print(data)
        else:
            print(f"Error when requesting data. Status code: {self.response.status_code}")


def loading(api):
    api.load()

hh_api = HeadHunter_API()
sj_api = SuperJob_API()

loading(sj_api)
loading(hh_api)