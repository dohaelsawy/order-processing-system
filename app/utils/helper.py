from bson import ObjectId
from datetime import datetime

def json_converter(obj):
    if isinstance(obj, ObjectId) or isinstance(obj, datetime):
        return str(obj)

    raise TypeError(f"Type not serializable {obj}")