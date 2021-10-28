from flask import *
import database_services.RDBService as d_service
from flask_cors import CORS
import json
import pymysql

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.CatResource.cat_service import CatResource
from application_services.BreederResource.breeder_service import BreederResource


app = Flask(__name__)
CORS(app)



@app.route('/')
def get_index():
    return render_template('index.html')


@app.route('/add_cat')
def add_cat_page():
    return render_template('add_cat.html')

@app.route('/delete_cat')
def delete_cat_page():
    return render_template('delete_cat.html')

@app.route('/search_cat')
def search_cat_page():
    return render_template('search_cat.html')

@app.route('/add_breeder')
def add_breeder_page():
    return render_template('add_breeder.html')

@app.route('/search_breeder')
def search_breeder_page():
    return render_template('search_breeder.html')

@app.route('/view_breeder_rating')
def view_breeder_rating_page():
    return render_template('view_breeder_rating.html')

# request.form is for retrieving POST request data from html form
# requeust.args is for retrieving GET request data from html form


@app.route('/breeders', methods=['GET', 'POST', 'PUT', 'DELETE'])
def breeders():
####GET START
    if request.method == 'GET':
        template = request.args.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''

        res = None
        try:
            res = BreederResource.get_breeders(template)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
####GET START


####POST START
    if request.method == 'POST':
        # print(request.form.to_dict())
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''
        id = template.get('id', None)
        print("id", id)
        if not id.isdigit() or int(id) <= 0:
            rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                           content_type="application/json")
            return rsp
        elif BreederResource.check_breeder_id_exist(id):
            rsp = Response(json.dumps("id already exist", default=str), status=422,
                           content_type="application/json")
            return rsp

        res = None
        try:
            res = BreederResource.post_breeder(template)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        rsp.headers['location'] = '/breeders'
        return rsp
####POST END

####DELETE START
    if request.method == 'DELETE':
        template = request.args.to_dict()
        # print(template)
        id = template.get('id', None)
        # print("id", id)
        if not id.isdigit() or int(id) <= 0:
            rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                           content_type="application/json")
            return rsp
        elif not BreederResource.check_breeder_id_exist(id):
            rsp = Response(json.dumps("id does not exist", default=str), status=422,
                           content_type="application/json")
            return rsp

        res = None
        try:
            res = BreederResource.delete_breeder(id)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500, content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=204, content_type="application/json")
        return rsp
####DELETE END

####PUT START
    if request.method == 'PUT':
        template = request.args.to_dict()
        id = template.get('id', None)
        # print('id:', id)

        if not id.isdigit() or int(id) <= 0:
            rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                           content_type="application/json")
            return rsp
        elif not BreederResource.check_breeder_id_exist(id):
            rsp = Response(json.dumps("id does not exist", default=str), status=422,
                           content_type="application/json")
            return rsp

        template = {k: v for k, v in template.items() if
                    v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''
        # print('template:', template)

        res = None
        try:
            res = BreederResource.put_breeder(id, template)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/breeders/rating', methods=['GET', 'POST', 'PUT', 'DELETE'])
def breeder_rating():
    if request.method == 'GET':
        breeder_id = request.args.get('bid', default = '1', type = str)
        res = BreederResource.get_breeder_rating(breeder_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/cats', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cats():
####GET START
    if request.method == 'GET':
        template = request.args.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''

        res = None
        try:
            res = CatResource.get_cats(template)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
####GET START


####POST START
    if request.method == 'POST':
        # print(request.form.to_dict())
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''
        for k,v in template.items():
            if k == 'id':
                if not v.isdigit() or int(v) <= 0:
                    rsp = Response(json.dumps("id in wrong format", default=str), status=400, content_type="application/json")
                    return rsp
                elif CatResource.check_cat_id_exist(v):
                    rsp = Response(json.dumps("id already exist", default=str), status=422,
                                   content_type="application/json")
                    return rsp

            if k == 'father':
                if not v.isdigit() or int(v) <= 0:
                    rsp = Response(json.dumps("father id in wrong format", default=str), status=400, content_type="application/json")
                    return rsp
                elif not CatResource.check_cat_id_exist(v):
                    rsp = Response(json.dumps("father id does not exist", default=str), status=422,
                                   content_type="application/json")
                    return rsp

            if k == 'mother':
                if not v.isdigit() or int(v) <= 0:
                    rsp = Response(json.dumps("mother id in wrong format", default=str), status=400, content_type="application/json")
                    return rsp
                elif not CatResource.check_cat_id_exist(v):
                    rsp = Response(json.dumps("mother id does not exist", default=str), status=422,
                                   content_type="application/json")
                    return rsp

            if k == 'breeder':
                if not v.isdigit() or int(v) <= 0:
                    rsp = Response(json.dumps("breeder id in wrong format", default=str), status=400, content_type="application/json")
                    return rsp
                elif not BreederResource.check_breeder_id_exist(v):
                    rsp = Response(json.dumps("breeder id does not exist", default=str), status=422,
                                   content_type="application/json")
                    return rsp

        res = None
        try:
            res = CatResource.post_cat(template)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
        rsp.headers['location'] = '/cats'
        return rsp
####POST END

####DELETE START
    if request.method == 'DELETE':
        template = request.args.to_dict()
        print(template)
        id = template.get('id', None)
        print("id", id)
        if not id.isdigit() or int(id) <= 0:
            rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                           content_type="application/json")
            return rsp
        elif not CatResource.check_cat_id_exist(id):
            rsp = Response(json.dumps("id does not exist", default=str), status=422,
                           content_type="application/json")
            return rsp

        res = None
        try:
            res = CatResource.delete_cat(id)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500, content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=204, content_type="application/json")
        return rsp
####DELETE END

####PUT START
    if request.method == 'PUT':
        template = request.args.to_dict()
        id = template.get('id', None)
        # print('id:', id)

        if not id.isdigit() or int(id) <= 0:
            rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                           content_type="application/json")
            return rsp
        elif not CatResource.check_cat_id_exist(id):
            rsp = Response(json.dumps("id does not exist", default=str), status=422,
                           content_type="application/json")
            return rsp

        template = {k: v for k, v in template.items() if
                    v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''
        # print('template:', template)

        res = None
        try:
            res = CatResource.put_cat(id, template)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/cats/breeder/<cid>')
def breeder_of_cat(cid):
    res = CatResource.get_breeder_id(cid)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")



# @app.route('/imdb/artists/<prefix>')
# def get_artists_by_prefix(prefix):
#     res = IMDBArtistResource.get_by_name_prefix(prefix)
#     rsp = Response(json.dumps(res), status=200, content_type="application/json")
#     return rsp

# @app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
# def get_by_prefix(db_schema, table_name, column_name, prefix):
#     res = d_service.get_by_prefix(db_schema, table_name, column_name, prefix)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
