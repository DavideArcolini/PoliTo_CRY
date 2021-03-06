import socket
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


ecb_oracle_secret = "Here's my secret"
ecb_oracle_key = b'\x1e\x86\x114\x0b\x8d6k`\xb1\xdc\xb5\xa9\xc7,\xe8A\xe2\x1c\x0bk\x93Lc\xc0\xa9\xce\xae\xcc.z\xd2'
HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 12345


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
print('Socket bind complete')

s.listen(10)
print('Socket now listening')

#wait to accept a connection - blocking call
while 1:
    conn, addr = s.accept()
    print('A new encryption requested by ' + addr[0] + ':' + str(addr[1]))

    input0 = conn.recv(1024).decode()

    # ecb_oracle_secret is 16 bytes long, all printable strings
    message = """Here is the msg:{0} - and the sec:{1}""".format( input0, ecb_oracle_secret)
    message = pad(message.encode(),AES.block_size)
    cipher = AES.new( ecb_oracle_key, AES.MODE_ECB )
    ciphertext = cipher.encrypt(message)

    conn.send(ciphertext)
    conn.close()

s.close()