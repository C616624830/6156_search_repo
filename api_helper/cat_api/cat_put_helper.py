from application_services.CatResource.cat_service import CatResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    template = request.args.to_dict()
    id = template.get('id', None)
    # print('id:', id)

    res = None
    try:
        if not id.isdigit() or int(id) <= 0:
            return ret_message("400", "id in wrong format")
        elif not CatResource.check_cat_id_exist(id):
            return ret_message("422", "id does not exist")

        template = {k: v for k, v in template.items() if
                    v and k != 'id'}  # remove key-value pairs where value is empty such as 'father': ''
        # print('template:', template)

        res = CatResource.put_cat(id, template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("200", res)