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


def select_specific_column(db_schema, table_name, column_name, targeted_row, value):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select " + column_name +" from " + db_schema + "." + table_name + " where " + \
        targeted_row + " = " + value
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()
    # print("res: ")
    # print(res)
    # print("..")
    return res


def insert_by_template(db_schema, table_name, template, field_list):

    conn = _get_db_connection()
    cur = conn.cursor()

    clause,args = _insert_clause_args(template)

    sql = "INSERT INTO " + db_schema + "." + table_name + clause

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql, args=args)
    conn.commit()
    res = cur.fetchall()

    conn.close()

    return res


def _insert_clause_args(template):
    terms = []
    args = []
    params = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(k)
            params.append("%s")
            args.append(v)

        clause = " (" + ", ".join(terms) + ") VALUES (" + ", ".join(params) + ")"

    # print(clause)
    # print(args)
    return clause, args


def delete_by_id(db_schema, table_name, id, field_list):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = f"delete from {db_schema}.{table_name} where id = {id}"

    res = cur.execute(sql)
    conn.commit()
    res = cur.fetchall()

    conn.close()

    return res


def update_by_id_template(db_schema, table_name, id, template, field_list):

    conn = _get_db_connection()
    cur = conn.cursor()

    clause,args = _update_clause_args(id, template)

    sql = "UPDATE " + db_schema + "." + table_name + " " + clause

    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql, args=args)
    conn.commit()
    res = cur.fetchall()

    conn.close()

    return res


def _update_clause_args(id, template):
    terms = []
    args = []
    clause = None

    if template is None or template == {}:
        clause = ""
        args = None
    else:
        for k, v in template.items():
            terms.append(f"{k}=%s")
            args.append(v)

    clause = "SET " + ", ".join(terms) + f" where id = {id}"

    # print(clause)
    # print(args)
    return clause, args


def select_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def select_by_template(db_schema, table_name, template, field_list):

    limit = template.get('limit');
    offset = template.get('offset');

    template = {k: v for k, v in template.items() if k!= 'limit' and k!='offset'}
    wc,args = _where_clause_args(template)


    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " " + wc + " limit " + limit + " offset " + offset
    res = cur.execute(sql, args=args)
    res = cur.fetchall()
    print(sql)
    # print(res)
    conn.close()

    return res


def _where_clause_args(template):

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
