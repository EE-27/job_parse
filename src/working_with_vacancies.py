from load_api import *
import json
from abc import ABC, abstractmethod
import re


class JobDataHandler_abs(ABC):
    """
    Abstract base class for handling job data, providing methods for adding, reading, and filtering jobs.
    """
    @abstractmethod
    def add_job(self, job):
        """
        Add a job to the data storage.

        Args: job (JobOffer): The job to be added.

        Returns: None
        """
        pass

    @abstractmethod
    def read_jobs(self):
        """
        Read and retrieve all jobs from the data storage.

        Returns: list: A list of job data in JSON format.
        """
        pass

    @abstractmethod
    def filter_jobs_salary(self, json_data, salary_from, salary_to):
        """
        Filter jobs based on salary range.

        Args:
            json_data (list): List of job data in JSON format.
            salary_from (int): Minimum salary value.
            salary_to (int): Maximum salary value.

        Returns: list: A list of filtered job data in JSON format.
        """
        pass


class Json_JobDataHandler(JobDataHandler_abs):
    """
    Class for handling job data in JSON format.
    """
    def __init__(self, file_path):
        """
        Initialize the Json_JobDataHandler.

        Args: file_path (str): The file path where job data will be stored.
        """
        self.file_path = file_path

    def add_job(self, job):
        """
        Add a job to the JSON data storage.

        Args: job (JobOffer): The job to be added.

        Returns: None
        """
        with open(self.file_path, "a", encoding='utf-8') as file:
            #  json.dump(job, file, ensure_ascii=False)
            json.dump(job.__dict__, file, ensure_ascii=False)
            file.write('\n')

    def read_jobs(self):
        """
        Read and retrieve all jobs from the JSON data storage.

        Returns: list: A list of job data in JSON format.
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            self.jobs_in_json = []
            for line in file:
                one_job = json.loads(line)
                self.jobs_in_json.append(one_job)

            return self.jobs_in_json

    def filter_jobs_salary(self, json_data, salary_from, salary_to):
        """
        Filter jobs based on salary range.

        Args:
            json_data (list): List of job data in JSON format.
            salary_from (int): Minimum salary value.
            salary_to (int): Maximum salary value.

        Returns: list: A list of filtered job data in JSON format.
        """
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
    """
    Class representing a job offer.
    """

    def __init__(self, name, job_id, url, requirement, responsibility, salary_from=None, salary_to=None,
                 salary_currency=None):
        """
        Initialize a JobOffer instance.

        Args:
            name (str): The name or title of the job.
            job_id (int): The unique identifier of the job.
            url (str): The URL to the job posting.
            requirement (str): The job requirements.
            responsibility (str): The job responsibilities.
            salary_from (int, optional): The minimum salary offered by the job. Defaults to None.
            salary_to (int, optional): The maximum salary offered by the job. Defaults to None.
            salary_currency (str, optional): The currency of the salary. Defaults to None.
        """
        self.job_id = job_id
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        self.url = url
        self.requirement = requirement
        self.responsibility = responsibility

    @staticmethod
    def max_pay(jobs):
        """
        Get the job with the highest salary from a list of jobs.

        Args: jobs (list): List of JobOffer objects.

        Returns: str: A message indicating the job with the highest salary.
        """
        #  jobs_with_salary = [job for job in jobs if job.salary_from is not None]
        jobs_with_salary = []
        for job in jobs:
            if job.salary_from is not None:
                jobs_with_salary.append(job)

        if jobs_with_salary:
            max_job = max(jobs_with_salary, key=lambda job: job.salary_from)
            return (
                f"The job with the highest salary is: {max_job.name};{max_job.job_id} - {max_job.salary_from} {max_job.salary_currency}"
            )
        else:
            return "No jobs with salary information found."

    def __str__(self):
        job_info = f"Job ID: {self.job_id}\nName: {self.name}\nURL: {self.url}\n"
        salary_info = f"Salary: {self.salary_from} {self.salary_currency}" if self.salary_from else ("Salary: Not "
                                                                                                     "specified")
        # requirement_info = f"Requirements: {self.requirement}\n"
        # responsibility_info = f"Responsibilities: {self.responsibility}\n"

        return f"{job_info}{salary_info}\n"  # {requirement_info}{responsibility_info}"


# "менеджер", "повар", "программист", "Курьер",
keyword = "Курьер"

hh_api = HeadHunter_API(keyword)
sj_api = SuperJob_API(keyword)

loading(hh_api)
loading(sj_api)

data_sj = sj_api.data
data_hh = hh_api.data

jobs = []


def job_filling_sj(data_sj):
    """
    Fill the 'jobs' list with job data from SuperJob API response.

    Args: data_sj (dict): SuperJob API response data.

    Returns: list: List of JobOffer objects.
    """
    for object in data_sj["objects"]:
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
    return jobs


def job_filling_hh(data_hh):
    """
    Fill the 'jobs' list with job data from HeadHunter API response.

    Args: data_hh (dict): HeadHunter API response data.

    Returns: list: List of JobOffer objects.
    """
    for item in data_hh["items"]:
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
    return jobs


# job_filling_hh(data_hh)
# job_filling_sj(data_sj)

jobs_with_salary = []

job_handle = Json_JobDataHandler("jobs.json")


# # tohle maže vše v jobs.json, takže nemusím řešit duplicity
# with open('jobs.json', 'w', encoding='utf-8'):
#     pass

# # adding jobs into json
# for job in jobs:
#     job_handle.add_job(job)

# # reading jobs in json
# (job_handle.read_jobs())

# filtering jobs based of min/max salary
# (job_handle.filter_jobs_salary(job_handle.jobs_in_json,100000,9999999))
# for filtered_job in job_handle.filtered:
#     name = filtered_job["name"]
#     min_salary = filtered_job["salary_from"]
#     max_salary = filtered_job["salary_to"]
#     currency = filtered_job["salary_currency"]
#     if max_salary is None:
#         print(f"{name}: {min_salary} {currency} ")
#     else:
#         print(f"{name}: {min_salary}-{max_salary} {currency} ")

def maximum():
    for job in jobs:
        if job.salary_from is not None:
            jobs_with_salary.append(job)

    # if jobs_with_salary:
    #     max_job = max(jobs_with_salary, key=lambda mj: mj.max_pay())
    #     print(
    #         f"The job with the highest salary is: {max_job.name};{max_job.job_id} - {max_job.salary_from} {max_job.salary_currency}")
    # else:
    #     print("No jobs with salary information found.")


###
#  print(JobOffer.max_pay(jobs))
