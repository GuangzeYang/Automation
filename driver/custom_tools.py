import functools
from loguru import logger


def exception_is_executed_log(is_ignore_exception=False):
    def is_executed_log(func):
        """为函数添加是否正常执行的日志"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(f'{func.__module__}-{func.__name__} is starting execution...')
                res = func(*args, **kwargs)
                logger.debug(f'{func.__module__}-{func.__name__} is finished execution.')
            except Exception as e:
                logger.debug(f'{func.__module__}-{func.__name__} raise an exception: {e}.')
                if not is_ignore_exception: raise e
                res = None
            return res
        return wrapper
    return is_executed_log