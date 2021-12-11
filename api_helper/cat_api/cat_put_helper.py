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

    if (not template or template.get('id') == None):
        return ret_message("you did not provide cat id", "422")

    id = template.get('id')
    breeder = request.headers.get('Email')

    #filter out non-related data
    template = {k: v for k, v in template.items() if
                v and k != 'id' and (k == 'race' or k == 'name' or k == 'color' or k == 'dob' or k == 'father' or k == 'mother' or k == 'breeder' or k == 'listing_price')}

    if (not template):
        return ret_message("you did not provide update info", "200")

    try:
        if not id.isdigit() or int(id) <= 0:
            return ret_message("400", "id in wrong format")
        elif not CatResource.check_cat_id_exist(id):
            return ret_message("422", "id does not exist")
        elif CatResource.get_cats({'id': id}, None)[0].get("breeder") != breeder:
            return ret_message("424", "you are not the breeder of this cat")

        res = CatResource.put_cat(id, template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("200", res)