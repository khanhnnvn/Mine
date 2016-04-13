#Padding Oracle decryption 
import binascii
import urllib2
import string, requests
 
target="http://crypto-class.appspot.com/po?er="
 
plain_text=[]
 
def padding_oracle(iv,ct):
    global target,plain_text
    #print "iv=",iv
    iv=binascii.unhexlify(iv)
    iv=list(iv) #because string is immutable,convert to a string first
    iv_index=len(iv)-1
 
    j=0x1
    bf_range=list(" "+string.ascii_letters)
    for k in range(16):
        #print "orig =0x%02x " %ord(iv[iv_index])
        temp=iv[iv_index]
        for i in bf_range:
 
            iv[iv_index]=chr(ord(iv[iv_index]) ^ ord(i) ^ j)
            final_target="".join(iv).encode("hex")+ct
         #   if i == 's' and k==1:
         #       print final_target
         #       print iv[iv_index],iv_index,i,j
            r = requests.get(target, cookies={'flag_auth': final_target})
            ecode = r.status_code
            # request=urllib2.Request(final_target) #create a HTTP Request
            # try:
            #     resp=urllib2.urlopen(request) #capture the Response
            # except urllib2.HTTPError,e:
            if ecode == 404: #valid pad
                #print final_target
                print "Got the %d byte and it is 0x%02x" %(iv_index+1,ord(i))
                plain_text.append("%c" % i)
                #print plain_text

                break

            elif ecode == 403: #invalid pad, iterate
                print "403:Forbidden"

            else:
                print "unknown code :%d" % ecode
            iv[iv_index]=temp #restore the value back
        #print final_target
        #print "modified=0x%02x" % ord(iv[iv_index])
        iv_index-=1
        j+=1
        list_index=0
        end_index=len(iv)-1
 
        while end_index > iv_index and list_index < len(plain_text): #this is to take care of further padding
            if k==15: #skip the last iteration
                break
            iv[end_index]=chr(ord(iv[end_index]) ^  j ^ (j-1))
            #print "pad modified=0x%02x" % ord(iv[end_index])
            end_index-=1
            list_index+=1
 
    print "Padding Oracle Attack successful"
    print "Decrypted text : ","".join(plain_text)[::-1] #print the decrypted text
 
if __name__ == "__main__":
 
 
    cipher_text="02d1b12cc642236808d06f7eecbf555d2bc3220f06ee20da7c87de2164afead6319e642bd28e1ab08cf7b28259ec5f6826cdb13f69d5fb98dca613b952efb4ac"
    print "len of cipher text = %d" % len(cipher_text)
 
    iv=cipher_text[:32]
    ct=cipher_text[32:64]
    padding_oracle(iv,ct)
