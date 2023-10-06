from working_with_vacancies import *

maximum()


# working with user

class PickApi:

    def __init__(self):


        job_handle = Json_JobDataHandler("jobs.json")
        with open('jobs.json', 'w', encoding='utf-8'):
            pass

        print("Hello, from which site would you like to see the vacancies?")
        print("Press 1 for HeadHunter.")
        print("Press 2 for SuperJob.")
        print("Press 'Enter' if you want both.")

        api = input()
        if api == "1":
            print("You chose HeadHunter!")
            profession = input("Which profession are you looking for?: ")
            hh_api = HeadHunter_API(profession)
            loading(hh_api)
            job_filling_hh(hh_api.data)
            for job in jobs:
                job_handle.add_job(job)
            for job in jobs:
                print(job)

        elif api == "2":
            print("You chose SuperJob!")
            profession = input("Which profession are you looking for?: ")
            sj_api = SuperJob_API(profession)
            loading(sj_api)
            job_filling_sj(sj_api.data)
            for job in jobs:
                job_handle.add_job(job)
            for job in jobs:
                print(job)

        else:
            print("You chose both!")
            profession = input("Which profession are you looking for?: ")
            hh_api = HeadHunter_API(profession)
            sj_api = SuperJob_API(profession)
            loading(hh_api)
            loading(sj_api)
            job_filling_hh(hh_api.data)
            job_filling_sj(sj_api.data)
            for job in jobs:
                job_handle.add_job(job)
            for job in jobs:
                print(job)


class PickTopJobs(PickApi):
    def __init__(self):
        super().__init__()


# "менеджер", "повар", "программист", "Курьер",

user = PickTopJobs()
