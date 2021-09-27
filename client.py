import socket
import argparse
from cryptography.fernet import Fernet
import hashlib
import pickle
from play_ibm_sound import play_ibm_sound

parser = argparse.ArgumentParser()
parser.add_argument("-sip", "--server_ip", help="server IP address")
parser.add_argument("-sp", "--server_port", help="Server port", type=int)
parser.add_argument("-z", "--socket_size", help="socket size", type=int)

args = parser.parse_args()

print('[Client01] –Connecting to ', args.server_ip, ' on port ', args.server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print((args.server_ip, args.server_port))
sock.connect((args.server_ip, args.server_port))
flag = True
while True:
    print("[Client02] –Listening for tweets from Twitter API that contain questions")
    if(flag):
        tweet_text = 'What is the capital of India?'
        print("[Client03] –New question found: ", tweet_text)
        key = Fernet.generate_key()#generate key
        print("[Client05] –Generated Encryption Key: ", key)
        f = Fernet(key)

        encrypted = f.encrypt(tweet_text.encode('utf-8'))
        print("[Client06] –Cipher Text: ", encrypted)

        checksum = hashlib.md5(tweet_text.encode()).hexdigest()
        print(checksum)
        payload = (key, encrypted, checksum)
        print('[Client07] –Question payload: ', payload)
        pickled = pickle.dumps(payload)
        print('[Client 08] –Sending question: ', pickled)
        sock.send(pickled)
        flag = False
    if(not flag):
        pickled = sock.recv(args.socket_size)
        unpickled = pickle.loads(pickled)
        print('[Client09] –Received data: ', unpickled)
        print('[Client10] –Decrypt Key: ', key)
        f = Fernet(key)
        decrypted = f.decrypt(unpickled[0])
        print('[Client11] –Plain Text: ', decrypted)
        print('[Client 12] –Speaking answer: ', decrypted)
        play_ibm_sound(decrypted.decode('utf-8'))
        flag = True

sock.close()



