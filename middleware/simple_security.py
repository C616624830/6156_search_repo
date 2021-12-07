import json

insecure_paths = ['/login_check']

def check_security(db, request):
    path = request.path
    if path not in insecure_paths:
        print("request: ", request)
        data = request.get_json()
        if (data == None or data.get("Email") == None or data.get("id_token") == None):
            print("access service without token")
            return 1
        Email = data.get("Email")
        id_token = data.get("id_token")
        print("flag1")
        print("Email: ", Email)
        print("id_token: ", id_token)
        res = db.find_by_template("logindynamo", {"Email":Email, "id_token":id_token})
        print("tokendb_res: ", res)
        flag = 0
        for e in res:
            if (e.get('Email') == Email and e.get('id_token') == id_token):
                flag = 1
        if (flag == 1):
            print("Found token")
            return 2
        else:
            print("No token Found")
            return 1
    else:
        return 3


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