from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message
from address_services.smarty_address_service import SmartyAddressService

def ret(request):
    print("request.form.to_dict(): ", request.form.to_dict())
    print("request.get_json(): ", request.get_json())
    print("request.headers.get('Email'): ", request.headers.get('Email'))

    template = request.args.to_dict()
    if not template:
        template = request.get_json()

    template = {k: v for k, v in template.items() if
                v}  # remove key-value pairs where value is empty such as 'father': ''

    if not template:
        return ret_message("your provided info is not enough to sign up breeder", "422")



    # address = template.get('address')
    # if (SmartyAddressService.do_lookup(address) == False):
    #     return ret_message("400", "invalid address")


    try:
        id = request.headers.get('Email')
        template['id'] = id
        if BreederResource.check_breeder_id_exist(id):
            return ret_message("422", "this email has already been signed up")

        res = BreederResource.post_breeder(template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    # rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    # rsp.headers['location'] = '/breeders'
    return ret_message("201", res, {'location': '/breeders'})