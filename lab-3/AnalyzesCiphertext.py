import Warm_Up as C 
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
def AnalyzesCipherText(Cipher):
    Length = len(Cipher)
    occurrences ={}
    for c in Cipher : 
        if not(c.isalpha()) : 
            continue
        if c in occurrences :
             occurrences[c]=occurrences[c]+1
        else:
             occurrences[c] = 1
    #percentage:
    percentage = {}
    for O in occurrences :
        percentage[O] = occurrences[O]/Length
    for char, pct in sorted(percentage.items(), key=lambda x: x[1] ,reverse=True):
        print(f"{char}: {pct:.2f}%")

def AnswerOfRoom1():
     print("-------------------------------------------------------------")
    # the cipher for the Room 1 
     cipher = list("EKT YTJRTE BTYYQFT PY KPZZTO PO EKPY NQRQFRQNK.STEETR GRTCVTOJD ZXTY OXE RTHTQS EKT IKXST LTD,MVE PE FPHTY Q FXXZ YEQRE.SXXL GXR JXBBXO IXRZY, RTNTQETZ NQEETROY,QOZ YKXRE IXRZY.IKTO DXV RTJXHTR EKT BTYYQFT,EKT HPFTOTRT LTD KQY GXVR STEETRY.")
    # cipher = list("VVHWGQUIVYHIRSUPGTWXJSVIPCWIUPHGCIVIVVHPGHWITSDTRSDVUSYITMZLGFHIXSUCVSDQOSPFGFVLQIOHEVHGMSDGJQRPWAQWGSNXJSPSUHIVGEXIPHVCOPRPCBGYUSLXVCUIECYITHKIMSBAJSQXJSPIUGDKGPHGQAHWEZHETSQXGFWLGOFGGGVAQFGIEZLTUS.")
     print("the cipher text : ","".join(cipher))
     print("-------------------------------------------------------------")
     for i in range(len(cipher)):
            if cipher[i] == 'T':
                cipher[i] = 'e'
            elif cipher[i] == 'E':
                cipher[i] = 't'
            elif cipher[i] == 'K':
                cipher[i] = 'h'
            elif cipher[i] == 'Y':
                cipher[i] = 's'
            elif cipher[i] == 'P':
                cipher[i] ='i'
            elif cipher[i] == 'R':
                cipher[i] ='r'
            elif cipher[i] == 'J':
                cipher[i] ='c'
            elif cipher[i] == 'Q':
                cipher[i] ='a'
            elif cipher[i] == 'O':
                cipher[i] ='n'
            elif cipher[i] == 'N':
                cipher[i] ='p' 
            elif cipher[i] == 'F':
                cipher[i] ='g'  
            elif cipher[i] == 'Z':
                cipher[i] ='d'   
            elif cipher[i] == 'B':
                cipher[i] ='m'
            elif cipher[i] == 'X':
                cipher[i] ='o'
            elif cipher[i] == 'I':
                cipher[i] ='w'
            elif cipher[i] == 'H':
                cipher[i] ='v'
            elif cipher[i] == 'S':
                cipher[i] ='l'
            elif cipher[i] == 'M':
                cipher[i] ='b'
            elif cipher[i] == 'V':
                cipher[i] ='u'            
            elif cipher[i] == 'G':
                cipher[i] ='f'
            elif cipher[i] == 'L':
                cipher[i] ='k'
            elif cipher[i] == 'M':
                cipher[i] ='m'
            elif cipher[i] == 'D':
                cipher[i] ='y'
            elif cipher[i] == 'C':
                cipher[i] ='q'
             
             
     print ("the orginal text :", "".join(cipher))
     print("-------------------------------------------------------------")

def AnswerOfRoom2():
    print("-------------------------------------------------------------")
    cipher = list("VVHWGQUIVYHIRSUPGTWXJSVIPCWIUPHGCIVIVVHPGHWITSDTRSDVUSYITMZLGFHIXSUCVSDQOSPFGFVLQIOHEVHGMSDGJQRPWAQWGSNXJSPSUHIVGEXIPHVCOPRPCBGYUSLXVCUIECYITHKIMSBAJSQXJSPIUGDKGPHGQAHWEZHETSQXGFWLGOFGGGVAQFGIEZLTUS")
    group1= cipher[0::4]
    group2= cipher[1::4]
    group3= cipher[2::4]
    group4= cipher[3::4]
    #we find tat the code is the key 
    for i in range(len(cipher)):
        if i % 4 ==0:
            cipher[i] = C.Decrypt(cipher[i],2)
        elif i % 4 ==1:            
            cipher[i] = C.Decrypt(cipher[i],14)
        elif i % 4 ==2:            
            cipher[i] = C.Decrypt(cipher[i],3)
        elif i % 4 ==3:            
            cipher[i] = C.Decrypt(cipher[i],4)
    print()
    print("the key : code")
    print()
    print("the text without space : ", "".join(cipher))
    print()
    print("the text with space : The secret keeper left these notes because the letter E appears everywhere. Every team member should check each column, seek the most frequent symbol, and use it to recover the key. When the message becomes clear, enter the access word ECLIPSE.")
    print()
    print("access word : ECLIPSE")
    print()
    print("--------------------------------------------------------------")
      

if __name__ == "__main__":
     #AnswerOfRoom1()
     AnswerOfRoom2()