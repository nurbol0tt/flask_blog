import mysql.connector

mydb = mysql.connector.connect(
    port="3308",
    user="root",
    passwd="Nuru_141592",
    auth_plugin='mysql_native_password',
    database='db'
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE flask_blog")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db)

