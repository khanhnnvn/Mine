__author__ = 'namhb1'

import binascii, base64
str 		=	"49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
hexStr 		=	binascii.unhexlify(str)
b64Str 		=	base64.b64encode(hexStr)

print("Result: {}".format(b64Str))
