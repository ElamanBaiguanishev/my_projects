import wave
import librosa

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import json
import os

AudioSegment.converter = "D:\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "D:\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "D:\\bin\\ffprobe.exe"

SetLogLevel(0)

# Проверяем наличие модели
if not os.path.exists("Model1"):
    print(
        "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit(1)

sound = AudioSegment.from_file("test.wav")
sound = sound.set_channels(1)
sound.export("primer.wav", format="wav")


def main() -> str:
    wf = wave.open('primer.wav', 'rb')
    print(librosa.get_duration(filename='primer.wav'))
    if wf.getnchannels() != 1:
        print(f"Неверный канал {wf.getnchannels()}")
        exit(1)
    elif wf.getsampwidth() != 2:
        print("самп ширина")
        exit(1)
    elif wf.getcomptype() != "NONE":
        print("че то с типом")
        exit(1)
    frame = wf.getframerate()
    model = Model("Model2")
    rec = KaldiRecognizer(model, frame)

    result = ''
    last_n = False
    print(frame)
    count = 0
    while True:
        data = wf.readframes(frame)
        count = count + 1
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print(res)
            # print(rec)

            if res['text'] != '':
                result += f" {res['text']}"
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True

    res = json.loads(rec.FinalResult())
    result += f' {res["text"]}'
    print(count)
    return result


if __name__ == '__main__':
    print(main())
