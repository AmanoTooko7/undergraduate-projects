def Leibniz(terms):
    acc = 0
    num = 4
    den = 1
    k = 1

    for aTerm in range(terms):
        nextTerm = num / den* k
        acc = acc + nextTerm
        den = den + 2
        k=k* (-1)

    return acc
