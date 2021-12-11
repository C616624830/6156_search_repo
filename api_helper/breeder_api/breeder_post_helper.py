from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message
from address_services.smarty_address_service import SmartyAddressService
# user  can sign up a breeder account using another email
def ret(request):
    print("request.form.to_dict(): ", request.form.to_dict())
    print("request.get_json(): ", request.get_json())

    template = request.form.to_dict()
    if not template:
        template = request.get_json()

    template = {k: v for k, v in template.items() if
                v and (k == 'id' or k == 'name' or k == 'organization' or k == 'phone' or k == 'address' or k == 'website' or k == 'rating')}

    if (not template
        or template.get('id') == None
        or template.get('name') == None
        or template.get('organization') == None
        or template.get('phone') == None
        or template.get('address') == None
        or template.get('website') == None
        or template.get('rating') == None):
        return ret_message("422", "your provided info is not enough to sign up breeder")


    address = template.get('address')
    if (SmartyAddressService.do_lookup(address) == False):
        return ret_message("400", "invalid address")


    try:
        id = template.get('id')
        if BreederResource.check_breeder_id_exist(id):
            return ret_message("422", "this email has already been signed up")

        res = BreederResource.post_breeder(template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    # rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    # rsp.headers['location'] = '/breeders'
    return ret_message("201", res, {'location': '/breeders'})