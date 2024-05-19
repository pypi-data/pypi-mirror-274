__version__ = "0.0.1"

def DEBUG(data):
    def decorator(func):
        def wrapper(*args,**kwargs):
            print(f"[DEBUG]开始执行[{data}]函数")
            res = func(*args,**kwargs)
            print(f"[DEBUG]函数[{data}]执行结束")
            return res
        return wrapper
    return decorator
