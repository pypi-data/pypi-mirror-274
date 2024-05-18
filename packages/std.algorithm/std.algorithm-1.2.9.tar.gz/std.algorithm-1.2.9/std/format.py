import sys
from math import ceil, log10, floor


def get_format_args(is_positive, abs_num, format):
    if is_positive is None:
        return format, abs_num

    exponent = floor(log10(abs_num))
    num = abs_num * 10 ** -exponent
    float_points = 0
    if is_positive_exponent := exponent > 0:
        exponent_abs = exponent
    else:
        exponent_abs = -exponent
    if is_positive:
        if exponent_abs < 10:
            float_points += 1
            num = min(num, 9.9)
        else:
            if exponent_abs < 100:
                format = '+' + format
            num = min(num, 9)
    else:
        exponent_abs = min(99, exponent_abs)
        num = min(num, 9)
    return format % float_points, (num, exponent_abs if is_positive_exponent else -exponent_abs)


def format_number(num, ANSI=None):
    if isinstance(num, int):
        format = '%6d'
    else:
        abs_num = abs(num)
        if abs_num >= 1e3:
            if is_positive := num > 0:
                num = min(num, sys.float_info.max)
                format = "%%1.%dfe+%%d"
                abs_num = num
            else:
                num = max(num, -sys.float_info.max)
                format = "-%%1.%dfe+%%02d"
                abs_num = -num

            format, num = get_format_args(is_positive, abs_num, format)
        elif abs_num <= 1e-3:
            if is_positive := num > 0:
                num = max(num, sys.float_info.min)
                format = "%%1.%dfe%%d"
                abs_num = num
            elif num:
                num = min(num, -sys.float_info.min)
                format = "-%%1.%dfe%%03d"
                abs_num = -num
            else:
                format = '%6.4f'
                abs_num = 0.0
                is_positive = None

            format, num = get_format_args(is_positive, abs_num, format)
        else:
            if num > 0:
                n = 6
                num_digits = log10(num)
                num_digits_ceil = ceil(num_digits)
                d = 5 - max(1, num_digits_ceil)
                if num_digits == num_digits_ceil:
                    if num_digits_ceil >= 0:
                        d -= min(num_digits_ceil, 1)
                elif num >= 10 ** num_digits_ceil - 5 * 10 ** (num_digits_ceil - 6):
                    d -= 1
            else:
                n = 5
                if num:
                    num_digits = log10(-num)
                    num_digits_ceil = ceil(num_digits)
                    d = 4 - max(1, num_digits_ceil)
                    if num_digits == num_digits_ceil:
                        if num_digits_ceil >= 0:
                            d -= min(num_digits_ceil, 1)
                    elif num <= -10 ** num_digits_ceil + 5 * 10 ** (num_digits_ceil - 5):
                        d -= 1
                        if not d:
                            d = 1
                            num += 9 * 10 ** (1 - num_digits_ceil)
                else:
                    d = 3
            format = f'%{n}.{max(d, 0)}f'
    text = format % num
    assert len(text) == 6, num
    if ANSI:
        text = f'{ANSI[0]}{text}{ANSI[1]}'
    return text


def format_dict(obj, ANSI=None):
    return [f"{name}: {format_number(value, ANSI)}" for name, value in obj.items()]


def format_time(ss, width=1):
    left_justification = 0
    mm, args = divmod(ss, 60)
    if mm:
        left_justification += 1
        HH, mm = divmod(mm, 60)
        format = ':%02d'
        args = mm, args
        if HH:
            left_justification += 1
            d, HH = divmod(HH, 24)
            format = ':%02d' + format
            args = HH, *args
            if d:
                left_justification += 1
                format = ' %02d' + format
                args = d, *args
    else:
        format = 's'
    return f'%{max(width - left_justification * 3, 1)}d{format}' % args


if __name__ == '__main__':
    import numpy
    assert format_number(0.0)[0] != ' '
    args = []
    for t in range(1, 10):
        args += [10 - t * 10 ** -i for i in range(1, 10)]
    
    args += [90 + arg for arg in args] + [990 + arg for arg in args] + [9990 + arg for arg in args]
    
    for i in range(0, 309):
        args.append(i * 1.0)
        for num in numpy.arange(1.0, 10.1, 0.1):
            args.append(num * 10 ** -i)
            args.append(num * 10 ** i)

    for num in args + [-arg for arg in args]:
        try:
            assert format_number(num)[0] != ' '
        except:
            print(format_number(num))
