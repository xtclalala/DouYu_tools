# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  14:52

class Singleton(type):
    """
    学习记录一下，万一有什么用，可以帮助使用
    利用 type 创建类，来实现单例，_instances 是类属性，在实例化一次之后再次调用，不会执行再 __init__方法
    代码演示：
    class A(metaclass=Singleton):
        def __init__(self):
            print('this is A __init__')
                                    对应结果：
    a1 = A()                                    this is A __init__
    a2 = A()
    a3 = A()
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]