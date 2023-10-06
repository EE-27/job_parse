from load_api import *
from working_with_vacancies import *


maximum()


# working with user

class PickApi:

    def __init__(self):
        print("Hello, from which site would you like to see the vacancies?")
        print("Press 1 for HeadHunter.")
        print("Press 2 for SuperJob.")
        print("Leave emtpy if you want both.")
        api = int(input())
        if api == "":
            api = 5

        if api in (1, 2):
            if api == 1:
                print("You chose HeadHunter!")
                proffesion = input("Which profession are you looking for?: ")
                hh_api = HeadHunter_API(proffesion)
                loading(hh_api)

            else:
                print("You chose SuperJob!")
                proffesion = input("Which profession are you looking for?: ")
                sj_api = SuperJob_API(proffesion)
                loading(sj_api)
        else:
            print("You chose both!")
            proffesion = input("Which profession are you looking for?: ")
            hh_api = HeadHunter_API(proffesion)
            sj_api = SuperJob_API(proffesion)
            loading(hh_api)
            loading(sj_api)
            job_filling_hh(hh_api.data)
            job_filling_sj(sj_api.data)

user = PickApi()
