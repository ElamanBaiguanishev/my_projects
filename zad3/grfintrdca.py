import PySimpleGUI as sg
import wave

from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import json
import os

# AudioSegment.converter = "ffmpeg.exe"
# AudioSegment.ffmpeg = "ffmpeg.exe"
# AudioSegment.ffprobe = "ffprobe.exe"

SetLogLevel(0)


def main():
    try:
        output_win = [
            [sg.Output(size=(78, 20))]
        ]
        layout = [[sg.Text('path Model')],
                  [sg.Input(), sg.FolderBrowse()],
                  [sg.Text("path Audio")],
                  [sg.Input(), sg.FileBrowse()],
                  [sg.Frame('Output', layout=output_win)],
                  [sg.Submit('Start'), sg.Cancel()]]
        window = sg.Window("Main Window", layout)
        while True:
            event, values = window.read()
            sound = AudioSegment.from_file(values[1]).set_channels(1)
            name = os.path.basename(values[1]).split('.')[0]
            sound.export("primer.wav", format="wav")
            wf = wave.open('primer.wav', 'rb')
            file_duration = wf.getnframes() / wf.getframerate()
            frame = wf.getframerate()
            result = ''
            last_n = False
            if event == 'Cancel' or event is None:
                break
            elif event == 'Start':
                count = 0
                sg.one_line_progress_meter('Progress', count, int(file_duration), orientation='h')
                rec = KaldiRecognizer(Model(values[0]), frame)
                while True:
                    count = count + 1
                    data = wf.readframes(frame)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        if res['text'] != '':
                            result += f" {res['text']}"
                            last_n = False
                        elif not last_n:
                            result += '\n'
                            last_n = True
                    sg.one_line_progress_meter('Progress', count, int(file_duration), orientation='h')
                res = json.loads(rec.FinalResult())
                result += f' {res["text"]}'
                print(result)
                with open(f'C:\\Users\\Elaman\\PycharmProjects\\zad3\\datab\\{name}.txt', 'w') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)

        window.close()
    except:
        print()


if __name__ == "__main__":
    main()
