
'''测试__all__变量的模块'''
def hello():
    print("Hello, Python")

def world():
    print("Pyhton World is funny")

def test():
    print('--test--')

# 定义__all__变量，指定默认只导入hello和world两个成员
__all__ = ['hello', 'world']