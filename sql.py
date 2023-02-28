import pyodbc
cnxn = pyodbc.connect(
    driver='{SQL Server Native Client 11.0}',
    Server='ltsrvbr1',
    Database='ACS_LT',
    UID='TCManager_User',
    PWD='An@n@$12345',
    Trusted_Connection='no'
)

wo = "EGB - 14YR - HM 22/23"
cursor = cnxn.cursor()
cursor.execute(
    f"SELECT number FROM vw_mro_nrc WHERE wo_number = '{wo}' AND zone_id = 1435")

nrc_list = []
for row in cursor:

    for y in [x for x in row]:
        nrc_list.append(int(y))

print(nrc_list)
