from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.args.to_dict(): ", request.args.to_dict())
    print("request.get_json(): ", request.get_json())

    template = request.args.to_dict()
    if not template:
        template = request.get_json()

    template = {k: v for k, v in template.items() if
                v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''

    if not template:
        return ret_message("no put data", "300")

    id = template.get('id')

    try:
        if not BreederResource.check_breeder_id_exist(id):
            return ret_message("422", "id does not exist")

        res = BreederResource.put_breeder(id, template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("200", res)