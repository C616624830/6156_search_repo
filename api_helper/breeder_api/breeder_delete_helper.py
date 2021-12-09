from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.headers.get('Email'): ", request.headers.get('Email'))
    id = request.headers.get('Email')

    try:
        if not BreederResource.check_breeder_id_exist(id):
            return ret_message("422", "your email does not exist, go add breeder")
        res = BreederResource.delete_breeder(id)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("204", res)