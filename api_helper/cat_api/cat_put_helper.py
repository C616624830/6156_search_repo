from application_services.CatResource.cat_service import CatResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.args.to_dict(): ", request.args.to_dict())
    print("request.get_json(): ", request.get_json())

    template = request.args.to_dict()
    if not template:
        template = request.get_json()

    if not template:
        return ret_message("no put data", "300")

    id = template.get('id')

    template = {k: v for k, v in template.items() if
                v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''

    try:
        if not id.isdigit() or int(id) <= 0:
            return ret_message("400", "id in wrong format")
        elif not CatResource.check_cat_id_exist(id):
            return ret_message("422", "id does not exist")

        res = CatResource.put_cat(id, template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("200", res)