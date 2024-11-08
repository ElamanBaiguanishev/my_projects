import wave

from moviepy.editor import *
from pydub import AudioSegment

AudioSegment.converter = "D:\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "D:\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "D:\\bin\\ffprobe.exe"

sound = AudioSegment.from_file("m4a.m4a")
sound = sound.set_channels(1)
sound.export("primer.wav", format="wav")

wf = wave.open("primer.wav").getnchannels()

print(wf)
