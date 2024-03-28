#!/usr/bin/python3
"""
Use https://jsonplaceholder.typicode.com/ API to get data
about a certain employee
"""

import json
import requests
import sys

if __name__ == "__main__":
    uri = "https://jsonplaceholder.typicode.com"
    users_info = {}
    user_data = []
    user_id = int(sys.argv[1])
    file_name = f"{user_id}.json"

    name = requests.get(f"{uri}/users/{user_id}").json().get("username")
    todos = requests.get(f"{uri}/todos").json()

    for todo in todos:
        userId = todo.get("userId")
        user_info = {}
        if user_id == userId:
            user_info["username"] = name
            user_info["task"] = todo.get("title")
            user_info["completed"] = todo.get("completed")
        if user_info != {}:
            user_data.append(user_info)
    users_info[user_id] = user_data

    with open(file_name, "w") as json_file:
        json.dump(users_info, json_file)
