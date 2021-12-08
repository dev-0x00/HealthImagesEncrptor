import os
import random
import base64
import time
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class mainClass(object):

    def __init__(self):
        pass
    
    def DirectoryListing(self, path):
        Directories = {
                "Directory": [], 
                "File": []
                }
        directories = os.listdir(path)
        for path in directories:
            if os.path.isdir(path):
                Directories["Directory"].append(path) 
            elif os.path.isfile:
                Directories["File"].append(path)
                  
        return(Directories)

    def GenerateKey(self):
        generateSecret = hex(random.getrandbits(128))
        secretKey = ''.join(list(str(generateSecret))[:16]).encode()
        return secretKey
    

    def Encryptor(self, plainFile, chunkSize=64*1024):
        key = self.GenerateKey()
        filePath = plainFile
        iv = bytes([random.randint(0, 0xff) for i in range(16)])
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        fileSize = os.path.getsize(plainFile)
       

        with open(plainFile, 'rb') as plainFile:
            directory = filePath.split("/")[:-1]
            cipherFilePath =  filePath.split("/")[-1] + ".enc"
            directory.append(cipherFilePath)
            cipherFile = "/".join(directory)
            print(cipherFile)
            with open(cipherFile, 'wb') as cipherFile:
                cipherFile.write(struct.pack('<Q', fileSize))
                cipherFile.write(iv)

                while True:
                    chunk = plainFile.read(chunkSize)
                    if len(chunk) == 0:
                        break

                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    cipherFile.write(encryptor.encrypt(chunk))
            os.system("rm {}".format(filePath))
        return cipherFile

    def Decryptor(self, cipherFile, chunkSize=64*1024):
        key = self.GenerateKey()
        filePath = cipherFile
        print(filePath)
        with open(cipherFile, 'rb') as cipherFile:
            originalSize = struct.unpack('<Q', cipherFile.read(struct.calcsize('Q')))[0]
            iv = cipherFile.read(16)
            decryptor = AES.new(key.decode(), AES.MODE_CBC, iv)

            directory = filePath.split("/")[:-1]
            plainFilePath = filePath.split("/")[-1].split(".")[-1]
            print(directory, plainFilePath)
            plainFile = ".".join(plainFilePath) 
            directory.append(plainFile)
            plainFile = "/".join(directory)

            with open(plainFile,'wb') as plainFile:
                while True:
                    chunk = cipherFile.read(chunkSize)
                    if len(chunk) == 0:
                        break
                    plainFile.write(decryptor.decrypt(chunk))
                plainFile.truncate(originalSize)
            os.system("rm {}".format(filePath))
        return plainFile





if __name__ == "__main__":
    serve = mainClass()
    serve.Encryptor("/home/dev/personalProjects/inovators/johnBCSF/archive/chest.jpeg")
