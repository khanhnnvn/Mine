__author__ = 'namhb1'
import binascii, base64


def xor(hexstr, key):
	result 		=	""
	for i in range(0,len(hexstr)):
		tmp		=	ord(hexstr[i]) ^ key
		result	+=	chr(tmp)
	print(result)

str1 		=	"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
hexstr1		=	binascii.unhexlify(str1)
for i in range(0, 255):
	print("Use key: {}".format(i))
	xor(hexstr1, i)

# key = 88
