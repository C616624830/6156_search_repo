from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    template = request.args.to_dict()
    id = template.get('id', None)
    template = {k: v for k, v in template.items() if
                v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''
    # print('template:', template)
    # print('id:', id)

    res = None
    try:
        if not BreederResource.check_breeder_id_exist(id):
            return ret_message("422", "id does not exist")

        res = BreederResource.put_breeder(id, template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("200", res)