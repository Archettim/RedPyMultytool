from cryptography.fernet import Fernet

def Key_gen():
    with open("filekey.key","wb") as key:
        key.write(Fernet.generate_key())

def CipherFile(key):
    ferCP=Fernet(key)
    with open("target.txt","rb") as plain:
        p=plain.read()
        print(p)
    with open("target.txt","wb") as orig:
        orig.write(ferCP.encrypt(p))

def DecipherFile(key):
    ferDC=Fernet(key)
    with open("target.txt","rb") as cryp:
        dc=cryp.read()
        print(dc)
    with open("target.txt","wb") as rest:
        rest.write(ferDC.decrypt(dc))
    

if __name__=="__main__":
    Key_gen()
    with open("filekey.key","r") as key: k=key.read()
    CipherFile(k)
    DecipherFile(k)
