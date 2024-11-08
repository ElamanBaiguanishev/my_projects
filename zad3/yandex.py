import wave
import librosa

print(librosa.get_duration(filename='primer.wav'))

wf = wave.open('primer.wav', 'rb')
file_duration = wf.getnframes() / wf.getframerate()

print(file_duration)