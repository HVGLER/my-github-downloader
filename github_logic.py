# github_logic.py
import requests

def fetch_repos(username, token=""):
    headers = {"Authorization": f"token {token}"} if token else {}
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"API 错误: {response.status_code} - {response.text}")
        data = response.json()
        if not data:
            break
        repos.extend([repo["name"] for repo in data])
        if len(data) < 100:
            break
        page += 1
    return repos