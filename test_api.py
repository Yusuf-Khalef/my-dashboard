import requests

response = requests.get("https://api.github.com/users/Yusuf-Khalef")
data = response.json()

if response.status_code == 200:
    data = response.json()
    print("Followers:", data["followers"])
elif response.status_code == 404:
    print("That user doesn't exist.")
else:
    print("Something went wrong. Status code:", response.status_code)