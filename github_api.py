import requests
from collections import Counter
from cache import get_cache, set_cache


def get_github_data(username):
    cached = get_cache(f"username: {username}")
    if cached is not None:
        return cached
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
    except requests.exceptions.RequestException:
        return None
    if response.status_code == 200:
        data = response.json()
        set_cache(f"username: {username}", data)
        return data
    return None
    
def get_github_repos(username):
    cached = get_cache(f"repos: {username}")
    if cached is not None:
        return cached
    try:
        response = requests.get(f"https://api.github.com/users/{username}/repos", timeout=5)
    except requests.exceptions.RequestException:
        return None
    if response.status_code == 200:
        data = response.json()
        set_cache(f"repos: {username}", data)
        return data
    return None

def get_language_stats(repos):
    if repos is None:
        return None
    if not repos:
        return []
    
    cached = get_cache(f"language_stats: {repos}")
    if cached is not None:
        return cached
    languages = [repo.get("language") for repo in repos if repo.get("language") is not None]
    counter_languages = Counter(languages)
    result = counter_languages.most_common()
    set_cache(f"language_stats: {repos}", result)
    return result