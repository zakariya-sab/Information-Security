#a small program Encrypt and  decrypt the message.
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

#encrypt
def Encrypt(Message,k):
    result = ""
    for  m in Message :
        if m == ' ':
             result = result + ' ' 
        else: 
            position = alphabet.index(m)
            result = result + alphabet[(position+k) % 26]  
    return result
#decrypt
def Decrypt(Chper,k):
    result = ""
    for c in Chper :
        if c == ' ':
             result = result + ' '
        elif c.isalpha() == False :
            continue 
        else: 
            position = alphabet.index(c)
            result = result + alphabet[(position-k) % 26]  
    return result

if __name__ == "__main__":
#     print(Encrypt("CRYPTO IS FUN UNTIL THE PROFESSOR SAYS QUIZ",4))
#     print("------------------------------------------------------------")
    text = "xmjnndiboczmpwdxjizaukqzbt"
    text = text.upper()
    for i in range(26):
        resutl = Decrypt(text,i)
        print(f"{i}:{resutl.lower()}")
