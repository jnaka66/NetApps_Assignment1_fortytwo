import socket
import argparse
import pickle
from cryptography.fernet import Fernet
import hashlib
import wolframalpha
from ServerKeys import appID

def play_ibm_sound(phrase):
    from ibm_watson import TextToSpeechV1
    import os
    from playsound import playsound
    import vlc
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ServerKeys import ibm_url, ibm_key

    authenticator = IAMAuthenticator(ibm_key)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )
    text_to_speech.set_service_url(ibm_url)

    with open('hello_world.wav', 'wb+') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                phrase,
                voice='en-US_AllisonV3Voice',
                accept='audio/wav'
            ).get_result().content)

        # play audio on the raspi with vlc
        p = vlc.MediaPlayer("hello_world.wav")
        p.play()

args = argparse.ArgumentParser()
args.add_argument("-sp", "--server_port", help="Server port", type=int)
args.add_argument("-z", "--socket_size", help="socket size", type=int)

args = args.parse_args()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('',int(args.server_port)))
msg = "[Server01] –Created socket at " + str(socket.gethostbyname(socket.gethostname())) + " on port " + str(args.server_port)
print(msg)
serversocket.listen(5)
print("[Server02] –Listening for client connections")

while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()

    with clientsocket:
        print('[Server03] –Accepted client connection from ', address[0], ' On port ', args.server_port)
        l=1
        while(l):
            pickled = clientsocket.recv(args.socket_size)
            if(pickled is not None):
                unpickled = pickle.loads(pickled)
                print('[Server04] –Received data: ', unpickled)
                key = unpickled[0]
                print('[Server05] –Decrypt Key: ', key.decode('utf-8'))
                f = Fernet(key)
                decrypted = f.decrypt(unpickled[1])
                print('[Server06] –Plain Text: ', decrypted.decode('utf-8'))
                print('[Server07] –Speaking Question: ', decrypted.decode('utf-8'))
                play_ibm_sound(decrypted.decode('utf-8'))
                print('[Server08] –Sending question to Wolframalpha')
                #send to wolfram
                app_id = appID # App id
                client = wolframalpha.Client(app_id) # Instance of wolf ram alpha client class
                res = client.query(decrypted.decode('utf-8')) # Stores the response from wolf ram alpha
                try:
                    answer = next(res.results).text # Includes only text from the response
                except StopIteration:
                    answer = 'No answer'
                print('[Server09] –Received answer from Wolframalpha: '+answer)
                #use same key as before
                print('[Server10] –Encryption Key: ', key.decode('utf-8'))
                f = Fernet(key)
                encrypted = f.encrypt(answer.encode('utf-8'))
                print('[Server11] –Cipher Text: ', encrypted.decode('utf-8'))
                checksum = hashlib.md5(answer.encode()).hexdigest()
                print('[Server12] –Generated MD5 Checksum: ', checksum)
                answer_payload = (encrypted, checksum)
                print('[Server13] –Answer payload: ', answer_payload)
                pickled = pickle.dumps(answer_payload)
                print('[Server14] –Sending answer: ', pickled)
                clientsocket.sendto(pickled, address)
serversocket.close()