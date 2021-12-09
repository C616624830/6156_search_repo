from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message
from address_services.smarty_address_service import SmartyAddressService

def ret(request):
    # print(request.form.to_dict())
    template = request.form.to_dict()
    template = {k: v for k, v in template.items() if
                v}  # remove key-value pairs where value is empty such as 'father': ''
    id = template.get('id')

    print("id", id)

    res = None
    address = template.get('address')
    print(address)
    if (SmartyAddressService.do_lookup(address) == False):
        return ret_message("400", "invalid address")
    try:
        if BreederResource.check_breeder_id_exist(id):
            return ret_message("422", "id already exist")

        res = BreederResource.post_breeder(template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    # rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    # rsp.headers['location'] = '/breeders'
    return ret_message("201", res, {'location': 'breeders'})