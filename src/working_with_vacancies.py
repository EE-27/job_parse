from load_api import *


class JobOffer:

    def __init__(self, name, url, requirement, responsibility, salary_from=None, salary_to=None, salary_currency=None):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility

    def max_pay(self):
        return self.salary_from


hh_api = HeadHunter_API()
loading(hh_api)
var = hh_api.data

jobs = []

for item in var["items"]:
    name = item["name"]
    url = item["alternate_url"]
    requirement = item["snippet"]["requirement"]
    responsibility = item["snippet"]["responsibility"]

    if "salary" in item and item["salary"]:
        salary_from = item["salary"]["from"]
        salary_to = item["salary"]["to"]
        salary_currency = item["salary"]["currency"]
    else:
        salary_from = None
        salary_to = None
        salary_currency = None

    job = JobOffer(name, url, requirement, responsibility, salary_from, salary_to, salary_currency)
    jobs.append(job)

jobs_with_salary = []

def maximum():
    for job in jobs:
        if job.salary_from is not None:
            jobs_with_salary.append(job)

    if jobs_with_salary:
        max_job = max(jobs_with_salary, key=lambda mj: mj.max_pay())
        print(f"The job with the highest salary is: {max_job.name} - {max_job.salary_from} {max_job.salary_currency}")
    else:
        print("No jobs with salary information found.")
maximum()