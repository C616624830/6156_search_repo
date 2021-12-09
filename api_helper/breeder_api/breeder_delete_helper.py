from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.args.to_dict(): ", request.args.to_dict())
    print("request.get_json(): ", request.get_json())

    template = request.args.to_dict()
    if not template:
        template = request.get_json()

    if not template:
        return ret_message("no delete info", "300")

    id = template.get('id')

    try:
        if not BreederResource.check_breeder_id_exist(id):
            return ret_message("201", "id does not exist")
        res = BreederResource.delete_breeder(id)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("204", res)