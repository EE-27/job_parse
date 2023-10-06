from working_with_vacancies import *

# working with user


class PickApi:

    def __init__(self):


        job_handle = Json_JobDataHandler("jobs.json")
        with open('jobs.json', 'w', encoding='utf-8'):
            pass

        print("Hello, from which site would you like to see the vacancies?")
        print("Press '1' for HeadHunter.")
        print("Press '2' for SuperJob.")
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


        elif api == "2":
            print("You chose SuperJob!")
            profession = input("Which profession are you looking for?: ")
            sj_api = SuperJob_API(profession)
            loading(sj_api)
            job_filling_sj(sj_api.data)
            for job in jobs:
                job_handle.add_job(job)


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



class PickTopJobs(PickApi):
    def __init__(self):
        super().__init__()
        jobs_with_salary = []
        for job in jobs:
            if job.salary_from is not None:
                jobs_with_salary.append(job)
        while True:
            try:
                print("Filtering job by salary, if job does not have salary, its omitted.")
                top_n = int(input("How many top jobs do you want to see (filtered by salary)? "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        sorted_jobs = sorted(jobs_with_salary, key=lambda job: job.salary_from, reverse=True)
        top_jobs = sorted_jobs[:top_n]
        print(f"Top-{top_n} jobs:")
        for i, job in enumerate(top_jobs):
            print(f"{i + 1}. {job.name};#{job.job_id} - {job.salary_from} {job.salary_currency}")


class PickTopJobs2:
    def __init__(self):
        jobs_with_salary = []
        for job in jobs:
            if job.salary_from is not None:
                jobs_with_salary.append(job)
        while True:
            try:
                print("Filtering job by salary, if job does not have salary, its omitted.")
                top_n = int(input("How many top jobs do you want to see (filtered by salary)? "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        sorted_jobs = sorted(jobs_with_salary, key=lambda job: job.salary_from, reverse=True)
        top_jobs = sorted_jobs[:top_n]
        print(f"Top-{top_n} jobs:")
        for i, job in enumerate(top_jobs):
            print(f"{i + 1}. {job.name};#{job.job_id} - {job.salary_from} {job.salary_currency}")



# "менеджер", "повар", "программист", "Курьер",


PickApi()
PickTopJobs2()

print(JobOffer.max_pay(jobs))
