#!/usr/bin/python3

"""This is the subs module.
This module defines 1 function: def number_of_subscribers(subreddit)
"""
import requests


def number_of_subscribers(subreddit):
    """
        queries the Reddit API.
        Args:
            - subreddit (str) : The subreddit to be queried
        Raises: none
        Returns:
            the number of subscribers (not active users, total subscribers) for a given subreddit.
    

    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = { "User-Agent" : "MyApp/1.0" }
    res = requests.get(url, headers=headers,  allow_redirects=False) #.json()"""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    header = {"User-Agent": "Mozilla/5.0"}

    data = requests.get(url, headers=header, allow_redirects=False)
    print(data)
    if data.status_code == 200:
        subscribers = data.json().get("data").get("subscribers")
        return subscribers
    return 0
    return 1
#res.data.subscribers

