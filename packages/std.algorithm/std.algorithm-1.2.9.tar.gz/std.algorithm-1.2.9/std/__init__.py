import os, json, time, inspect, functools, sys, signal, types
from enum import Enum, unique
from tqdm import tqdm

def is_Windows():
    return os.sep == '\\'


# is Linux System
def is_Linux():
    return os.sep == '/'


def argmax(arr):
    m = arr[0]
    index = 0
    for i in range(1, len(arr)):
        a = arr[i]
        if a > m:
            index = i
            m = a

    return index


def argmin(arr):
    m = arr[0]
    index = 0
    for i in range(1, len(arr)):
        a = arr[i]
        if a < m:
            index = i
            m = a

    return index


def rindex(arr, e):
    for i, _e in enumerate(reversed(arr)):
        if e == _e:
            return -i - 1
    else:
        raise ValueError(f'{e} is not in list')


def batch_map(proc, items, processes=8):
    '''
# usage:
# pip install std.algorithm
import os, std
from std import http
os.environ['MYSQL_HOST'] = 'your_host'
os.environ['MYSQL_DATABASE'] = 'your_database'
from std import MySQL
data = ((obj['id'], obj['text']) for obj in MySQL.instance.select('website', training=0, limit=256, dictionary=True))
id, text = zip(*data)

def proc(text):
    return http.json_post('http://localhost/your_awesomeapi', dict(text=text, lang='en'))

if __name__ == '__main__':
    label = std.flatten(std.batch_map(proc, std.batches(text, batch_size=16), processes=4))
    rowcount = MySQL.instance.executemany('update your_table set label = %s, training = 2 where id = %s', [*zip(label, id)])
    print('rowcount =', rowcount)
    '''

    from multiprocessing import Pool
    with Pool(processes=processes) as pool:
        return pool.map(proc, items)


def batch_imap(proc, items, processes=8):
    from multiprocessing import Pool
    with Pool(processes=processes) as pool:
        yield from pool.imap(proc, items)


def batch_imap_unordered(proc, items, processes=8):
    from multiprocessing import Pool
    with Pool(processes=processes) as pool:
        yield from pool.imap_unordered(proc, items)


def listdir(rootdir, ext='', recursive=False):
    for name in os.listdir(rootdir):
        path = os.path.join(rootdir, name)

        if os.path.isdir(path):
            if recursive:
                yield from listdir(path, ext, recursive=True)
        else:
            if ext:
                hit = False
                if isinstance(ext, str):
                    hit = path.endswith(ext)
                else:
                    hit = any(path.endswith(ext) for ext in ext)
                if hit:
                    yield path
            else:
                yield path


def listfolders(rootdir):
    for name in os.listdir(rootdir):
        path = os.path.join(rootdir, name)
        if os.path.isdir(path):
            yield name


def listdir_recursive(rootdir, ext='.txt'):
    for name in os.listdir(rootdir):
        path = os.path.join(rootdir, name)

        if os.path.isdir(path):
            yield from listdir_recursive(path, ext)
        else:
            if ext:
                if path.endswith(ext):
                    yield path
            else:
                yield path


def eol_convert(fileName):
    def eol_convert(fileName):
        with open(fileName, "rb") as f:
            data = bytearray(os.path.getsize(fileName))
            f.readinto(data)
            # print(data)
            data = data.replace(b"\r\n", b"\n")

        with open(fileName, "wb") as f:
            # print(data)
            f.write(data)

    if fileName.startswith('.'):
        for file in listdir('.', fileName, recursive=True):
            eol_convert(file)
    else:
        eol_convert(fileName)


def cstring(s):
    return bytes(s, 'utf8')


def json_encode(data, utf8=False, indent=None):
    if isinstance(data, types.FunctionType):
        def func(*args, **kwargs):
            return json_encode(data(*args, **kwargs), utf8=utf8, indent=indent)

        func.__name__ = data.__name__
        return func

    s = json.dumps(data, ensure_ascii=False, indent=indent, cls=JSONEncoder)
    if utf8:
        s = s.encode(encoding='utf-8')
    return s


class Object:

    def __init__(self, *args, **kwargs):
        if args:
            kwargs, = args

        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = Object(value)

            self.__dict__[key] = value

    def __iter__(self):  # Get iterator object on iter
        return iter(self.__dict__.keys())

    def __getitem__(self, index):
        return self.__dict__.get(index, None)

    def __setitem__(self, index, rhs):
        self.__dict__[index] = rhs

    def __delitem__(self, index):
        del self.__dict__[index]

    def __setattr__(self, index, rhs):
        self.__dict__[index] = rhs

    def __getattr__(self, index):
        return self.__dict__.get(index, None)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def serialize(self):
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, Object):
                v = v.serialize()
            res[k] = v
        return res

    # perform el in self
    def __contains__(self, el):
        return el in self.__dict__

    def pop(self, key):
        return self.__dict__.pop(key)

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__

    # self | rhs
    # self |= rhs
    def __or__(self, rhs):
        obj = Object()
        for key, value in self.items():
            obj[key] = value

        for key, value in rhs.items():
            obj[key] = value

        return obj

    def __len__(self):
        return len(self.__dict__)

    def __eq__(self, rhs):
        if len(self) != len(rhs):
            return False

        for k, v in self.items():
            if v != rhs[k]:
                return False
        return True

    @staticmethod
    def from_dict(kwargs):
        obj = Object()
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = Object.from_dict(value)

            obj[key] = value
        return obj


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, (bytes, bytearray)):
            return str(obj, encoding='utf-8')

        if isinstance(obj, Object):
            return obj.__dict__

        from inspect import isgenerator
        if isgenerator(obj):
            return [*obj]

        return super().default(self, obj)


class Array(list):

    def __init__(self, *args):
        super(Array, self).__init__(*args)

    def __getitem__(self, index):
        if index < len(self):
            return super(Array, self).__getitem__(index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self += [None] * (index - len(self) + 1)

        super(Array, self).__setitem__(index, value)

    def binary_search(self, value, compareTo=None):
        return binary_search(self, value, compareTo)

    def equal_range(self, value, compareTo=None):
        return equal_range(self, value, compareTo)

    @property
    def length(self):
        return len(self)


def binary_insert(arr, value, **kwargs):
    arr.insert(binary_search(arr, value, **kwargs), value)


def compareTo(lhs, rhs):
    if isinstance(lhs, str):
        return compareTo([ord(c) for c in lhs], [ord(c) for c in rhs])

    if isinstance(lhs, (tuple, list)):
        for lhs, rhs in zip(lhs, rhs):
            cmp = compareTo(lhs, rhs)
            if cmp:
                return cmp

        return 0

    return lhs - rhs


def cache_key(value, compareTo=None, key=None):
    if compareTo is None:
        if key is None:
            compareTo = lambda x, y: -1 if x < y else 1 if x > y else 0
        else:
            value = key(value)
            def compareTo(lhs, rhs):
                global compareTo
                return compareTo(key(lhs), rhs)
    return value, compareTo


def binary_search(arr, value, compareTo=None, key=None):
    value, compareTo = cache_key(value, compareTo, key)

    begin = 0
    end = len(arr)
    while True:
        if begin == end:
            return begin

        mid = begin + end >> 1
        ret = compareTo(arr[mid], value)
        if ret < 0:
            begin = mid + 1
        elif ret > 0:
            end = mid
        else:
            return mid


def equal_range(arr, value, compareTo=None, key=None):
    value, compareTo = cache_key(value, compareTo, key)

    begin = 0
    end = len(arr)
    while True:
        if begin == end:
            break

        mid = begin + end >> 1

        ret = compareTo(arr[mid], value)
        if ret < 0:
            begin = mid + 1
        elif ret > 0:
            end = mid
        else:
            stop = begin - 1
            begin = mid
            while True:
                pivot = -(-begin - stop >> 1)
                if pivot == begin:
                    break

                if compareTo(arr[pivot], value):
                    stop = pivot
                else:
                    begin = pivot

            while True:
                pivot = mid + end >> 1
                if pivot == mid:
                    break

                if compareTo(arr[pivot], value):
                    end = pivot
                else:
                    mid = pivot

            break

    return begin, end


def computed(prop):

    @cache
    @property
    def func(self):
        return prop(self)

    func.fget.__name__ = prop.__name__
    return func


def cache(prop):
    if isinstance(prop, property):

        class cached(property):

            def __get__(self, obj, objtype=None):
                name = self.fget.__name__
                if name in obj.__dict__:
                    return obj.__dict__[name]
                value = self.fget(obj)
                obj.__dict__[name] = value
                return value

        return cached(prop.fget)


class cached_property:
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")

        name = self.fget.__name__
        if name in obj.__dict__:
            return obj.__dict__[name]
        value = self.fget(obj)
        obj.__dict__[name] = value
        return value

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


def indexOf(arr, value):
    for i, val in enumerate(arr):
        if val == value:
            return i

    return -1


def indexFor(arr, fn):
    for i, val in enumerate(arr):
        if fn(val):
            return i

    return -1


class _DecoratorContextManager:
    """Allow a context manager to be used as a decorator"""

    def __call__(self, func):
        if inspect.isgeneratorfunction(func):
            return self._wrap_generator(func)

        @functools.wraps(func)
        def decorate_context(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return decorate_context

    def _wrap_generator(self, func):
        """Wrap each generator invocation with the context manager"""
        @functools.wraps(func)
        def generator_context(*args, **kwargs):
            gen = func(*args, **kwargs)

            # Generators are suspended and unsuspended at `yield`, hence we
            # make sure the grad mode is properly set every time the execution
            # flow returns into the wrapped generator and restored when it
            # returns through our `yield` to our caller.
            cls = type(self)
            try:
                # Issuing `None` to a generator fires it up
                with cls():
                    response = gen.send(None)

                while True:
                    try:
                        # Forward the response to our caller and get its next request
                        request = yield response

                    except GeneratorExit:
                        # Inform the still active generator about its imminent closure
                        with cls():
                            gen.close()
                        raise

                    except BaseException:
                        # Propagate the exception thrown at us by the caller
                        with cls():
                            response = gen.throw(*sys.exc_info())

                    else:
                        # Pass the last request to the generator and get its response
                        with cls():
                            response = gen.send(request)

            # We let the exceptions raised above by the generator's `.throw` or
            # `.send` methods bubble up to our caller, except for StopIteration
            except StopIteration as e:
                # The generator informed us that it is done: take whatever its
                # returned value (if any) was and indicate that we're done too
                # by returning it (see docs for python's return-statement).
                return e.value

        return generator_context


class Timer(_DecoratorContextManager):
    def __init__(self, message=None, logger=None, startHint=False):
        self.message = message
        self.logger = logger
        if startHint:
            if self.logger:
                self.logger.info(message)
            else:
                print(message)

    def __enter__(self):
        self.start = time.time()

    @property
    def HHmmss(self):
        lapse = time.time() - self.start
        seconds = lapse % 60
        minutes = int(lapse // 60)
        if minutes > 0:
            hours = minutes // 60
            if hours > 0:
                minutes %= 60
                return "%02d:%02d:%02d" % (hours, minutes, seconds)

            return "%02d:%02d" % (minutes, seconds)

        return "%.2f seconds" % seconds

    def __exit__(self, *_):
        if self.message:
            msg = f'time cost for {self.message} is %s' % self.HHmmss
        else:
            msg = 'time cost is %s' % self.HHmmss

        if self.logger:
            self.logger.info(msg)
        else:
            print(msg)


class Timeout:
    """Timeout class using ALARM signal."""

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)  # disable alarm

    def raise_timeout(self, *args):
        raise Exception("runtime timeout")


def array_key_exists(key, data):
    if isinstance(data, list):
        return key < len(data)
    return key in data


def __setitem__(data, key, value):
    if isinstance(data, list):
        assert isinstance(key, int)
        if key >= len(data):
            data += [None] * (key + 1 - len(data))

    data[key] = value


def setitem(data, *args):
    *indices, value = args

    parentData = None
    for i, key in enumerate(indices):
        if data is None and parentData is not None and i:
            data = [] if isinstance(key, int) else {}
            parentData[indices[i - 1]] = data

        if i + 1 < len(indices):
            if isinstance(data[key], (str, int)) if array_key_exists(key, data) else True:
                __setitem__(data, key, [] if isinstance(indices[i + 1], int) else {})

            parentData = data
            data = data[key]
        else:
            if isinstance(key, str) and isinstance(data, list):
                if parentData != None and i:
                    data = {}
                    parentData[indices[i - 1]] = data
                else:
                    for i in [*reversed(range(data.length))]:
                        del data[i]

            __setitem__(data, key, value)


def __set__(*cls):
    if len(cls) == 1:
        cls, = cls
        if isinstance(cls, (types.ModuleType, type)):
            def __set__(func):
                __name__ = func.fget.__name__ if isinstance(func, property) else func.__name__
                setattr(cls, __name__, func)
                if isinstance(func, classmethod):
                    assert getattr(cls, __name__).__func__ is func.__func__
                elif isinstance(func, staticmethod):
                    assert getattr(cls, __name__) is func.__func__
                else:
                    assert getattr(cls, __name__) is func
                return func
        else:
            # cls is an object, thus we use func.__get__(cls) to create a method for it.
            def __set__(func):
                '''
usage of __get__ method:
def function(self, *args, **kwargs):
    # do something with args, kwargs and return a result
    result = ...
    return result
self.function = function.__get__(self)
now you can use:
result = self.function(*args, **kwargs)
                '''
                __name__ = func.__name__
                if func.__code__.co_varnames[0] == 'self':
                    setattr(cls, __name__, func.__get__(cls))
                    func = getattr(cls, __name__)
                else:
                    setattr(cls, __name__, func)
                return func
        return __set__
    else:
        def __set__(func):
            global __set__
            for c in cls:
                __set__(c)(func)
            return func
    return __set__


def yield_from_slices(data, slices):
    assert isinstance(slices, slice)
    start, stop, step = slices.start, slices.stop, slices.step
    if start is None:
        start = 0

    if stop is None:
        stop = float('inf')

    if step is None:
        step = 1

    for i, obj in enumerate(data):
        if i < start:
            continue
        # i >= start
        if i >= stop:
            break
        # i < stop
        if (i - start) % step == 0:
            yield obj


def getitem(data, *indices, default=None):
    for i in indices:
        if data is None:
            return default

        if isinstance(i, int):
            if i >= len(data):
                return default
        else:
            if i not in data:
                return default

        data = data[i]

    return data


def splice(arr, index, num, *args):
    assignment = []
    insertion = []

    for i, arg in enumerate(args):
        if i < num:
            assignment.append(arg)
        else:
            insertion.append(arg)

    if len(assignment) < num:
        num = len(assignment)
        arr[index: index + num] = assignment
        del arr[index + num:]
    else:
        arr[index: index + num] = assignment

        index += num
        for arg in insertion:
            arr.insert(index, arg)
            index += 1

    return arr


def split_filename(filename):
    extIndex = filename.rindex('.')
    return filename[:extIndex], filename[extIndex + 1:]


def json_to_array(json):
    if isinstance(json, list):
        return [json_to_array(data) for data in json]

    if isinstance(json, dict) and all(isinstance(index, int) or index.isdigit() for index in json):
        arr = []
        for index in json:
            setitem(arr, int(index), json_to_array(json[index]))

        return arr

    return json


def toggleCase(s):
    return ''.join(ch.upper() if ch.islower() else ch.lower() if ch.isupper() else ch for ch in s)


def clip(this, min, max):
    if this < min:
        return min

    if this > max:
        return max

    return this


def deleteIndices(arr, fn, postprocess=None):
    indicesToDelete = []
    is_binary = fn.__code__.co_argcount > 1
    for i in range(len(arr)):
        if fn(arr, i) if is_binary else fn(arr[i]):
            indicesToDelete.append(i)

    if postprocess:
        is_binary = postprocess.__code__.co_argcount > 1

    if indicesToDelete:
        indicesToDelete.reverse()

        if not isinstance(arr, list):
            arr = [*arr]

        for i in indicesToDelete:
            if postprocess:
                if is_binary:
                    postprocess(arr, i)
                else:
                    postprocess(arr[i])
            del arr[i]

        return arr


def batches(data, batch_size):
    if isinstance(data, (types.GeneratorType, tqdm)):
        batch = []
        for args in data:
            batch.append(args)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
    else:
        size = len(data)
        divisor = int((size + batch_size - 1) / batch_size)
        if divisor:
            quotient = int(size / divisor)
            sizes = [quotient] * divisor

            for i in range(size % divisor):
                sizes[i] += 1
            
            # assert sum(sizes) == size
            start = 0
            for length in sizes:
                stop = start + length
                yield data[start: stop]
                start = stop
            # assert stop == size
        else:
            yield data

def flatten(data):
    result = []
    for arr in data:
        result += arr

    return result


def is_same(list):
    if isinstance(list, types.GeneratorType):
        list = [*list]
    for i in range(1, len(list)):
        if list[i] != list[i - 1]:
            return False

    return True


@unique
class Enum(Enum):
    def __new__(cls):
        value = len(cls.__members__)

        if not value:
            cls.members = []

        obj = object.__new__(cls)
        obj._value_ = value

        cls.members.append(obj)
        return obj

    @property
    def type(self):
        return self.name.split('_')[0]


def merge_sort(arr1, arr2, compareTo=None, ret=None):
    if ret is None:
        ret = Array()

    if compareTo is None:
        compareTo = lambda a, b: a - b

    _merge_sort(arr1, len(arr1), arr2, len(arr2), compareTo, ret)

    return ret


# precondition: the destine array is not the same as the source arrays;
def _merge_sort(arr1, sz1, arr2, sz2, compareTo, dst):
    i = 0
    j = 0
    k = 0
    while i < sz1 and j < sz2:
        if compareTo(arr1[i], arr2[j]) < 0:
            dst[k] = arr1[i]
            i += 1
        else:
            dst[k] = arr2[j]
            j += 1

        k += 1

    while i < sz1:
        dst[k] = arr1[i]
        k += 1
        i += 1

    while j < sz2:
        dst[k] = arr2[j]
        k += 1
        j += 1


def items(dict, **kwargs):
    [*dict] = dict.items()
    dict.sort(key=lambda args: args[0], **kwargs)
    return dict


def fromEntries(*args, object=True):
    obj = Object() if object else {}

    if len(args) > 1:
        for i in range(0, len(args), 2):
            obj[args[i]] = args[i + 1]
    else:
        args, = args
        for key, value in args:
            obj[key] = value

    return obj


def array_split(self, pivot):
    if isinstance(pivot, int):
        return self[:pivot], self[pivot:]

    if isinstance(pivot, slice):
        start, stop, step = pivot.start, pivot.stop, pivot.step
        if step is None:
            step = 1

        if step > 0:
            if start is None:
                start = 0
            elif start < 0:
                start += len(self)

            if stop is None:
                stop = len(self)
            elif stop < 0:
                stop += len(self)

            if step > 1:
                rest = (self[i] for i in {*range(start, stop)} - {*range(start, stop, step)})
                rest = self[:start] + type(self)(rest) + self[stop:]
            else:
                rest = self[:start] + self[stop:]

            return self[pivot], rest
        else:
            if start is None:
                start = len(self) - 1
            elif start < 0:
                start += len(self)

            if stop is None:
                stop = -1
            elif stop < -1:
                stop += len(self)

            if step < -1:
                rest = (self[i] for i in {*range(start, stop, -1)} - {*range(start, stop, step)})
                rest = self[:stop + 1] + type(self)(rest) + self[start + 1:]
            else:
                rest = self[:stop + 1] + self[start + 1:]

            return rest, self[pivot]

    former = []
    latter = []
    for arg in self:
        if pivot(arg):
            former.append(arg)
        else:
            latter.append(arg)
    return former, latter


def array_merge(*array):
    if len(array) == 1:
        array, = array
    for array in array:
        yield from array


def parse_args(argv, args, kwargs):
    # print('in parse_args')
    # print('argv =', argv)
    # print('args =', args)
    # print('kwargs =', kwargs)

    for i, arg in enumerate(argv):
        if arg.startswith('--'):
            args.extend(argv[:i])
            return parse_kwargs(argv[i:], args, kwargs)
    else:
        args.extend(argv)


def parse_kwargs(argv, args, kwargs):
    # print('in parse_kwargs')
    # print('argv =', argv)
    # print('args =', args)
    # print('kwargs =', kwargs)
    def get_val(value):
        try:
            return eval(value)
        except:
            return value

    name = None
    for i, arg in enumerate(argv):
        if arg.startswith('--'):
            if name is not None:
                if kwargs[name] is None:
                    kwargs[name] = True

            name = arg[2:]
            if '=' in name:
                index = name.index('=')
                name, arg = name[:index], name[index + 1:]
                kwargs[name] = get_val(arg)
                name = None
        elif name is None:
            return parse_args(argv[i:], args, kwargs)

        elif name in kwargs:
            if not isinstance(kwargs[name], list):
                kwargs[name] = [kwargs[name]]
            kwargs[name].append(get_val(arg))
        else:
            kwargs[name] = get_val(arg)

    if name is not None:
        if kwargs[name] is None:
            kwargs[name] = True

    return kwargs


def argparse():
    argv = sys.argv[1:]
    args = []
    kwargs = Object()
    parse_args(argv, args, kwargs)

    for key in [*kwargs.keys()]:
        _key = key.replace('-', '_')
        if _key != key:
            kwargs[_key] = kwargs.pop(key)

    return args, kwargs


def kill():
    pid = os.getpid()
    if is_Linux():
        os.system(f"kill -9 {pid}")
    else:
        os.system(f"taskkill /F /pid {pid}")


def list_to_tuple(array):
    if isinstance(array, list):
        return tuple(list_to_tuple(a) for a in array)
    return array


if __name__ == '__main__':
    arr = [*range(10)]
    former, latter = array_split(arr, slice(-2, -8, -2))
    print(former)
    print(latter)

