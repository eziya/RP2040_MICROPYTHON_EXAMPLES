import os
import time
import board
import digitalio
import busio
import sdcardio
import storage

from audiomp3 import MP3Decoder # pylint: disable=wrong-import-position

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

button1 = digitalio.DigitalInOut(board.GP20)
button1.direction = digitalio.Direction.INPUT

spi = busio.SPI(board.GP10, board.GP11, board.GP12)
sd = sdcardio.SDCard(spi, board.GP15)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

mp3files = sorted("/sd/" + filename for filename in os.listdir("/sd")
    if filename.lower().endswith("mp3"))

# You have to specify some mp3 file when creating the decoder
mp3 = open(mp3files[0], "rb")
decoder = MP3Decoder(mp3)
audio = AudioOut(board.GP18, right_channel=board.GP19)

while True:
    if button1.value == False:
        filename = mp3files[0]
        print("Playing", filename)

        # Updating the .file property of the existing decoder
        # helps avoid running out of memory (MemoryError exception)
        decoder.file = open(filename, "rb")
        audio.play(decoder)

        while button1.value == False:
            continue

        while audio.playing:
            if button1.value == False:
                print("Stop", filename)
                audio.stop()

                while button1.value == False:
                    continue

                break
