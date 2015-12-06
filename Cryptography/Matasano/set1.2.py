__author__ = 'namhb1'

import binascii, base64
str1 		=	"1c0111001f010100061a024b53535009181c"
str2		=	"686974207468652062756c6c277320657965"
hexStr1 	=	binascii.unhexlify(str1)
hexStr2 	=	binascii.unhexlify(str2)
length 		=	len(hexStr1)
result 		=	""
for i in range(0, length):
	tmp 	=	ord(hexStr1[i]) ^ ord(hexStr2[i])
	result 	+= 	chr(tmp)

result 		=	binascii.hexlify(result)

