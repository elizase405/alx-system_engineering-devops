#!/usr/bin/python3
"""
Use https://jsonplaceholder.typicode.com/ API to get data
about a certain employee
"""

import requests
import sys

if __name__ == "__main__":
    uri = "https://jsonplaceholder.typicode.com"
    emp_id = int(sys.argv[1])
    total_todos = 0
    completed_todos = 0
    emp_tasks = []

    user = requests.get(f"{uri}/users/{emp_id}").json()
    emp_name = user.get("name")

    todos = requests.get(f"{uri}/todos").json()
    for todo in todos:
        userId = todo.get("userId")
        if userId == emp_id:
            total_todos += 1
        if userId == emp_id and todo.get("completed"):
            completed_todos += 1
            title = todo.get("title")
            emp_tasks.append(title)

    print("Employee {} is done with tasks({}/{}):"
          .format(emp_name, completed_todos, total_todos))

    for task in emp_tasks:
        print("\t {}".format(task))
