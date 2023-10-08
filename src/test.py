import json

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
        # print(f"Line data: {line_data}")
        # print(f"Job ID from JSON: {line_data.get('job_id')}")
        # print(f"User input job_id: {user_job_id}")

        if line_data.get("job_id") == user_job_id:
            with open("user.txt", "a", encoding='utf-8') as my_file:
                my_file.write(str(line_data))
                my_file.write("\n")
            break
    else:
        print(f"No job found with job_id {user_job_id} in the JSON file.")

