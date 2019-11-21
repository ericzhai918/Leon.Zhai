
'''
1.不带括号时，调用的是这个函数本身 ，是整个函数体，是一个函数对象，无需等该函数执行完成
2.带括号（参数或者无参），调用的是函数的执行结果，需等该函数执行完成的结果
'''
def bracket(data):
    return data

funcbody = bracket
funcvalue = bracket(7)

print(funcbody)
print(funcvalue)