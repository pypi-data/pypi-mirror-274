import numpy as np
import random, os


def extend(arr, mask, maxlength, padding_side):
    if isinstance(arr, (tuple, np.ndarray)):
        arr = [*arr]

    padding = [mask] * (maxlength - len(arr))
    if padding_side == 'right':
        arr.extend(padding)
    elif padding_side == 'left':
        arr = padding + arr
    else:
        for mask in padding:
            arr.insert(random.randrange(0, len(arr)), mask)

    return arr


def extend_right(arr, mask, max_length):
    if isinstance(arr, tuple):
        arr = [*arr]

    padding = [mask] * (max_length - len(arr))

    arr.extend(padding)

    return arr


def padding_right(arr, mask_value=0):
    maxWidth = max(len(x) for x in arr)
    # arr is a 2-dimension array
    for i in range(len(arr)):
        arr[i] = extend_right(arr[i], mask_value, maxWidth)
    return np.array(arr)


def padding_left(arr, mask_value=0):
    return padding(arr, mask_value, padding_side='left')


def get_padding_left(input_ids):
    try:
        i = 0
        while True:
            if any(input[i] for input in input_ids):
                return i
            i += 1
    except IndexError:
        raise Exception('input with the minimum length consists of all zeros!')


def padding(arr, mask_value=0, padding_side='right', dtype=None):
    '''
    
    :param arr:
    :param mask_value:
    :param shuffle: randomly insert the padding mask into the sequence！ this is used for testing masking algorithms!
    '''

    try:
        maxWidth = max(len(x) for x in arr)
    except (TypeError, AttributeError) as _:
        return np.array(arr, dtype=dtype)

    try:
        maxHeight = max(max(len(word) for word in x) for x in arr)
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                arr[i][j] = extend(arr[i][j], mask_value, maxHeight, padding_side)
            arr[i] = extend(arr[i], [mask_value] * maxHeight, maxWidth, padding_side)
    except (TypeError, AttributeError, ValueError) as _:

        # arr is a 2-dimension array
        try:
            for i in range(len(arr)):
                arr[i] = extend(arr[i], mask_value, maxWidth, padding_side)
        except AttributeError as _:
            #arr might be an array of string
            ...

    return np.array(arr, dtype=dtype)


def randomize(data, count):
    from std.combinatorics import random_combination
    for i in random_combination(len(data) - 1, min(count, len(data) - 1)):
        assert len(data) - i > 1
        j = random.randrange(1, len(data) - i) + i # j > i
        data[i], data[j] = data[j], data[i]

    return data


def sample(data, count):
    '''
    this sampling ensure dislocation arrangement
    '''
    
    if count <= len(data):
        for i in range(count):
            if 1 < len(data) - i:
                j = random.randrange(1, len(data) - i) + i # j > i
                data[i], data[j] = data[j], data[i]

        if count < len(data):
            data = data[:count]
        return data
    quotient, remainder = count // len(data), count % len(data)
    if remainder:
        return sample(data * quotient + sample(data[:], remainder), count)
    else:
        return sample(data * quotient, count)


def create_memmap(filename, mode='r'):
    dtype = np.dtype(filename[filename.rindex('.') + 1:])
    return np.memmap(
        filename,
        dtype=dtype,
        mode=mode,
        shape=(os.path.getsize(filename) // dtype.alignment,))


def get_len_padded(input):
    for i, id in enumerate(input):
        if id:
            return i

def get_seq_length(input):
    return len(input) - get_len_padded(reversed(input))


if __name__ == '__main__':
    count = 22
    data = [*range(10)]
    data_sampled = sample(data, count)
    print(data_sampled)
    assert len(data_sampled) == count
    
    if len(data) < count:
        assert {*data} & {*data_sampled} == {*data}
    