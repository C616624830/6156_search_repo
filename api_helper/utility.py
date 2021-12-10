from flask import Response
import json

def ret_message(status, message, headers = {}):
    return Response(json.dumps({"codddddddde": status, "message": message, "headers": headers}, default=str), content_type="application/json")