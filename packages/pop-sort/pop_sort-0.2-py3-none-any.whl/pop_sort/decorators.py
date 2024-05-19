def reverse_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        reverse = kwargs.get('reverse', False)
        if reverse:
            return result[::-1]
        return result

    return wrapper
