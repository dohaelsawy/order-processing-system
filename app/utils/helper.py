from bson import ObjectId


def json_converter(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Type not serializable {obj}")