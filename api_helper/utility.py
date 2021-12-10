from flask import Response
import json

def ret_message(status, message, headers = {}, code=2):
    return Response(json.dumps({"message": message, "code": status, "headers": headers, "status": status}, default=str), content_type="application/json")