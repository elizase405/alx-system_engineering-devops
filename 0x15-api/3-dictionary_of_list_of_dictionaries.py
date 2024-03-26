#!/usr/bin/python3
"""
Use https://jsonplaceholder.typicode.com/ API to get data
about a certain employee
"""

import json
import requests

if __name__ == "__main__":
    uri = "https://jsonplaceholder.typicode.com"
    users_info = {}
    file_name = "todo_all_employees.json"

    users = requests.get(f"{uri}/users").json()
    todos = requests.get(f"{uri}/todos").json()
    for user in users:
        user_id = user.get("id")
        user_info = []
        for todo in todos:
            userId = todo.get("userId")
            user_data = {}
            if user_id == userId:
                user_data["username"] = user.get("username")
                user_data["task"] = todo.get("title")
                user_data["completed"] = todo.get("completed")
            if user_data != {}:
                user_info.append(user_data)
        users_info[user_id] = user_info

    with open(file_name, "w") as json_file:
        json.dump(users_info, json_file)
