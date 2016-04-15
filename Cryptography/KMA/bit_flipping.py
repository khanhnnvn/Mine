import binascii
str = "1694e473cc3571ea1f374c1cfd37a52ea21b3402e5ffd3cfa9e9804a3ec7785f596897888011addddc3a3220c83f08ba942ee7f836e8323ba8d86fd1f49fa0ef"
iv=binascii.unhexlify(str)
iv = list(iv)
tmp = ord(iv[10]) ^ ord("0") ^ ord("1")
print(tmp)
iv[10] = chr(tmp)
print "".join(iv).encode("hex")