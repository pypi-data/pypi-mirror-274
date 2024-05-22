from json import JSONEncoder

from peliqan.exceptions import PeliqanJsonSerializerException


class Empty:
    pass


empty = Empty()


def _serialize_data(obj):
    if isinstance(obj, dict):
        for k in obj:
            obj[k] = _serialize_data(obj[k])

        formatted_obj = obj
    elif type(obj) in (list, tuple):
        obj_len = len(obj)
        for i in range(obj_len):
            obj[i] = _serialize_data(obj[i])

        formatted_obj = obj

    elif isinstance(obj, (int, float, str)):
        formatted_obj = obj
        if isinstance(obj, float) and str(obj) == 'nan':
            formatted_obj = None

    elif isinstance(obj, type(None)):
        formatted_obj = None

    else:
        try:
            formatted_obj = JSONEncoder().encode(obj)
        except Exception as e:
            try:
                formatted_obj = str(obj)
            except Exception:
                raise PeliqanJsonSerializerException(
                    f"Could not serialize {obj.__class__.__name__} with value {obj}. "
                    f"Original error is {e}"
                )

    return formatted_obj
