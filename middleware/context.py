
import os
# This is a bad place for this import
import pymysql
import json


def get_context(key):
    """
    Get all paths which subscriped SNS message
    :return: a list of string
    """
    subscriptions = os.environ.get("SUBSCRIPTIONS", None)
    smarty_info = os.environ.get("SMARTY", None)

    if subscriptions is None:
        subscriptions = ["/breeders"]
    if smarty_info is None:
        smarty_info = {
            "auth_id": os.environ.get("AUTH_ID", None),
            "auth_token": os.environ.get("AUTH_TOKEN", None)
        }
    if key == "SMARTY":
        return smarty_info
    if key == "SUBSCRIPTIONS":
        return subscriptions



def get_db_info():
    """
    This is crappy code.

    :return: A dictionary with connect info for MySQL
    """
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)


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


