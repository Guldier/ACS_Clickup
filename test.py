import requests
import json

# EGB
# list_id = "900500335607"

# LWL
list_id = "900500295661"

# AILT
# list_id = "212634037"

# AIBK
# list_id = "900500003302"


url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

query = {
    "archive": "false",
    "include_closed": "true",
    'page': 0
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "pk_36351215_U4VR22QCX5FGX9622Y3WYUNBGRWVOO4E"
}

response = requests.get(url, headers=headers, params=query)

data = response.json()
d = data['tasks']

print(len(d))

lista = []
wo = []
for i in d:
    wo = {}
    lista.append(i['name'])
    custom = i['custom_fields']
    wo = custom[23]
    for k, v in wo.items():
        if k == 'value':
            print(v)
        if k == 'id':
            print(v)

print(sorted(lista))
print(len(lista))
print(wo)
