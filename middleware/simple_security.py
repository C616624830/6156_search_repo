import json

insecure_paths = ['/login/google', '/login/google/authorized']


def check_security(request, google, blueprint):

    path = request.path
    result_ok = False

    if path not in insecure_paths:
        google_data = None

        print("flag1")

        user_info_endpoint = '/oauth2/v2/userinfo'

        if google.authorized:
            print("flag2")

            google_data = google.get(user_info_endpoint).json()

            print(json.dumps(google_data, indent=2))

            s = blueprint.session
            t = s.token
            print("Token = \n", json.dumps(t, indent=2))

            result_ok = True

    else:
        result_ok = True

    return result_ok