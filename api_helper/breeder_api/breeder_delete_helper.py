from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message


def ret(request):
    if request.method == 'DELETE':
        template = request.args.to_dict()
        # print(template)
        id = template.get('id', None)
        # print("id", id)

        res = None
        try:
            if not BreederResource.check_breeder_id_exist(id):
                return ret_message("201", "id does not exist")
            res = BreederResource.delete_breeder(id)

        except pymysql.err.OperationalError as e:
            print(f"error: {e}")
            return ret_message("500", "Internal Server Error")

        return ret_message("204", res)