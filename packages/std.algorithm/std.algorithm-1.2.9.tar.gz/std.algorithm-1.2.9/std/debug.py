from collections import OrderedDict


def compare(obj, _obj):

    def compare_element(v, _v):
        if isinstance(v, (dict, OrderedDict)):
            if isinstance(_v, (dict, OrderedDict)):
                compare(v, _v)
            else:
                return 'type'

        elif isinstance(v, (list, tuple)):
            if isinstance(_v, (list, tuple)):
                compare(v, _v)
            else:
                return 'type'

        else:
            try:
                b = v == _v
                if hasattr(b, 'all'):
                    if b.all():
                        ...
                    else:
                        return 'value'
                elif b:
                    ...
                else:
                    return 'value'
            except RuntimeError as e:
                return e

    if isinstance(obj, (dict, OrderedDict)) and isinstance(_obj, (dict, OrderedDict)):
        if len(obj) != len(_obj):
            print("keys lengths are not equal!")
            if len(obj) > len(_obj):
                print("missing keys in the right hand side:", obj.keys() - _obj.keys())
            else:
                print("missing keys in the left hand side:", _obj.keys() - obj.keys())

        for key, v in obj.items():
            if key not in _obj:
                print(f"{key} does not exist in the right hand side")
                continue
            err_type = compare_element(v, _obj[key])
            if err_type:
                print(f'{err_type} error, at key = {key}')

    elif isinstance(obj, (list, tuple)) and isinstance(_obj, (list, tuple)):
        if len(obj) != len(_obj):
            print("lengths are not equal!")
            print(len(obj), len(_obj))
            return

        for i, [v, _v] in enumerate(zip(obj, _obj)):
            err = compare_element(v, _v)
            if err:
                print('index =', i, 'error info:', err)
