import mysql.connector as mc

connection = mc.connect(host="localhost", user="root", password="S@bri2019", db="smartsheets")
cursor = connection.cursor()
cursor.execute("SHOW TABLES")

tables = {'table': []}
for x in cursor:
    tables['table'].append(x[0])
print(tables)