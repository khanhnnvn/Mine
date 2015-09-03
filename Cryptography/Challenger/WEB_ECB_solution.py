__author__ = 'namhb1'
import requests, re

find_url = "http://localhost:5000/find/"
def unblock(text):
    length = len(text)
    cipher_block_size = 32
    block_num, y = divmod(length, cipher_block_size)
    result = []
    for i in range(1, block_num+1):
        start = (i-1)*cipher_block_size
        end   = (i)*cipher_block_size
        result.append(text[start:end])
    return result
def get_ticket(username):
    post_data = {"username":username}
    r = requests.post(find_url, data=post_data)
    m = re.search('ticket\/(.*)"', r.text)
    m = m.group(1)
    return m
#Get ticket
for i in range(1, 50):
    uname = "9"*i
    #print "Input: %d    | Output %d" %(len(uname), len(get_ticket(uname)))
    '''
    i = 4 ==> Block add =>
    {"username": "99
    9999999999999999
    9999", "money":
    0}
    username = 9999999999999999999999 (22)
        '''
#print get_ticket("9"*22)
#f3c507a4ec4fb1e1e86daa9f6eb7830592ceb14a9a9a4e4233ee78cb4b7b6f602d6cc4dd38c79d298d9aad8b7e08c251d9a65ba662d921bf3745b66e47322e45
cipher = "f3c507a4ec4fb1e1e86daa9f6eb7830592ceb14a9a9a4e4233ee78cb4b7b6f602d6cc4dd38c79d298d9aad8b7e08c251d9a65ba662d921bf3745b66e47322e45"
s = unblock(cipher)
a = s[0] + s[2] + s[1] + s[3]
print a
