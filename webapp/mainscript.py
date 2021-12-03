import os
import random
import base64
import time
import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class mainClass():
    
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

    def GenerateKey():
        generateSecret = random.getrandbits(128).hex()
        secretKey = ''.joint(list(str(generateSecrete))[:16]).encode()
        return secretKey

    def Encryptor(plainFile, chunckSize=64*1024):
        iv = bytes([random.randint(0, 0xff) for i in range(16)])
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        fileSize = os.path.getsize(plainFile)
        key = GenerateKey()

        with open(plainFile, 'rb') as plainFile:
            directory = plainFile.split("/")[:-1]
            cipherFilePath =  "." + plainFile.split("/")[-1]
            cipherFile = (directory.append(cipherFilePath))
            cipherFile = "/".join(cipherFile)
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

        return cipherFile

    def Decryptor(cipherFile, chunkSize=64*1024):
        key = GenerateKey()
        with open(cipherFile, 'rb') as cipherFile:
            originalSize = struct.unpack('<Q', cipher.read(struct.aclcsize('Q')))[0]
            iv = cipher.read(16)
            decryptor = AES.new(key.decode(), AES.MODE_CBC, iv)

            directory = cipherFile.split("/")[:-1]
            plainFilePath = cipherFile.split("/")[-1].split(".")
            palinFilePath.pop(0)
            plainFile = ".".join(plainFile)  
            plainFile = directory.append(plainFilePath)
            plainFile = "/".join(directory)

            with open(plainFile,'wb') as plainFile:
                while True:
                    chunk = cipher.read(chunkSize)
                    if len(chunk) == 0:
                        break
                    plainFile.write(decryptor.decrypt(chunk))
                plainFile.truncate(originalSize)

        return plainFile





if __name__ == "__main__":
    serve = mainClass()
    serve.DirectoryListing(os.getcwd())
