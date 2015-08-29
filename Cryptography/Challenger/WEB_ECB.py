from flask import Flask, request, render_template
from Crypto.Cipher import AES
import binascii, struct, json
app = Flask(__name__)

key = "12345678"
iv  = "87654321"
######################################################################################
def encrypt(key, text, iv):
    if(len(key) > 32):
        print "Error!"
        exit(1)
    else:
        if(len(key) < 16):
            key  = padding(string2byte(key),16)
        else:
            if(len(key) < 24):
                key  = padding(string2byte(key),24)
            else:
                key  = padding(string2byte(key),32)
    text = padding(string2byte(text))

    iv  = padding(string2byte(iv))
    encrypt_suite = AES.new(key, AES.MODE_ECB, iv)
    cipher = encrypt_suite.encrypt(text)
    return cipher
def decrypt(key, cipher, iv):
    iv  = padding(string2byte(iv))
    if(len(key) > 32):
        print "Error!"
        exit(1)
    else:
        if(len(key) < 16):
            key  = padding(string2byte(key),16)
        else:
            if(len(key) < 24):
                key  = padding(string2byte(key),24)
            else:
                key  = padding(string2byte(key),32)
    decrypt_suite = AES.new(key, AES.MODE_ECB, iv)
    data = decrypt_suite.decrypt(cipher)
    byte = byte2string(depadding(string2byte(data)))
    return byte
def padding(data, block_size=16):
    x, y = divmod(len(data),block_size)
    if y!=0:
        length = block_size - (len(data) % block_size)
        for i in range(1,length+1):
            data.append(length)
    return struct.pack('b'*len(data), *data)
def depadding(bytes):
    length = bytes[-1]
    if length > 0 and length < 16:
        for i in range(1, length+1):
            bytes.pop()
    return bytes
def string2byte(text):
    return list(ord(c) for c in text)
def byte2string(byte):
    return "".join(chr(i) for i in byte)
######################################################################################




@app.route("/")
def hello():
	return "Hello World!"
@app.route("/find/", methods=['GET', 'POST'])
def find():
    if request.method == "GET":
        return find_form()
    elif request.method == "POST":
        return do_find()
def find_form():
    return render_template("find_form.html")
def do_find():
    username = request.form['username']
    data = {
        'username'  : username,
        'money'     : 0
    }
    ticket_raw = json.dumps(data)
    print ticket_raw
    ticket = binascii.hexlify(encrypt(key,ticket_raw,iv))
    return render_template("ticket_result.html", username=username, ticket=ticket)

@app.route("/ticket/<ticket>")
def check_ticket(ticket):
    data = binascii.unhexlify(ticket)
    data_raw = decrypt(key, data, iv)
    print data_raw
    data_raw2 = depadding(data_raw)
    user_info = json.loads(data_raw2)
    if (user_info['money'] < 1000000):
        message = "You not enough money, you need 1000000 VND"
    else:
        message = "You are rich man :). This is your key: XXX_{ecb_is_not_good}"
    return render_template("check_ticket.html", username=user_info['username'], money=user_info['money'], message=message)


if __name__ == "__main__":
    app.debug = True
    app.run()