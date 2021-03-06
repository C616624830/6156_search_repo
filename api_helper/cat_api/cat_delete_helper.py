from application_services.CatResource.cat_service import CatResource
from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.form.to_dict(): ", request.form.to_dict())
    print("request.get_json(): ", request.get_json())
    print("request.headers.get('Email'): ", request.headers.get('Email'))

    template = request.form.to_dict()
    if not template:
        template = request.get_json()

    if (not template or not template.get('id')):
        return ret_message("421","you did not provide cat id")

    id = template.get('id')
    breeder = request.headers.get('Email')

    try:
        if not id.isdigit() or int(id) <= 0:
            return ret_message("422", "id in wrong format")
        elif not CatResource.check_cat_id_exist(id):
            return ret_message("423", "id does not exist")
        elif CatResource.get_cats({'id': id}, None)[0].get("breeder") != breeder:
            return ret_message("424", "you are not the breeder of this cat")

        res = CatResource.delete_cat(id)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("204", "success")