import requests, re, binascii, string
cookie = "1694e473cc3571ea1f374c1cfd37a52ea21b3402e5ffd3cfa9e9804a3ec7785f596897888011addddc3a3220c83f08ba942ee7f836e8323ba8d86fd1f49fa0ef"
blockSize = 32
num = 128/blockSize
stringText = "0123456789abcdef"
url = "http://42.112.213.90:8011/"


# iv = cookie[:blockSize]
# # firstBlock = cookie[blockSize:blockSize*2]
# firstBlock = cookie[blockSize:]
# prefix = "0"*(blockSize-1)
# for i in range(0, 16):
# 	tmp = prefix + stringText[i]
# 	attackPayload = tmp + firstBlock
# 	r = requests.get(url, cookies={'flag_auth': tmp})
# 	print r.headers["content-length"]

# preLast = cookie[128-blockSize*2:128-blockSize]
# lastBlock = cookie[128-blockSize:]
# prefix = "0"*(blockSize-1)
# for i in range(0, 16):
# 	attackPayload = cookie[:128-blockSize*2] + prefix + stringText[i] + lastBlock
# 	r = requests.get(url, cookies={'flag_auth': attackPayload})
# 	print r.status_code


# iv = cookie[:blockSize]
# firstBlock = cookie[blockSize:blockSize*2]
# prefix = "0"*(blockSize-2)
# for i in range(0, 255):

# 	tmp = hex(1)[2:]
# 	if(len(tmp)==1):
# 		tmp += "0"+tmp
# 	attackPayload = prefix + tmp + firstBlock
# 	r = requests.get(url, cookies={'flag_auth': tmp})
# 	print r.status_code
# 	# print r.headers["content-length"]




# iv = cookie[:blockSize]
# firstBlock = cookie[blockSize:blockSize*2]
# iv=binascii.unhexlify(iv)
# bf_range=list(" "+string.ascii_letters)
# iv = list(iv)
# iv_index = len(iv)-1
# j=0x1
# temp=iv[iv_index]
# for i in range(0,255):
# 	iv[iv_index]=chr(ord(iv[iv_index]) ^ i)

# 	final_target="".join(iv).encode("hex")+firstBlock
# 	r = requests.get(url, cookies={'flag_auth': final_target})
# 	print chr(ord(iv[iv_index])^j) + " " + str(r.status_code)
	
iv = cookie[:blockSize]
firstBlock = cookie[blockSize:blockSize*2]
iv=binascii.unhexlify(iv)
iv = list(iv)
bf_range=list(" "+string.ascii_letters)
iv_index = len(iv)-1
plain_text=[]
# tmp = iv[iv_index] 
# for i in range(0,255):
# 	iv[iv_index]=chr(ord(iv[iv_index]) ^ i)
# 	final_target="".join(iv).encode("hex")+firstBlock
# 	r = requests.get(url, cookies={'flag_auth': final_target})
# 	if(r.status_code == 404):
# 		print i
# 	iv[iv_index] = tmp
# #xxxxxxxxxxxxxxxf
# print(iv)
# j+=1
# iv[iv_index] = chr(59)
# iv_index=14
# print(iv)

# for i in bf_range:

# 	iv[iv_index]=chr(ord(iv[iv_index]) ^ ord(i) ^ j)
# 	final_target="".join(iv).encode("hex")+firstBlock
# 	r = requests.get(url, cookies={'flag_auth': final_target})
# 	if(r.status_code == 404):
# 		print "Got the %d byte and it is 0x%02x" %(iv_index+1,ord(i))
# 		plain_text.append("%c" % i)
# 		print "Found "+i
# 	iv[iv_index] = tmp

# print(iv)
# 102

# iv[15] = chr(103)

# iv_index=14
# tmp = iv[iv_index] 
# for i in range(0,255):
# 	print i
# 	iv[iv_index]=chr(ord(iv[iv_index]) ^ i)
# 	final_target="".join(iv).encode("hex")+firstBlock
# 	r = requests.get(url, cookies={'flag_auth': final_target})
	

# 	if(r.status_code == 404):
# 		print "Found"
# 	iv[iv_index] = tmp


def find_for_n(s, n):
	# print "xor {0} ^ {1} ^ {2}".format(ord(s), n+1, n)
	return ord(s) ^ (n+1) ^ (n)



# n = 1
# for i in range (0,n):
# 	iss = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,117,58]
# 	m = n+1
# 	for k in (15,15-m,-1):
# 		iv[k] = chr(find_for_n(iss[k],n))
iv1 = cookie[:blockSize]
iv1=binascii.unhexlify(iv1)

for i1 in range(0,16):
	iv[i1] = chr(0)

# iv[15] = chr(58)
# iv[14] = chr(117)
# iv[13] = chr(156)
# iv[12] = chr(196)
# iv[11] = chr(89)
# iv[10] = chr(89)
# iv[9] = chr(245)
# iv[8] = chr(32)
# iv[7] = chr(91)
# iv[6] = chr(11)
# iv[5] = chr(33)
# iv[4] = chr(190)
# iv[3] = chr(84)
# iv[2] = chr(222)
# iv[1] = chr(252)
# iv[0] = chr(105)

# for i in range(0,16):
# 	tmp = ord(iv[i]) ^ ord(iv1[i]) ^ (16-i)
# 	print chr(tmp)
# for m in range(0,15):

# n = 2
# for m in range(0,n):
# 	for k in range(15,15-n,-1):
# 		if(k >= (15-m)):
# 			iv[k] = chr(find_for_n(iv[k],m+1))
# print iv

# for j in range(0,255):
# 	iv[15-n] = chr(j)


# 	final_target = "".join(iv).encode("hex")+firstBlock
# 	r = requests.get(url, cookies={'flag_auth': final_target})
# 	if(r.status_code == 404):
# 		print "Found ",
# 		print j
# 		# iv[15-n] = chr(j)
# 		break
# print iv

###################################
'''
iv1 = cookie[:blockSize]
firstBlock = cookie[blockSize*2:blockSize*3]
for i1 in range(0,16):
	iv[i1] = chr(0)
iv[15] = chr(176) #1
iv[14] = chr(137) #2
iv[13] = chr(192)
iv[12] = chr(6)
iv[11] = chr(6)
iv[10] = chr(248)
iv[9] = chr(186)
iv[8] = chr(86)
# iv[7] = chr(182)
# iv[6] = chr(11)
# iv[5] = chr(33)
# iv[4] = chr(190)
# iv[3] = chr(84)
# iv[2] = chr(222)
# iv[1] = chr(252)
# iv[0] = chr(105)
# for i in range(0,16):
# 	tmp = ord(iv[i]) ^ ord(iv1[i]) ^ (16-i)
# 	print chr(tmp)
# for m in range(0,15):

n = 8
for m in range(0,n):
	for k in range(15,15-n,-1):
		if(k >= (15-m)):
			iv[k] = chr(find_for_n(iv[k],m+1))
print iv

for j in range(0,255):
	iv[15-n] = chr(j)


	final_target = iv1 + "".join(iv).encode("hex")+firstBlock
	r = requests.get(url, cookies={'flag_auth': final_target})
	if(r.status_code == 404):
		print "Found ",
		print j
		# iv[15-n] = chr(j)
		break
print iv



'''

iv1 = cookie[:blockSize]
iv1 = ""
firstBlock = cookie[blockSize*1:blockSize*2]
for i1 in range(0,16):
	iv[i1] = chr(0)
result_iv = cookie[:blockSize]
result_iv=binascii.unhexlify(result_iv)
result_iv = list(iv)
for i1 in range(0,16):
	result_iv[i1] = chr(0)
# iv[15] = chr(176) #1
# iv[14] = chr(137) #2
# iv[13] = chr(192)
# iv[12] = chr(6)
# iv[11] = chr(6)
# iv[10] = chr(248)
# iv[9] = chr(186)
# iv[8] = chr(86)
# iv[7] = chr(182)
# iv[6] = chr(11)
# iv[5] = chr(33)
# iv[4] = chr(190)
# iv[3] = chr(84)
# iv[2] = chr(222)
# iv[1] = chr(252)
# iv[0] = chr(105)
# for i in range(0,16):
# 	tmp = ord(iv[i]) ^ ord(iv1[i]) ^ (16-i)
# 	print chr(tmp)
# for m in range(0,15):
found = None
iv1 = cookie[:blockSize*2]
iv1 = ""
primaryBlock = cookie[blockSize*0:blockSize*1]
primaryBlock=binascii.unhexlify(primaryBlock)
result = ""
firstBlock = cookie[blockSize*1:blockSize*2]
for i1 in range(0,16):
	iv[i1] = chr(0)

for n in range(0,16):
	for k in range(15,15-n,-1):
		iv[k] = chr(find_for_n(iv[k],n))
	print iv

	for j in range(0,255):
		iv[15-n] = chr(j)
		final_target = iv1 + "".join(iv).encode("hex")+firstBlock
		r = requests.get(url, cookies={'flag_auth': final_target})
		if(r.status_code == 404):
			print "Found ",
			print j
			found = j
			break
	print "Set {0} to {1}".format(15-n, j)
	iv[15-n] = chr(found)
	result_iv[15-n] = chr(found)
	tmp2 = found ^ ord(primaryBlock[15-n]) ^ (n+1)
	print "Found char: {0}".format(chr(tmp2))
	result = chr(tmp2) + result
	print "Result: {0}".format(result)
	# print iv

# print "result: "
# print result_iv
# result = ""
# for i in range(0,16):
# 	tmp = ord(result_iv[i]) ^ ord(primaryBlock[i]) ^ (15-i)
# 	result += chr(tmp)
# print (result)
