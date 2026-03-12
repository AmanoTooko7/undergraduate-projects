def genKeyFromPass(password):
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    #转为小写并去除字符串中相同的字母
    password = password.lower()
    password = removeDupes(password)

    lastChar = password[-1]
    lastidx = alphabet.find(lastChar)

    afterString = removeMatches(alphabet[lastidx + 1:], password)
    beforeString =  removeMatches(alphabet[:lastidx], password)

    key = password + afterString + beforeString
    return key
