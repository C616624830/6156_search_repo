from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message
from address_services.smarty_address_service import SmartyAddressService

def ret(request):
    print("request.args.to_dict(): ", request.args.to_dict())
    print("request.get_json(): ", request.get_json())
    print("request.headers.get('Email'): ", request.headers.get('Email'))

    template = request.args.to_dict()
    if not template:
        template = request.get_json()

    if not template:
        return ret_message("200", "no update performed")

    #filter out non-related data
    template = {k: v for k, v in template.items() if
                v and (k == 'name' or k == 'organization' or k == 'phone' or k == 'address' or k == 'website' or k == 'rating')}

    id = request.headers.get('Email')

    address = template.get('address')
    if (address and SmartyAddressService.do_lookup(address) == False):
            return ret_message("422", "invalid address")

    if (not template):
        return ret_message("200", "no update performed")

    try:
        if not BreederResource.check_breeder_id_exist(id):
            return ret_message("423", "your email account has not signed up as a breeder, go sign up a breeder with your email")

        res = BreederResource.put_breeder(id, template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    return ret_message("200", "success")