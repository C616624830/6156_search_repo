
import os

# This is a bad place for this import
import pymysql


def get_context(key):
    """
    Get all paths which subscriped SNS message
    :return: a list of string
    """
    subscriptions = os.environ.get("SUBSCRIPTIONS", None)

    if subscriptions is None:
        dic = {
            "SUBSCRIPTIONS": ["/breeders"]
        }
        return dic[key]
    return subscriptions


def get_db_info():
    """
    This is crappy code.

    :return: A dictionary with connect info for MySQL
    """
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)


    # print(db_host)

    # db_host = "searhbase.coy0xnvkfahm.us-east-2.rds.amazonaws.com"
    # db_user = "admin"
    # db_password = "12345678"

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
            "password": "Leon123456",
            "cursorclass": pymysql.cursors.DictCursor
        }


    return db_info


