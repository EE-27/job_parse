from load_api import *
import json
from abc import ABC, abstractmethod
import re


class JobDataHandler_abs(ABC):
    @abstractmethod
    def add_job(self, job):
        pass

    def read_jobs(self):
        pass

    def filter_jobs_salary(self, json_data, salary_from, salary_to):
        pass


class Json_JobDataHandler(JobDataHandler_abs):
    def __init__(self, file_path):
        self.file_path = file_path

    def add_job(self, job):
        with open(self.file_path, "a", encoding='utf-8') as file:
            json.dump(job.__dict__, file, ensure_ascii=False)
            file.write('\n')

    def read_jobs(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.jobs_in_json = []
            for line in file:
                one_job = json.loads(line)
                self.jobs_in_json.append(one_job)

            return  self.jobs_in_json

    def filter_jobs_salary(self, json_data, salary_from, salary_to):
        self.filtered = []
        for job in json_data:
            if dict(job).get("salary_from") == None:
                from_salary = 0
            else:
                from_salary = dict(job).get("salary_from")
            if dict(job).get("salary_to") == None:
                to_salary = 0
            else:
                to_salary = dict(job).get("salary_to")

            if from_salary >= salary_from and to_salary <= salary_to:
                self.filtered.append(job)
        return self.filtered


class JobOffer:

    def __init__(self, name, job_id, url, requirement, responsibility, salary_from=None, salary_to=None,
                 salary_currency=None):
        self.job_id = job_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility

    def max_pay(self):
        return self.salary_from


# "менеджер", "повар", "программист", "Курьер",
keyword = "Курьер"

hh_api = HeadHunter_API(keyword)
sj_api = SuperJob_API(keyword)

loading(hh_api)
loading(sj_api)

jobs = []

for object in sj_api.data["objects"]:
    job_id = object["id"]
    name = object["profession"]
    url = object["link"]
    requirement = object["candidat"]
    responsibility = object["vacancyRichText"]

    # removing html tags
    html_tags_pattern = r'<.*?>'
    responsibility = re.sub(html_tags_pattern, '', responsibility)

    salary_from = object["payment_from"]
    salary_to = object["payment_to"]
    salary_currency = object["currency"]

    job = JobOffer(name, int(job_id), url, requirement, responsibility, salary_from, salary_to,
                   str(salary_currency).upper())
    jobs.append(job)

for item in hh_api.data["items"]:
    job_id = item["id"]
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

    job = JobOffer(name, int(job_id), url, requirement, responsibility, salary_from, salary_to, salary_currency)
    jobs.append(job)

jobs_with_salary = []

job_handle = Json_JobDataHandler("jobs.json")

#  tohle maže vše v jobs.json, takže nemusím řešit duplicity
with open('jobs.json', 'w', encoding='utf-8'):
    pass

# adding jobs into json
for job in jobs:
    job_handle.add_job(job)

# reading jobs in json
(job_handle.read_jobs())

# filtering jobs based of min/max salary
(job_handle.filter_jobs_salary(job_handle.jobs_in_json,1000,9999999))
for jab in job_handle.filtered:
    name = jab["name"]
    sl_fr = jab["salary_from"]
    sl_to = jab["salary_to"]
    cur = jab["salary_currency"]
    if sl_to == None:
        print(f"{name}: {sl_fr} {cur} ")
    else:
        print(f"{name}: {sl_fr}-{sl_to} {cur} ")

def maximum():
    for job in jobs:
        if job.salary_from is not None:
            jobs_with_salary.append(job)

    if jobs_with_salary:
        max_job = max(jobs_with_salary, key=lambda mj: mj.max_pay())
        print(
            f"The job with the highest salary is: {max_job.name};{max_job.job_id} - {max_job.salary_from} {max_job.salary_currency}")
    else:
        print("No jobs with salary information found.")

###
