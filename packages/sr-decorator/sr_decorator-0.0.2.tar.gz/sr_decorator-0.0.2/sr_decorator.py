__version__ = "0.0.2"

def DEBUG(data):
    def decorator(func):
        def wrapper(*args,**kwargs):
            print(f"[DEBUG]开始执行[{data}]函数")
            res = func(*args,**kwargs)
            print(f"[DEBUG]函数[{data}]执行结束")
            return res
        return wrapper
    return decorator

def EMAP(data):
    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs_tuple = tuple(sorted(kwargs.items()))
            cache_key = (args, kwargs_tuple)
            if cache_key in data:
                return data[cache_key]
            else:
                tmp = func(*args, **kwargs)
                data[cache_key] = tmp
                return tmp
        return wrapper
    return decorator
