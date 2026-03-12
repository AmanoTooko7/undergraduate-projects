#用于移除myString中的重复字母
def removeDupes(myString):
    newStr = ""
    for ch in myString:
        if ch not in newStr:
            newStr = newStr + ch

    return newStr


#用于移除字符串myString中的removeString字符串
def removeMatches(myString, removeString):
    newStr = ""
    for ch in myString:
        if ch not in removeString:
            newStr  = newStr + ch

    return newStr


alphabet = "abcdefghijklmnopqrstuvwlyz "
a=removeMatches(alphabet, removeDupes("wonder woman"))
print(a)
