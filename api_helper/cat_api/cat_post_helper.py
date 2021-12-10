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

    if (not template or template.get('id') == None):
        return ret_message("you did not provide cat id", "422")

    template = {k: v for k, v in template.items() if
                v}  # remove key-value pairs where value is empty such as 'father': ''



    try:
        breeder = request.headers.get('Email')
        template['breeder'] = breeder
        if not BreederResource.check_breeder_id_exist(breeder):
            return ret_message("423", "you are not allowed to add cat because this email is not signed up")
        # if CatResource.get_cats({'id': id}, None)[0].get("breeder") != breeder:
        #     return ret_message("424", "you are not the breeder of this cat")

        print("CatResource.get_cats({'id': id}, None): ", CatResource.get_cats({'id': id}, None)[0].get("breeder"))
        print("CatResource.get_cats({'id': id}, None)[0].get(\"breeder\").get(\"breeder\"): ", CatResource.get_cats({'id': id}, None)[0].get("breeder").get("breeder"))

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