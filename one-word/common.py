import json

__all__ = ['is_json']

def is_json(req):
    try:
        json.loads(req.text)
        return True
    except AttributeError as error:
        return False
    return False