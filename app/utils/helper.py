from bson import ObjectId
from datetime import datetime

def json_converter(obj):
    obj["_id"] = str(obj["_id"])
    return obj
