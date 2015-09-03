__author__ = 'namhb1'

from Crypto.Cipher import AES
import binascii, struct


def encrypt(key, text, iv):
    encrypt_suite = AES.new(key, AES.MODE_ECB, iv)
    cipher = encrypt_suite.encrypt(text)
    return cipher
def decrypt(key, cipher, iv):
    decrypt_suite = AES.new(key, AES.MODE_ECB, iv)
    data = decrypt_suite.decrypt(cipher)
    return data
def padding(data, block_size=16):
    x, y = divmod(len(data),block_size)
    if y!=0:
        length = block_size - (len(data) % block_size)
        for i in range(1,length+1):
            data.append(length)
    return struct.pack('b'*len(data), *data)

def string2byte(text):
    return list(ord(c) for c in text)



key     =   "K"*16
iv      =   "A"*16

text    =   "Encrypt me nw"
block_size = 16

#print len(string2byte(text))
#print (padding(string2byte(text)))
#print len(padding(text))
a = (encrypt((key),padding(string2byte(text)),(iv)))

b = (decrypt((key),a,(iv)))
print string2byte(b)
