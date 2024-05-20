# DFPlayer

Python3 library for the DFPlayer Mini MP3 Module, works with USB to TTL.

![Main interface](/assets/wiring_diagram.webp?raw=true)

## Installation

```bash
pip install DFPlayer
```

## Usage

```python
from DFPlayer import DFPlayer

serial_device = '/dev/ttyUSB0' # on Windows OS use COMX, example 'COM5'
df = DFPlayer(serial_device)

df.num_files() # get number of files on the SD card
df.play(1) # play a song by a specific number of files, without argument play the first song
df.random() # play random song
df.next() # play next song
df.previous() # play previous song
df.pause() # pause played song
df.stop() # stop played song
df.loop() # loop current played song
df.loop_all() # loop all songs on the SD card
df.set_volume(60) # set volume to 60%, default is 50
df.get_volume() # get current audio volume
df.set_eq(DFPlayer.EQ_NORMAL) # set equalizer to (EQ_NORMAL, EQ_POP, EQ_ROCK, EQ_JAZZ, EQ_CLASSIC, EQ_BASS), default is EQ_NORMAL
df.get_eq() # get current equalizer
df.reset() # reset the module
```

## Test

Make sure the module has an SD card installed and has a minimum of three songs inside. Connect with USB to TTL.

```bash
pip install -r requirements.txt
python3 -m unittest
```
