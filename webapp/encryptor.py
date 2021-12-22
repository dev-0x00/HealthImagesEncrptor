import os
import random
import struct
import time
import keyGen
import argparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encryptFile(key, plainFile, cipherFile, chunkSize=64*1024):
    
    '''
    This function encrypts a file using AES(CBC mode)
    in this mode the Key must be either 16, 24 or 34 bytes long longer keys are more secure
    the chunkSize must be divisible by 16
    '''
 
    iv = bytes([random.randint(0, 0xFF) for i in range(16)])
    #iv = get_random_bytes(16)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    fileSize = os.path.getsize(plainFile)

    with open(plainFile, 'rb') as plainfile:
        with open(cipherFile, 'wb') as cipherfile:
            cipherfile.write(struct.pack('<Q', fileSize))
            cipherfile.write(iv)

            while True:
                chunk = plainfile.read(chunkSize)
                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                cipherfile.write(encryptor.encrypt(chunk))
    return cipherfile

'''def main():

    #key = b'bdc635k2-283d-4a2c-a477-339ea866'
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f', action='store_true', help='file to encrypt')
    args = parser.parse_args()
    key = keyGen.generateKey()
    
    plainFile = args.file
    cipherText = plainFile + ".enc"
    encryptFile = (key, plainFile, cipherText)
    keyGen.saveKay(key)
    with open(key, 'rb') as secrete:
        content = secrete.read()
        print("[INFO] keys veryfied...")
        time.sleep(2)
        plainFile = raw_input('[*]Enter the file to Encrypt: ')
        cipherText = plainFile + ".enc"
        time.sleep(2)
        print("[INFO] Encrypting file. this will take a minuite...")
        encryptFile(content, plainFile ,cipherText)
        time.sleep(2)
        print("[INFO] file encrypted and saved in " + cipherText)
        secrete.close()
        '''

#incase the file is imported as module
if __name__ == '__main__':
    encryptFile()
