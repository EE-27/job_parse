import requests
import os
from abc import ABC, abstractmethod


class LoadApi(ABC):

    @abstractmethod
    def load(self):
        pass


class HeadHunter_API(LoadApi):

    def __init__(self, keyword):
        self.data = None
        self.url = 'https://api.hh.ru/'
        self.endpoint = 'vacancies'
        self.keyword = keyword  # "менеджер"
        self.params = {'text': self.keyword}  #: 'менеджер'}

        self.response = requests.get(f'{self.url}{self.endpoint}', params=self.params)

    def load(self):
        if self.response.status_code == 200:
            self.data = self.response.json()
            #  print(self.data)
            return self.data
        else:
            return (f"Error when requesting data. Status code: {self.response.status_code}")


class SuperJob_API(LoadApi):

    def __init__(self, keyword):
        self.data = None
        self.sj_url = "https://api.superjob.ru/2.0/vacancies/"
        self.key = os.getenv("API_SuperJob")

        self.keyword = keyword  # "менеджер"

        payload = {}

        params = {'keyword': {self.keyword}}

        headers = {
            "Host": "api.superjob.ru",  # added
            "X-Api-App-Id": self.key,
            "Authorization": "Bearer r.000000010000001.example.access_token",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.response = requests.request("GET", self.sj_url, headers=headers, params=params, data=payload)

    def load(self):
        if self.response.status_code == 200:
            self.data = self.response.json()
            return self.data
        else:
            return f"Error when requesting data. Status code: {self.response.status_code}"


def loading(api):
    api.load()
