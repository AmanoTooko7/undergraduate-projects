from string import ascii_lowercase
alphabet = ascii_lowercase + ""

def substitutionEncrypt(plainText, key):
    plainText = plainText.lower()
    cipherText =  " "
    for ch in plainText:
        idx = alphabet.find(ch)
        cipherText = cipherTxet + key[idx]
        
    return cipherText
