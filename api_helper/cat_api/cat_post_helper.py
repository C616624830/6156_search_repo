from application_services.BreederResource.breeder_service import BreederResource
from application_services.CatResource.cat_service import CatResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    # print(request.form.to_dict())
    template = request.form.to_dict()
    template = {k: v for k, v in template.items() if
                v}  # remove key-value pairs where value is empty such as 'father': ''

    res = None
    try:

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

            if k == 'breeder':
                if not BreederResource.check_breeder_id_exist(v):
                    return ret_message("422", "breeder id does not exist")

        res = CatResource.post_cat(template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("201", res, {'location': '/cats'})