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

    #make sure all required data is included
    if (not template
        or not template.get('id')
        or not template.get('name')
        or not template.get('organization')
        or not template.get('phone')
        or not template.get('address')
        or not template.get('website')
        or not template.get('rating')):
        print("template: ", template)
        return ret_message("421", "your provided info is not enough to sign up breeder")

    # filter out non-related data
    template = {k: v for k, v in template.items() if
                v and (k == 'id' or k == 'name' or k == 'organization' or k == 'phone' or k == 'address' or k == 'website' or k == 'rating')}


    address = template.get('address')
    if (SmartyAddressService.do_lookup(address) == False):
        return ret_message("422", "invalid address")


    try:
        id = template.get('id')
        if BreederResource.check_breeder_id_exist(id):
            return ret_message("425", "this email has already been signed up")

        res = BreederResource.post_breeder(template)

    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    # rsp = Response(json.dumps(res, default=str), status=201, content_type="application/json")
    # rsp.headers['location'] = '/breeders'
    return ret_message("201", "success", {'location': '/breeders'})