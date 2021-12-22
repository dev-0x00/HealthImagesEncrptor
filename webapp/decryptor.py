import os
import random
import struct

from Crypto.Cipher import AES

def decryptCipher(key, cipherfile, plainfile, chunksize=64*1024):
    '''
    This function decrypts a file using AES CBC mode with the given 16 bit key
    '''

    with open(cipherfile, 'rb') as  cipher:
        originalSize = struct.unpack('<Q', cipher.read(struct.calcsize('Q')))[0]
        iv = cipher.read(16)
        decryptor = AES.new(key.decode(), AES.MODE_CBC, iv)

        with open(plainfile, 'wb') as  plaintext:
            while True:
                chunk = cipher.read(chunksize)
                if len(chunk) == 0:
                    break
                plaintext.write(decryptor.decrypt(chunk))
            plaintext.truncate(originalSize)
    return plaintext

def main():

    #key = b'bdc635k2-283d-4a2c-a477-339ea866'
    key = input('[*]Enter the key file: ')
    with open(key, 'rb') as secrete:
        content = secrete.read()
        cipherText = input('[*]Enter the file to decrypt: ')
        plain = cipherText.split('.')
        plainText = []
        plainText.append(plain[0])
        plainText.append('.')
        plainText.append(plain[1])
        plainText = ''.join(plainText)
        decryptCipher(content, cipherText, plainText)
        secrete.close()
        

#incase the file is not run a module
if __name__ == '__main__':
    main()

