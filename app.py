from flask import *
from flask_cors import CORS
import json
import pymysql
import logging
from application_services.CatResource.cat_service import CatResource
from application_services.BreederResource.breeder_service import BreederResource
from address_services.smarty_address_service import SmartyAddressService
from flask_dance.contrib.google import make_google_blueprint, google
import middleware.simple_security as simple_security
import os
import dynamo.dynamodb as db
import copy
import uuid
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


import middleware.notification as notification

app = Flask(__name__)
CORS(app)

client_id = os.environ.get("CLIENT_ID", None)
client_secret = os.environ.get("CLIENT_SECRET", None)
app.secret_key = 'some secret'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"],
    offline = True
)
app.register_blueprint(blueprint, url_prefix="/login")

g_bp = app.blueprints.get("google")

# @app.before_request
# def before_request_func():
#     # print("flag0")
#     result_ok = simple_security.check_security(request, google, g_bp)
#     # print("flag3")
#     if not result_ok:
#         print('flag4')
#         # print(url_for('/'))
#         return redirect(url_for('google.login'))



@app.after_request
def after_request_func(response):
    notification.NotificationMiddlewareHandler.notify(request, response)
    return response

@app.route('/test')
def test():
    res = db.get_item("searchdynamo",
                      {
                          "comment_id": "01cdb10e-6d9b-4b23-98bc-db062ae908ec"
                      })
    result = json.dumps(res, indent=4, default=str)
    print("Result = \n", result)
    return result

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
        limit = template.get('limit')
        offset = template.get('offset')
        if (limit == None or int(limit) <= 0):
            template['limit'] = '10'
            limit = '10'
        if (offset == None or int(offset) < 0):
            template['offset'] = '0'
            offset = '0'
        res = None
        try:
            res = BreederResource.get_breeders(template, None)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        print("res: ", res)
        print("full path", request.full_path)
        self_path = request.full_path
        next_path = None
        prev_path = None
        i = self_path.find('limit=')
        j = self_path.find('offset=')
        o_len = len(offset)
        l_len = len(limit)
        next_offset = str(int(offset)+10)
        prev_offset = str(str(int(offset)-10) if int(offset) >= 10 else '0')
        if (i == -1 and j == -1):
            next_path = self_path+f'&limit={limit}&offset={next_offset}'
            prev_path = self_path+f'&limit={limit}&offset={prev_offset}'
        elif (i==-1):
            next_path = self_path[:j] + f"offset={next_offset}" + self_path[j+7+o_len:]+f"&limit={limit}"
            prev_path = self_path[:j] + f"offset={prev_offset}" + self_path[j + 7 + o_len:] + f"&limit={limit}"
        elif (j==-1):
            next_path = self_path[:i] + f"limit={limit}" + self_path[i + 6 + l_len:] + f"&offset={next_offset}"
            prev_path = self_path[:i] + f"limit={limit}" + self_path[i + 6 + l_len:] + f"&offset={prev_offset}"
        else:
            next_path = self_path[:j] + f"offset={next_offset}" + self_path[j + 7 + o_len:]
            i = next_path.find("limit=")
            next_path = next_path[:i] + f"limit={limit}" + next_path[i + 6 + l_len:]
            prev_path = self_path[:j] + f"offset={prev_offset}" + self_path[j + 7 + o_len:]
            i = prev_path.find("limit=")
            prev_path = prev_path[:i] + f"limit={limit}" + prev_path[i + 6 + l_len:]


        links = [{"rel": "self", "href": self_path},
                 {"rel": "next", "href": next_path},
                 {"rel": "prev", "href": prev_path}]

        ret = {"data":res, "links": links}
        rsp = Response(json.dumps(ret, default=str), status=200, content_type="application/json")
        return rsp
####GET START


####POST START
    if request.method == 'POST':
        # print(request.form.to_dict())
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''
        id = template.get('id')

        print("id", id)

        res = None
        address = template.get('address')
        print(address)
        if (SmartyAddressService.do_lookup(address) == False):
            rsp = Response(json.dumps("invalid address", default=str), status=400,
                               content_type="application/json")
            return rsp
        try:
            if not id.isdigit() or int(id) <= 0:
                rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                               content_type="application/json")
                return rsp
            elif BreederResource.check_breeder_id_exist(id):
                rsp = Response(json.dumps("id already exist", default=str), status=422,
                               content_type="application/json")
                return rsp

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

        res = None
        try:
            if not id.isdigit() or int(id) <= 0:
                rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                               content_type="application/json")
                return rsp
            elif not BreederResource.check_breeder_id_exist(id):
                rsp = Response(json.dumps("id does not exist", default=str), status=422,
                               content_type="application/json")
                return rsp
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
        template = {k: v for k, v in template.items() if
                    v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''
        # print('template:', template)
        # print('id:', id)

        res = None
        try:
            if not id.isdigit() or int(id) <= 0:
                rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                               content_type="application/json")
                return rsp
            elif not BreederResource.check_breeder_id_exist(id):
                rsp = Response(json.dumps("id does not exist", default=str), status=422,
                               content_type="application/json")
                return rsp

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

@app.route('/comment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def comment():
    if request.method == 'GET':
        template = request.args.to_dict()
        template = {k: v for k, v in template.items() if
                    v}  # remove key-value pairs where value is empty such as 'father': ''

        res = db.find_by_template('searchdynamo', template)
        res = json.dumps(res, indent=4, default=str)
        print("Result = \n", res)
        return res

    elif request.method == 'POST':
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if
                    v}  # remove key-value pairs where value is empty such as 'father': ''
        tags = template.get('tags')
        print("tags", tags)
        comment = template.get('comment')
        print(comment)
        email = template.get('email')
        print(email)

        res = db.add_comment("searchdynamo", email, comment, tags)
        return res


    elif request.method == 'PUT':
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if
                    v}  # remove key-value pairs where value is empty such as 'father': ''
        comment_id = template.get('id')
        print(type(comment_id), comment_id)
        print("comment_id", comment_id)
        tags = template.get('tags')
        print("tags", tags)
        comment = template.get('comment')
        print("comment", comment)
        dt = time.time()
        dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))
        new_version_id = str(uuid.uuid4())

        original_comment = db.get_item("searchdynamo", {"comment_id": comment_id})

        print(original_comment)

        new_comment = copy.deepcopy(original_comment)
        new_comment["datetime"] = dts
        new_comment["comment"] = comment
        new_comment["tags"] = tags
        new_comment["version_id"] = new_version_id

        try:
            res = db.write_comment_if_not_changed("searchdynamo", new_comment, original_comment)
            print("First write returned: ", res)
            return res
        except Exception as e:
            print("First write exception = ", str(e))
            return "update exception"



    elif request.method == 'DELETE':
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if
                    v}  # remove key-value pairs where value is empty such as 'father': ''
        comment_id = template.get('id')
        print("comment_id", comment_id)

        res = db.delete_item('searchdynamo', comment_id)
        return res

    # res = db.get_item("searchdynamo",
    #                   {
    #                       "comment_id": "01cdb10e-6d9b-4b23-98bc-db062ae908ec"
    #                   })
    # result = json.dumps(res, indent=4, default=str)
    # print("Result = \n", result)
    return None

@app.route('/cats', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cats():
####GET START
    if request.method == 'GET':
        template = request.args.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''
        limit = template.get('limit')
        offset = template.get('offset')
        if (limit == None or int(limit) <= 0):
            template['limit'] = '10'
            limit = '10'
        if (offset == None or int(offset) < 0):
            template['offset'] = '0'
            offset = '0'
        res = None
        try:
            res = CatResource.get_cats(template, None)
        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            rsp = Response(json.dumps("Internal Server Error", default=str), status=500,
                           content_type="application/json")
            return rsp

        print("res: ", res)
        print("full path", request.full_path)
        self_path = request.full_path
        next_path = None
        prev_path = None
        i = self_path.find('limit=')
        j = self_path.find('offset=')
        o_len = len(offset)
        l_len = len(limit)
        next_offset = str(int(offset) + 10)
        prev_offset = str(str(int(offset) - 10) if int(offset) >= 10 else '0')
        if (i == -1 and j == -1):
            next_path = self_path + f'&limit={limit}&offset={next_offset}'
            prev_path = self_path + f'&limit={limit}&offset={prev_offset}'
        elif (i == -1):
            next_path = self_path[:j] + f"offset={next_offset}" + self_path[j + 7 + o_len:] + f"&limit={limit}"
            prev_path = self_path[:j] + f"offset={prev_offset}" + self_path[j + 7 + o_len:] + f"&limit={limit}"
        elif (j == -1):
            next_path = self_path[:i] + f"limit={limit}" + self_path[i + 6 + l_len:] + f"&offset={next_offset}"
            prev_path = self_path[:i] + f"limit={limit}" + self_path[i + 6 + l_len:] + f"&offset={prev_offset}"
        else:
            next_path = self_path[:j] + f"offset={next_offset}" + self_path[j + 7 + o_len:]
            i = next_path.find("limit=")
            next_path = next_path[:i] + f"limit={limit}" + next_path[i + 6 + l_len:]
            prev_path = self_path[:j] + f"offset={prev_offset}" + self_path[j + 7 + o_len:]
            i = prev_path.find("limit=")
            prev_path = prev_path[:i] + f"limit={limit}" + prev_path[i + 6 + l_len:]

        links = [{"rel": "self", "href": self_path},
                 {"rel": "next", "href": next_path},
                 {"rel": "prev", "href": prev_path}]

        ret = {"data": res, "links": links}

        rsp = Response(json.dumps(ret, default=str), status=200, content_type="application/json")
        return rsp
####GET START


####POST START
    if request.method == 'POST':
        # print(request.form.to_dict())
        template = request.form.to_dict()
        template = {k: v for k, v in template.items() if v} # remove key-value pairs where value is empty such as 'father': ''

        res = None
        try:

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

        res = None
        try:
            if not id.isdigit() or int(id) <= 0:
                rsp = Response(json.dumps("id in wrong format", default=str), status=400,
                               content_type="application/json")
                return rsp
            elif not CatResource.check_cat_id_exist(id):
                rsp = Response(json.dumps("id does not exist", default=str), status=422,
                               content_type="application/json")
                return rsp

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

        res = None
        try:
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



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
