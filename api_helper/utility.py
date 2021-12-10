from flask import Response
import json

def ret_message(status, message, headers = {}, code=2):
    return Response(json.dumps({"codddddddde": status, "message": message, "headers": headers, "code": status}, default=str), content_type="application/json")