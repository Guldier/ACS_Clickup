import pyodbc
import requests
import json
import pandas


def NRC_check(wo_number, list_id, wo=None):
    print(wo_number)
    nrc_list_ACS = []
    nrc_list_clickup = []
    cr_list_clickup = []

    # Clickup API SELECT
    headers = {
        "Content-Type": "application/json",
        "Authorization": "pk_36351215_U4VR22QCX5FGX9622Y3WYUNBGRWVOO4E"
    }
    if wo is None:
        query = {
            "archived": "false",
            "include_closed": "true",
            "page": 0
        }
        query1 = {
            "archived": "false",
            "include_closed": "true",
            "page": 1
        }
    else:
        custom_fields = [{
            "field_id": "bd2d6466-77b2-4c61-86ad-8fcf75ea888b",
            "operator": "ANY",
            "value": wo
        }]

        stringpa = f"?=custom_fields={custom_fields}"
        print(stringpa.replace("'", '"'))
        query = {
            "archived": "false",
            "include_closed": "true",
            "page": 0,
            "custom_fields": stringpa
        }
        query1 = {
            "archived": "false",
            "include_closed": "true",
            "page": 1,
            "custom_fields": stringpa
        }

    # Clickup API POST
    query_post = {
        "custom_task_ids": "true",
        "team_id": "24328424"
    }

    url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"

    # SQL connection string
    cnxn = pyodbc.connect(
        driver='{SQL Server Native Client 11.0}',
        Server='ltsrvbr1',
        Database='ACS_LT',
        UID='TCManager_User',
        PWD='An@n@$12345',
        Trusted_Connection='no'
    )

    # Pobranie SQL listy zadan
    cursor = cnxn.cursor()
    cursor.execute(
        f"SELECT number FROM vw_mro_nrc WHERE wo_number = '{wo_number}' AND zone_id = 1435")

    # zamiana listy z ACS na liczby
    for row in cursor:
        for y in [x for x in row]:
            nrc_list_ACS.append(int(y))

    # Pobieranie z Clickupa listy tasków
    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    d = data['tasks']

    response1 = requests.get(url, headers=headers, params=query1)
    data1 = response1.json()
    d1 = data1['tasks']

    all_data_from_Clickup = d + d1

    # Zamiana listy tasków na numery
    for i in all_data_from_Clickup:
        custom_field = i['custom_fields']
        wo_i = custom_field[23]
        for k, v in wo_i.items():
            if k == 'value':
                if v == wo_number:
                    try:
                        item = i['name'].split("VI/")
                        nrc_list_clickup.append(int(item[1]))
                    except:
                        try:
                            item = i['name'].split("CR/")
                            cr_list_clickup.append(int(item[1]))
                        except:
                            pass

    # for i in d1:
    #     try:
    #         item = i['name'].split("VI/")
    #         nrc_list_clickup.append(int(item[1]))
    #     except:
    #         try:
    #             item = i['name'].split("CR/")
    #             cr_list_clickup.append(int(item[1]))
    #         except:
    #             pass

    print('ACS')
    print(sorted(nrc_list_ACS))
    print('NRC in Clickup')
    print(sorted(nrc_list_clickup))
    print('CR in Clickup')
    print(sorted(cr_list_clickup))
    # Porownanie obu list
    for nrc in nrc_list_ACS:
        if nrc in nrc_list_clickup:
            pass
        else:
            cursor1 = cnxn.cursor()
            cursor1.execute(
                f"SELECT [description] FROM vw_mro_nrc WHERE wo_number = '{wo_number}' AND zone_id = 1435 and number = {nrc}")

            for row in cursor1:
                payload = {
                    "name": f"VI/{nrc:03d}",
                    "custom_fields": [
                        {
                            "id": "156f285f-353d-4a0f-8d34-4c3513ba69c8",
                            "value": f"{row[0]}"
                        },
                        {
                            "id": "bd2d6466-77b2-4c61-86ad-8fcf75ea888b",
                            "value": f"{wo_number}"
                        }
                    ]
                }
                # response_post = requests.post(
                #     url, json=payload, headers=headers, params=query_post)
                print(nrc)
                # data_post = response_post.json()
                # print(json.dumps(data_post, indent=4))
                pass


# RYR
NRC_check("EGB - 14YR - HM 22/23", "900500335607")

# WZZ
NRC_check("HA-LWL/H-23-EOL-8C", "900500295661")
NRC_check("HA-LWL/H-23-EOL", "900500295661")
# HA-LVH
NRC_check("WP434113", "900500637698")
NRC_check("HA-LVH/L-28223 STP", "900500637698")

# DLH
NRC_check("AIBK/H-22-C5-CHECKS, AIBK/H-22-C5-DOCS", "900500003302")
NRC_check("AILT/H-22-C2-CHECKS, AILT/H-22-C2-DOCS &AILT/H-22-C2-ADD1", "212634037")
