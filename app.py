from flask import *
import database_services.RDBService as d_service
from flask_cors import CORS
import json

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.cat_resource import CatResource
from application_services.BreederResource.breeder_service import BreederResource


app = Flask(__name__)
CORS(app)

@app.route('/json')
def json():
    return render_template('json.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")


@app.route('/')
def hello_world():
    return render_template('index.html')

# request.form is for retrieving POST request data from html form
# requeust.args is for retrieving GET request data from html form


@app.route('/breeders', methods=['GET', 'POST', 'PUT', 'DELETE'])
def breeders():
    if request.method == 'GET':
        res = BreederResource.get_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    if request.method == 'POST':
        res = BreederResource.post_breeder(request.form.get('breeder_id'), request.form.get('name'), request.form.get('organization'), request.form.get('phone'), request.form.get('email'), request.form.get('address'), request.form.get('website'), request.form.get('rating'))
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp

@app.route('/breeders/rating', methods=['GET', 'POST', 'PUT', 'DELETE'])
def breede_rating():
    if request.method == 'GET':
        breeder_id = request.args.get('bid', default = '1', type = str)
        res = BreederResource.get_breeder_rating(breeder_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp


@app.route('/cats', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cats():
    if request.method == 'GET':
        res = BreederResource.get_by_template(None)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
        return rsp
    if request.method == 'POST':
        res = CatResource.post_cat(request.form.get('cat_id'), request.form.get('race'), request.form.get('color'), request.form.get('dob'), request.form.get('father'), request.form.get('mother'), request.form.get('breeder'))
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
