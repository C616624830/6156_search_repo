from google.oauth2 import id_token
from google.auth.transport import requests
import os

# every request must provide a valid token to access services, if not, return with a status code = 300 to client, client see 300, it will go to google login page and login and then hold the valid token in local storage, then user can access the service using that token again, this method does not need "login_check" because we don't need to record the token in database, and the client can log out just by clear his local storage, so no "log_out" api is needed as well.
public_paths = ['/getcats', '/getbreeders', '/postbreeders']
def check_security(request):
    try:
        path = request.path
        if path in public_paths:
            return True, "good"
        else:
            print("request.headers: ", request.headers)
            token = request.headers['id_token']
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.environ.get("CLIENT_ID", None))
            print("security idinfo: ", idinfo)
            # userid = idinfo['sub']
            print("Token is valid, go using service")
            return True, "good"
    except ValueError:
        print("security valueError")
        return False, "security valueError"
    except KeyError:
        print("invalid token")
        return False, "invalid token, login in again\n"

# verify the token in request header by finding the same token in dynamodb, if found, allow access service, if not, denied and ask user to login again and update the dynamo with new token using /login_check api, after that, use service again
# public_paths = ['/login_check']
# def check_security(db, request):
#     path = request.path
#     if path not in public_paths:
#         print("request.header: ", request.headers.get("Email"))
#         print("request.args: ", request.args)
#         print("request: ", request)
#         if (request.headers.get("Email") == None or request.headers.get("id_token") == None):
#             print("access service without token")
#             return 1
#         Email = request.headers.get("Email")
#         id_token = request.headers.get("id_token")
#         print("flag1")
#         print("Email: ", Email)
#         # print("id_token: ", id_token)
#         res = db.find_by_template("logindynamo", {"Email":Email, "id_token":id_token})
#         # print("tokendb_res: ", res)
#         flag = 0
#         for e in res:
#             if (e.get('Email') == Email and e.get('id_token') == id_token):
#                 flag = 1
#         if (flag == 1):
#             print("Found token")
#             return 2
#         else:
#             print("No token Found")
#             return 1
#     else:
#         return 3


# insecure_paths = ['/login/google', '/login/google/authorized']
# def check_security(request, google, blueprint):
#
#     path = request.path
#     result_ok = False
#
#     if path not in insecure_paths:
#         google_data = None
#
#         # print("flag1")
#
#         user_info_endpoint = '/oauth2/v2/userinfo'
#
#         if google.authorized:
#             # print("flag2")
#
#             google_data = google.get(user_info_endpoint).json()
#
#             # print(json.dumps(google_data, indent=2))
#
#             s = blueprint.session
#             t = s.token
#             # print("Token = \n", json.dumps(t, indent=2))
#
#             result_ok = True
#
#     else:
#         result_ok = True
#
#     return result_ok