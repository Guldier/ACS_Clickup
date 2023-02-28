import requests
import json

team_id = "24328424"
space_id = "42355988"
url = "https://api.clickup.com/api/v2/space/" + space_id + "/list"

query = {
    "archived": "false"
}

headers = {"Authorization": "pk_36351215_U4VR22QCX5FGX9622Y3WYUNBGRWVOO4E"}

response = requests.get(url, headers=headers, params=query)

data = response.json()
print(json.dumps(data, indent=4))
