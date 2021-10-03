def play_ibm_sound(phrase):

    from ibm_watson import TextToSpeechV1
    import os
    from playsound import playsound
    import vlc
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from IBM_API_key import url, key

    authenticator = IAMAuthenticator(key)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(url)


    with open('hello_world.wav', 'wb+') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                phrase,
                voice='en-US_AllisonV3Voice',
                accept='audio/wav'
            ).get_result().content)
        
        #play audio on the raspi with vlc
        p = vlc.MediaPlayer("hello_world.wav")
        p.play()

'''
        #playsound for use on Linux

        playsound('hello_world.wav')
'''
'''
    # #following is janky way to play on windows
    os.system("start hello_world.wav")
    import time
    time.sleep(3)
    os.system("taskkill /IM wmplayer.exe ")
'''
