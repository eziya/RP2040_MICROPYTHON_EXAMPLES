import board
import digitalio
import audioio
import audiomp3
import audiobusio

button1 = digitalio.DigitalInOut(board.GP20)
button1.direction = digitalio.Direction.INPUT

audio = audioio.AudioOut(board.GP18, right_channel=board.GP19)
mp3 = audiomp3.MP3Decoder(open("9jx82-hl9h1.mp3", "rb"))

while True:
    if button1.value == False:        
        print("Playing")        
        audio.play(mp3)

        while button1.value == False:
            continue

        while audio.playing:
            if button1.value == False:
                print("Stop")
                audio.stop()

                while button1.value == False:
                    continue
                break