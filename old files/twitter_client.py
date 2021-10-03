import socket
import argparse
from cryptography.fernet import Fernet
import hashlib
import pickle
from play_ibm_sound import play_ibm_sound
from keys import *
import pandas as pd
import tweepy
import string

class SL(tweepy.Stream):

    def on_status(self, status):
        question = status.text
        question = question.replace("#ECE4564T13", '')
        print("[Client03] –New question found: ", question)

        print("[Client05] –Generated Encryption Key: ", key.decode('utf-8'))
        f = Fernet(key)
        encrypted = f.encrypt(question.encode('utf-8'))
        print("[Client06] –Cipher Text: ", encrypted.decode('utf-8'))
        checksum = hashlib.md5(question.encode()).hexdigest()
        payload = (key, encrypted, checksum)
        print('[Client07] –Question payload: ', payload)
        pickled = pickle.dumps(payload)
        print('[Client 08] –Sending question: ', pickled)
        sock.send(pickled)


parser = argparse.ArgumentParser()
parser.add_argument("-sip", "--server_ip", help="server IP address")
parser.add_argument("-sp", "--server_port", help="Server port", type=int)
parser.add_argument("-z", "--socket_size", help="socket size", type=int)

args = parser.parse_args()

print('[Client01] –Connecting to ', args.server_ip, ' on port ', args.server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((args.server_ip, args.server_port))
print("[Client02] –Listening for tweets from Twitter API that contain questions")
myStream = SL(API_key, API_key_secret, access_token, access_token_secret)
myStream.filter(track = ["#ECE4564T13"], threaded=True)

key = Fernet.generate_key()  # generate key
f = Fernet(key)

while True:
    pickled = sock.recv(args.socket_size)
    if (pickled is not None):
        unpickled = pickle.loads(pickled)
        print('[Client09] –Received data: ', unpickled)
        print('[Client10] –Decrypt Key: ', key)
        decrypted = f.decrypt(unpickled[0])
        print('[Client11] –Plain Text: ', decrypted.decode('utf-8'))
        print('[Client 12] –Speaking answer: ', decrypted.decode('utf-8'))
        play_ibm_sound(decrypted.decode('utf-8'))

sock.close()
