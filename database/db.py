import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="stock_management"
    )
