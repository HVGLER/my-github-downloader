# downloader.py
import requests

def download_repo_zip(username, repo, save_path):
    url = f"https://github.com/{username}/{repo}/archive/refs/heads/main.zip"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)