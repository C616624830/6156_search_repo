from application_services.BreederResource.breeder_service import BreederResource
from application_services.CatResource.cat_service import CatResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.form.to_dict(): ", request.form.to_dict())
    print("request.get_json(): ", request.get_json())
    print("request.headers.get('Email'): ", request.headers.get('Email'))

    template = request.form.to_dict()
    if not template:
        template = request.get_json()

    template = {k: v for k, v in template.items() if
                 v and (k == 'id' or k == 'race' or k == 'name' or k == 'color' or k == 'dob' or k == 'father' or k == 'mother' or k == 'breeder' or k == 'listing_price')}

    if (not template
        or template.get('id') == None
        or template.get('race') == None
        or template.get('color') == None
        or template.get('dob') == None
        or template.get('breeder') == None
    ):
        return ret_message("422", "your provided info is not enough to sign up breeder")

    try:
        breeder = request.headers.get('Email')
        if template.get("breeder") != breeder:
            return ret_message("424", "you are adding a cat to a breeder account which is not yours")
        if not BreederResource.check_breeder_id_exist(breeder):
            return ret_message("423", "you are not allowed to add cat because this email is not signed up")

        for k, v in template.items():
            if k == 'id':
                if not v.isdigit() or int(v) <= 0:
                    return ret_message("400", "id in wrong format")
                elif CatResource.check_cat_id_exist(v):
                    return ret_message("422", "id already exist")

            if k == 'father':
                if not v.isdigit() or int(v) <= 0:
                    return ret_message("400", "father id in wrong format")
                elif not CatResource.check_cat_id_exist(v):
                    return ret_message("422", "father id does not exist")

            if k == 'mother':
                if not v.isdigit() or int(v) <= 0:
                    return ret_message("400", "mother id in wrong format")
                elif not CatResource.check_cat_id_exist(v):
                    return ret_message("422", "mother id does not exist")

        res = CatResource.post_cat(template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("201", res, {'location': '/cats'})