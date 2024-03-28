#!/usr/bin/python3
"""
Use https://jsonplaceholder.typicode.com/ API to get data
about a certain employee
"""

import csv
import requests
import sys

if __name__ == "__main__":
    uri = "https://jsonplaceholder.typicode.com"
    emp_id = int(sys.argv[1])
    csv_file_path = f"{emp_id}.csv"
    datas = []

    user = requests.get(f"{uri}/users/{emp_id}").json()
    emp_name = user.get("username")

    todos = requests.get(f"{uri}/todos").json()
    for todo in todos:
        data = {}
        userId = todo.get("userId")
        if userId == emp_id:
            data["id"] = userId
            data["name"] = emp_name
            data["done"] = todo.get("completed")
            data["title"] = todo.get("title")

        if data != {}:
            datas.append(data)

    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=datas[0].keys(), quoting=csv.QUOTE_ALL)

        for data in datas:
            writer.writerow(data)
