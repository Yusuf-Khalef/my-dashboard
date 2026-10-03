from collections import Counter

import requests

response = requests.get("https://api.github.com/users/Yusuf-Khalef/repos")
data = response.json()

languages = [repo.get("language") for repo in data if repo.get("language") is not None]
print(languages)
counter_languages = Counter(languages)
print(counter_languages.most_common(1))
print(counter_languages.most_common())


'''if response.status_code == 200:
    data = response.json()
    print("Followers:", data["followers"])
elif response.status_code == 404:
    print("That user doesn't exist.")
else:
    print("Something went wrong. Status code:", response.status_code)'''