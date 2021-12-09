from application_services.BreederResource.breeder_service import BreederResource
import pymysql
from api_helper.utility import ret_message

def ret(request):
    print("request.args.to_dict(): ", request.args.to_dict())
    template = request.args.to_dict()
    template = {k: v for k, v in template.items() if
                v}  # remove key-value pairs where value is empty such as 'father': ''

    if not template:
        return ret_message("no get data", "300")

    limit = template.get('limit')
    offset = template.get('offset')
    if (limit == None or int(limit) <= 0):
        template['limit'] = '10'
        limit = '10'
    if (offset == None or int(offset) < 0):
        template['offset'] = '0'
        offset = '0'
    res = None
    try:
        res = BreederResource.get_breeders(template, None)
    except pymysql.err.OperationalError as e:
        print(f"error: {e}")
        return ret_message("500", "Internal Server Error")

    print("res: ", res)
    print("full path", request.full_path)
    self_path = request.full_path
    next_path = None
    prev_path = None
    i = self_path.find('limit=')
    j = self_path.find('offset=')
    o_len = len(offset)
    l_len = len(limit)
    next_offset = str(int(offset) + 10)
    prev_offset = str(str(int(offset) - 10) if int(offset) >= 10 else '0')
    if (i == -1 and j == -1):
        next_path = self_path + f'&limit={limit}&offset={next_offset}'
        prev_path = self_path + f'&limit={limit}&offset={prev_offset}'
    elif (i == -1):
        next_path = self_path[:j] + f"offset={next_offset}" + self_path[j + 7 + o_len:] + f"&limit={limit}"
        prev_path = self_path[:j] + f"offset={prev_offset}" + self_path[j + 7 + o_len:] + f"&limit={limit}"
    elif (j == -1):
        next_path = self_path[:i] + f"limit={limit}" + self_path[i + 6 + l_len:] + f"&offset={next_offset}"
        prev_path = self_path[:i] + f"limit={limit}" + self_path[i + 6 + l_len:] + f"&offset={prev_offset}"
    else:
        next_path = self_path[:j] + f"offset={next_offset}" + self_path[j + 7 + o_len:]
        i = next_path.find("limit=")
        next_path = next_path[:i] + f"limit={limit}" + next_path[i + 6 + l_len:]
        prev_path = self_path[:j] + f"offset={prev_offset}" + self_path[j + 7 + o_len:]
        i = prev_path.find("limit=")
        prev_path = prev_path[:i] + f"limit={limit}" + prev_path[i + 6 + l_len:]

    links = [{"rel": "self", "href": self_path},
             {"rel": "next", "href": next_path},
             {"rel": "prev", "href": prev_path}]

    ret = {"data": res, "links": links}
    return ret_message("500", ret)