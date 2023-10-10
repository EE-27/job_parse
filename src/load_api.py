import requests
import os
from abc import ABC, abstractmethod


class LoadApi(ABC):
    """
    Abstract base class for API loaders.
    """

    @abstractmethod
    def load(self):
        """
        Load data from the API.

        Returns:
            dict or str: The loaded data from the API if successful, or an error message if the request fails.
        """
        pass


class HeadHunter_API(LoadApi):
    """
    API loader for HeadHunter job vacancies.
    """

    def __init__(self, keyword):
        """
        Initialize the HeadHunter API loader.

        Args: keyword (str): The keyword to search for in job vacancies.
        """
        self.data = None
        self.url = 'https://api.hh.ru/'
        self.endpoint = 'vacancies'
        self.keyword = keyword  # "менеджер"
        self.params = {'text': self.keyword}  #: 'менеджер'}

        self.response = requests.get(f'{self.url}{self.endpoint}', params=self.params)

    def load(self):
        """
        Load data from the HeadHunter API.

        Returns: dict or str: The loaded data from the API if successful, or an error message if the request fails.
        """
        if self.response.status_code == 200:
            self.data = self.response.json()
            #  print(self.data)
            return self.data
        else:
            return (f"Error when requesting data. Status code: {self.response.status_code}")


class SuperJob_API(LoadApi):
    """
    API loader for SuperJob job vacancies.
    """

    def __init__(self, keyword):
        """
        Initialize the SuperJob API loader.

        Args: keyword (str): The keyword to search for in job vacancies.
        """
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
        """
        Load data from the SuperJob API.

        Returns: dict or str: The loaded data from the API if successful, or an error message if the request fails.
        """
        if self.response.status_code == 200:
            self.data = self.response.json()
            return self.data
        else:
            return f"Error when requesting data. Status code: {self.response.status_code}"


def loading(api):
    """
    Load data from the specified API.

    Args: api (LoadApi): An instance of a class that implements the LoadApi interface.

    Returns: dict or str: The loaded data from the API if successful, or an error message if the request fails.
    """
    api.load()
