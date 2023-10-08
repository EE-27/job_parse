from working_with_vacancies import *

# working with user


class PickApi:

    def __init__(self):


        job_handle = Json_JobDataHandler("jobs.json")
        with open('jobs.json', 'w', encoding='utf-8'):
            pass

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



# class PickTopJobs(PickApi):
#     def __init__(self):
#         super().__init__()
#         jobs_with_salary = []
#         for job in jobs:
#             if job.salary_from is not None:
#                 jobs_with_salary.append(job)
#         while True:
#             try:
#                 print("Filtering job by salary, if job does not have salary, its omitted.")
#                 top_n = int(input("How many top jobs do you want to see (filtered by salary)? "))
#                 break
#             except ValueError:
#                 print("Invalid input. Please enter a valid number.")
#         sorted_jobs = sorted(jobs_with_salary, key=lambda job: job.salary_from, reverse=True)
#         top_jobs = sorted_jobs[:top_n]
#         print(f"Top-{top_n} jobs:")
#         for i, job in enumerate(top_jobs):
#             print(f"{i + 1}. {job.name};#{job.job_id} - {job.salary_from} {job.salary_currency}")


class PickTop_N_Jobs:
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

class WriteJob:

    def __init__(self):
        with open("jobs.json", "r", encoding='utf-8') as file:
            print("Write 'job_id' of a job you want to add")
            user_job_id = input()
            for line in file:
                try:
                    user_job_id = int(user_job_id)
                except ValueError:
                    print("Invalid input. Please enter a valid job_id (a number).")
                    continue

                line_data = json.loads(line)

                if line_data.get("job_id") == user_job_id:
                    with open("user.txt", "a", encoding='utf-8') as my_file:
                        my_file.write(str(line_data))
                        my_file.write("\n")
                    break
            else:
                print(f"No job found with job_id {user_job_id} in the JSON file.")

class DeleteJob:
    def __init__(self):
        file_name = "user.txt"
        with open(file_name, "r", encoding='utf-8') as my_file:
            print("You have saved this job offers: ")
            for line in my_file:
                parts = line.split(",")
                job_id = parts[0][-8:]
                job_name = parts[1][9:]

                print(f"Job_id: {job_id} - {job_name}")
        print("Which job do you want to erase? Write only job_id.")
        user_job_id = input("job_id: ")

        with open(file_name, "r", encoding="utf-8") as my_file:
            lines = my_file.readlines()
            found = False
            filtered_lines = []

            for line in lines:
                parts = line.split(",")
                job_id = parts[0][-8:]

                if job_id == str(user_job_id):
                    found = True

                else:
                    filtered_lines.append(line)

        with open(file_name, "w", encoding="utf-8") as my_file:
            my_file.writelines(filtered_lines)

        if found:
            print(f"Line with job_id {user_job_id} deleted from the file.")
        else:
            print(f"No line found with job_id {user_job_id}.")


# "менеджер", "повар", "программист", "Курьер",
class User:
    def __init__(self):
        # Select site and proffesion
        print("Hello, from which site would you like to see the vacancies?")
        print("Press '1' for HeadHunter.")
        print("Press '2' for SuperJob.")
        print("Press 'Enter' if you want both.")

        PickApi()

        # Select how many top jobs to show
        print("Do you want to see top_'N' jobs, filtered by salary?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_topn = input()
        if user_pick_topn == "1":
            PickTop_N_Jobs()

        # Select if you want to see the highest paying job
        print("Do you want to see the highest paying job?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_max = input()
        if user_pick_max == "1":
            print(JobOffer.max_pay(jobs))

        # Watch all jobs without filter
        print("Do you want to see all the jobs without filter? (max 40)")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_list = input()
        if user_pick_list == "1":
            for job in jobs:
                print(job)

        # Write in your own file
        print("Do you want add job into your own file?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_write = input()
        if user_pick_write == "1":
            while True:
                WriteJob()
                print("Do you want to add another? Press '1' for 'yes'/ -anything else for 'no'.")
                user_pick_write = input()
                if user_pick_write != "1":
                    break


        # Delete in your own file
        print("Do you want delete job in your own file?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_delete = input()
        if user_pick_delete == "1":
            while True:
                DeleteJob()
                print("Do you want to delete another? Press '1' for 'yes'/ -anything else for 'no'.")
                user_pick_delete = input()
                if user_pick_delete != "1":
                    break
