import json

insecure_paths = ['/login_check']

def check_security(session, request):
    path = request.path
    if path not in insecure_paths:
        data = request.get_json()
        id_token = data["id_token"]
        Email = data["Email"]
        # print("flag1")

        if (id_token!=session.get("id_token") or Email!=session.get("Email")):
            return json.dumps({"code": "300", "message": "no record of token_id or email exists in the service"})
        else:
            return json.dumps({"code": "200", "message": "found record"})

    else:
        return json.dumps({"code": "200", "message": "insecure path"})


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