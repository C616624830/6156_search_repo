from flask import *
from flask_cors import CORS
import logging
import middleware.simple_security as simple_security
import dynamo.dynamodb as db
from api_helper.breeder_api import breeder_get_helper
from api_helper.breeder_api import breeder_post_helper
from api_helper.breeder_api import breeder_delete_helper
from api_helper.breeder_api import breeder_put_helper
from api_helper.cat_api import cat_get_helper
from api_helper.cat_api import cat_post_helper
from api_helper.cat_api import cat_delete_helper
from api_helper.cat_api import cat_put_helper
from api_helper.utility import ret_message
import copy
import uuid
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


import middleware.notification as notification

app = Flask(__name__)
CORS(app)


app.secret_key = 'some secret'


# @app.before_request
# def before_request_func():
#     print("flag0")
#     n, info = simple_security.check_security(request)
#     if n == False:
#         return ret_message("300", info)


@app.after_request
def after_request_func(response):
    notification.NotificationMiddlewareHandler.notify(request, response)
    return response

# request.form or request.get_json is for retrieving POST request data from html form
# requeust.args is for retrieving GET request data from html form

@app.route('/breeders', methods=['GET', 'POST', 'PUT', 'DELETE'])
def breeders():
    if request.method == 'GET':
       return breeder_get_helper.ret(request)
    elif request.method == 'POST':
        return breeder_post_helper.ret(request)
    elif request.method == 'DELETE':
        return breeder_delete_helper.ret(request)
    elif request.method == 'PUT':
        return breeder_put_helper.ret(request)

@app.route('/cats', methods=['GET', 'POST', 'PUT', 'DELETE'])
def cats():
    if request.method == 'GET':
        return cat_get_helper.ret(request)
    elif request.method == 'POST':
        return cat_post_helper.ret(request)
    elif request.method == 'DELETE':
        return cat_delete_helper.ret(request)
    elif request.method == 'PUT':
        return cat_put_helper.ret(request)

# @app.route('/login_check', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def login():
#     if (request.method == 'POST'):
#         print("request.headers.get(\"Email\"): ", request.headers.get("Email"))
#         if (request.headers.get("Email") == None or request.headers.get("id_token") == None):
#             return ret_message("300", "login_check did not see id_token and email in the header")
#
#         Email = request.headers.get("Email")
#         id_token = request.headers.get("id_token")
#         print("Email: ", Email)
#         db.add_token("logindynamo", Email, id_token)
#         return ret_message("200", "good")
#     else:
#         return ret_message("300", "Not post request")

# @app.route('/log_out', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def log_out():
#     if (request.method == 'POST'):
#         print(request.headers)
#         if (request.headers.get("Email") == None or request.headers.get("id_token") == None):
#             return ret_message("300", "No id_token and email")
#         res = db.delete_item('logindynamo', {"Email": request.headers.get("Email")})
#         print("log_out_res: ", res)
#         return ret_message("200", "logged out")

# @app.route('/cats/breeder/<cid>')
# def breeder_of_cat(cid):
#     res = CatResource.get_breeder_id(cid)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#
#
# @app.route('/breeders/rating', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def breeder_rating():
#     if request.method == 'GET':
#         breeder_id = request.args.get('bid', default = '1', type = str)
#         res = BreederResource.get_breeder_rating(breeder_id)
#         rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#         return rsp
#
# @app.route('/comment', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def comment():
#     if request.method == 'GET':
#         template = request.args.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#
#         res = db.find_by_template('searchdynamo', template)
#         res = json.dumps(res, indent=4, default=str)
#         print("Result = \n", res)
#         return res
#
#     elif request.method == 'POST':
#         template = request.form.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#         tags = template.get('tags')
#         print("tags", tags)
#         comment = template.get('comment')
#         print(comment)
#         email = template.get('email')
#         print(email)
#
#         res = db.add_comment("searchdynamo", email, comment, tags)
#         return res
#
#
#     elif request.method == 'PUT':
#         template = request.form.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#         comment_id = template.get('id')
#         print(type(comment_id), comment_id)
#         print("comment_id", comment_id)
#         tags = template.get('tags')
#         print("tags", tags)
#         comment = template.get('comment')
#         print("comment", comment)
#         dt = time.time()
#         dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))
#         new_version_id = str(uuid.uuid4())
#
#         original_comment = db.get_item("searchdynamo", {"comment_id": comment_id})
#
#         print(original_comment)
#
#         new_comment = copy.deepcopy(original_comment)
#         new_comment["datetime"] = dts
#         new_comment["comment"] = comment
#         new_comment["tags"] = tags
#         new_comment["version_id"] = new_version_id
#
#         try:
#             res = db.write_comment_if_not_changed("searchdynamo", new_comment, original_comment)
#             print("First write returned: ", res)
#             return res
#         except Exception as e:
#             print("First write exception = ", str(e))
#             return "update exception"
#
#
#
#     elif request.method == 'DELETE':
#         template = request.form.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#         comment_id = template.get('id')
#         print("comment_id", comment_id)
#
#         res = db.delete_item('searchdynamo', comment_id)
#         return res
#
#     # res = db.get_item("searchdynamo",
#     #                   {
#     #                       "comment_id": "01cdb10e-6d9b-4b23-98bc-db062ae908ec"
#     #                   })
#     # result = json.dumps(res, indent=4, default=str)
#     # print("Result = \n", result)
#     return None

# @app.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def test():
#     return

# @app.route('/')
# def get_index():
#     return render_template('index.html')

# @app.route('/add_cat')
# def add_cat_page():
#     return render_template('add_cat.html')
#
# @app.route('/delete_cat')
# def delete_cat_page():
#     return render_template('delete_cat.html')
#
# @app.route('/search_cat')
# def search_cat_page():
#     return render_template('search_cat.html')
#
# @app.route('/add_breeder')
# def add_breeder_page():
#     return render_template('add_breeder.html')
#
# @app.route('/search_breeder')
# def search_breeder_page():
#     return render_template('search_breeder.html')
#
# @app.route('/view_breeder_rating')
# def view_breeder_rating_page():
#     return render_template('view_breeder_rating.html')

###################################
# client_id = os.environ.get("CLIENT_ID", None)
# client_secret = os.environ.get("CLIENT_SECRET", None)
#
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
#
# blueprint = make_google_blueprint(
#     client_id=client_id,
#     client_secret=client_secret,
#     reprompt_consent=True,
#     scope=["profile", "email"],
#     offline = True
# )
# app.register_blueprint(blueprint, url_prefix="/login")
#
# g_bp = app.blueprints.get("google")
#
# @app.before_request
# def before_request_func():
#     # print("flag0")
#     result_ok = simple_security.check_security(request, google, g_bp)
#     # print("flag3")
#     if not result_ok:
#         print('flag4')
#         # print(url_for('/'))
#         return redirect(url_for('google.login'))
###################################

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
