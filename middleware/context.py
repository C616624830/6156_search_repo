
import os

# This is a bad place for this import
import pymysql

def get_db_info():
    """
    This is crappy code.

    :return: A dictionary with connect info for MySQL
    """
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)

    # db_host = os.environ.get("DBHOST")
    # db_user = os.environ.get("DBUSER")
    # db_password = os.environ.get("DBPASSWORD")

    print(db_host)

    db_host = "searhbase.coy0xnvkfahm.us-east-2.rds.amazonaws.com"
    db_user = "admin"
    db_password = "12345678"

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "cursorclass": pymysql.cursors.DictCursor
        }

    else:
        db_info = {
            "host": "localhost",
            "user": "root",
            "password": "118871356",
            "cursorclass": pymysql.cursors.DictCursor
        }


    return db_info


