import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_db_connection():

    db_connect_info = context.get_db_info()

    logger.info("RDBService._get_db_connection:")
    logger.info("\t HOST = " + db_connect_info['host'])

    db_info = context.get_db_info()
    db_connection = pymysql.connect(
       **db_info
    )
    return db_connection


def get_specifc_column(db_schema, table_name, column_name, targeted_row, value):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select " + column_name +" from " + db_schema + "." + table_name + " where " + \
        targeted_row + " = " + value
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def add_cat(db_schema, table_name, catid, race, color, dob, fatherid, motherid, breederid):

    conn = _get_db_connection()
    cur = conn.cursor()


    if fatherid == "0" and motherid == "0":
        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " (id, race, color, dob, breeder) VALUES(" + \
              catid + ", " + "'" + race + "'" + ", " + "'" + color + "'" + ", " + "'" + dob + "'" + ", " + breederid + ")"

    elif fatherid == "0" and motherid != "0":
        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " (id, race, color, dob, mother, breeder) VALUES (" + \
              catid + ", " + "'" + race + "'" + ", " + "'" + color + "'" + ", " + "'" + dob + "'" + ", " + motherid + ", " + breederid + ")"

    elif fatherid != "0" and motherid == "0":
        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " (id, race, color, dob, father, breeder) VALUES (" + \
              catid + ", " + "'" + race + "'" + ", " + "'" + color + "'" + ", " + "'" + dob + "'" + ", " + fatherid +  ", " + breederid + ")"

    else:
        sql = "INSERT INTO " + db_schema + "." + table_name + \
              " (id, race, color, dob, father, mother, breeder) VALUES (" + \
              catid + ", " + "'" + race + "'" + ", " + "'" + color + "'" + ", " + "'" + dob + "'" + ", " + fatherid + ", " + motherid + ", " + breederid + ")"



    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    conn.commit()
    res = cur.fetchall()

    conn.close()

    return res


def add_breeder(db_schema, table_name, bid, name, organization, phone, email, address, website, rating):

    conn = _get_db_connection()
    cur = conn.cursor()


    sql = "INSERT INTO " + db_schema + "." + table_name + \
          " (id, name, organization, phone, email, address, website, rating) VALUES (" + \
          bid + ", " + "'" + name + "'" + ", " + "'" + organization + "'" + ", " + "'" + phone + "'" + ", " + "'" + email + "'" + ", " + "'" + address + "'" + ", " + "'" + website + "'" + ", " + rating + ")"

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    conn.commit()
    res = cur.fetchall()

    conn.close()

    return res

def get_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def _get_where_clause_args(template):

    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k,v in template.items():
            terms.append(k + "=%s")
            args.append(v)

        clause = " where " +  " AND ".join(terms)


    return clause, args


def find_by_template(db_schema, table_name, template, field_list):

    wc,args = _get_where_clause_args(template)

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc
    res = cur.execute(sql, args=args)
    res = cur.fetchall()

    conn.close()

    return res

