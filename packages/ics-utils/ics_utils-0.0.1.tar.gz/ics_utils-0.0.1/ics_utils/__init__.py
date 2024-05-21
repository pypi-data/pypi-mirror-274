# -*- coding: utf-8 -*-
"""
@author: hanyanling
@date: 2024/5/21 下午5:32
@email:
---------
@summary:
"""
import sys
import atexit
import time


# 自定义任务执行时间
def timing(func=None):
    if func:
        # 被当做装饰器使用时
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"方法 '{func.__name__}' 的执行时间为: {end_time - start_time} 秒")
            return result
        return wrapper

    else:
        # 记录任务开始时间
        start_time = time.time()
        def __exit():
            # 记录任务结束时间
            end_time = time.time()
            print(f"本次任务 的执行时间为: {end_time - start_time} 秒")
        atexit.register(__exit)

timing(None)

# 自定义注册异常退出
def custom_excepthook(exc_type, exc_value, exc_trace):
    # TODO 异常消息处理，发送企微或邮件
    pass
    sys.__excepthook__(exc_type, exc_value, exc_trace)


sys.excepthook = custom_excepthook