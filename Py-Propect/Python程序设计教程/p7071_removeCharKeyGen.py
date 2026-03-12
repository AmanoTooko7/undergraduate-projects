#此函数用于除去字符串string中位置为idx的字符
def removeChar(string, idx):
    return string[:idx] + string[idx+1:]

#从alphabet中生成一个随机秘钥
def keyGen():
    import random        #此模块用于使用randint
    alphabet = "abcdefghijklmnopqrstuvwxyz "#共27个字符
    key = ""
    for i in range(len(alphabet)-1, -1, -1):#range中的条件是由26递减1一直到-1+1=0
        idx = random.randint(0, i)   #随机生成0到i中的任何整数
        key = key + alphabet[idx]
        alphabet = removeChar(alphabet, idx)

    return key
