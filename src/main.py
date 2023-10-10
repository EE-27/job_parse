from working_with_vacancies import *


# working with user


class PickApi:
    """
    Class for handling user interactions related to selecting and loading job data from APIs.
    """

    def __init__(self):
        """
        Initializes the PickApi class and allows the user to choose an API source and a profession to search for.
        """

        job_handle = Json_JobDataHandler("jobs.json")
        with open('jobs.json', 'w', encoding='utf-8'):
            pass

        api = input()
        if api == "1":
            print("---")
            print("You chose HeadHunter!")
            profession = input("Which profession are you looking for?: ")
            hh_api = HeadHunter_API(profession)
            loading(hh_api)
            job_filling_hh(hh_api.data)
            for job in jobs:
                job_handle.add_job(job)


        elif api == "2":
            print("---")
            print("You chose SuperJob!")
            profession = input("Which profession are you looking for?: ")
            sj_api = SuperJob_API(profession)
            loading(sj_api)
            job_filling_sj(sj_api.data)
            for job in jobs:
                job_handle.add_job(job)


        else:
            print("---")
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

class PickTop_N_Jobs:
    """
    Class for filtering and displaying the top N jobs based on salary.
    """
    def __init__(self):
        """
        Initializes the PickTop_N_Jobs class and allows the user to specify the number of top jobs to display.
        """
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
    """
    Class for writing a selected job to the user's own file.
    """

    def __init__(self):
        """
        Initializes the WriteJob class and allows the user to select a job to add to their file.
        """
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
    """
    Class for deleting a job from the user's own file.
    """
    def __init__(self):
        """
        Initializes the DeleteJob class and allows the user to select a job to delete from their file.
        """
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


class CompareJob:
    """
    Class for comparing two job offers that the user has saved.
    """
    def __init__(self):
        """
        Initializes the CompareJob class and allows the user to select two jobs to compare based on salary.
        """
        class Compare:
            def __init__(self, job_id, job_name, job_salary_from, job_salary_to, job_currency):
                self.job_id = job_id
                self.job_name = job_name
                self.job_salary_from = job_salary_from
                self.job_salary_to = job_salary_to
                self.job_currency = job_currency

            def compare(self, other):
                if self.job_currency != other.job_currency:
                    return f"Jobs can't be compared, different currency."
                elif self.job_salary_from == "None" or other.job_salary_from == "None" or self.job_salary_from == "0" or other.job_salary_from == "0":
                    return f"Vacancies cannot be compared, salary not specified."
                elif self.job_salary_to == "None" or other.job_salary_to == "None" or self.job_salary_to == "0" or other.job_salary_to == "0":
                    return f"Vacancies cannot be compared, salary not specified."

                if int(self.job_salary_from) > int(other.job_salary_from) or int(self.job_salary_to) > int(
                        other.job_salary_to):
                    return f'Job offer {self.job_name} has bigger salary than {other.job_name}.\nJob offer {self.job_name} offers a salary from {self.job_salary_from} to {self.job_salary_to} in {self.job_currency}'

                elif int(self.job_salary_from) < int(other.job_salary_from) or int(self.job_salary_to) < int(
                        other.job_salary_to):
                    return f'Job offer {other.job_name} has a salary higher than {self.job_name}.\nJob offer {other.job_name} offers a salary from {other.job_salary_from} to {other.job_salary_to} in {other.job_currency}'

        file_name = "user.txt"
        with open(file_name, "r", encoding='utf-8') as my_file:
            print("You have saved this job offers: ")
            for line in my_file:
                parts = line.split(",")
                job_id = parts[0][-8:]
                job_name = parts[1][9:]

                print(f"Job_id: {job_id} - {job_name}")
        print("Which jobs do you want to compare? Write only job_id.")
        user_job_id_1 = input("1st job_id: ")
        user_job_id_2 = input("2nd job_id: ")
        with open(file_name, "r", encoding="utf-8") as my_file:
            lines = my_file.readlines()
            for line in lines:
                if str(user_job_id_1) in line:
                    list_line = line.split(",")

                    line_id = list_line[0][-8:]
                    line_name = list_line[1][9:]
                    line_salary_from = list_line[2][16:]
                    line_salary_to = list_line[3][14:]
                    line_salary_currency = list_line[4][-5:]

                    job_1 = Compare(line_id, line_name, line_salary_from, line_salary_to, line_salary_currency)
            for line in lines:
                if str(user_job_id_2) in line:
                    list_line = line.split(",")

                    line_id = list_line[0][-8:]
                    line_name = list_line[1][9:]
                    line_salary_from = list_line[2][16:]
                    line_salary_to = list_line[3][14:]
                    line_salary_currency = list_line[4][-5:]

                    job_2 = Compare(line_id, line_name, line_salary_from, line_salary_to, line_salary_currency)

        print(job_1.compare(job_2))


# "менеджер", "повар", "программист", "Курьер",
class User:
    """
    Class for managing user interactions with the job-related functionality.
    """
    def __init__(self):
        """
        Initializes the User class and guides the user through various job-related tasks.
        """
        # Select site and proffesion

        print("Press '1' for HeadHunter.")
        print("Press '2' for SuperJob.")
        print("Press 'Enter' if you want both.")

        PickApi()

        # Select how many top jobs to show
        print("---")
        print("Do you want to see top_'N' jobs, filtered by salary?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_topn = input()
        if user_pick_topn == "1":
            PickTop_N_Jobs()

        # Select if you want to see the highest paying job
        print("---")
        print("Do you want to see the highest paying job?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_max = input()
        if user_pick_max == "1":
            print(JobOffer.max_pay(jobs))

        # Watch all jobs without filter
        print("---")
        print("Do you want to see all the jobs without filter? (max 40)")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_list = input()
        if user_pick_list == "1":
            for job in jobs:
                print(job)

        # Write in your own file
        print("---")
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
        print("---")
        print("Do you want delete job in your own file?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_delete = input()
        if user_pick_delete == "1":
            while True:
                DeleteJob()
                print("---")
                print("Do you want to delete another? Press '1' for 'yes'/ -anything else for 'no'.")
                user_pick_delete = input()
                if user_pick_delete != "1":
                    break

        # Compare two job offers that you have saved
        print("---")
        print("Do you want compare job in your own file?")
        print("Press '1' for 'yes'.")
        print("Press 'Enter' for 'no!. ")
        user_pick_compare = input()
        if user_pick_compare == "1":
            while True:
                CompareJob()
                print("---")
                print("Do you want to compare another? Press '1' for 'yes'/ -anything else for 'no'.")
                user_pick_compare = input()
                if user_pick_compare != "1":
                    break



