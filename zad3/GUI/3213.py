import PySimpleGUI as sg

sg.theme("LightBlue")
progress_value = 50
layout = [[sg.Text("Enter a number out of 50", font='Lucida'),
           sg.InputText(key='-PROGRESS_VALUE-', font='Lucida, 20', size=(20, 40))],
          [sg.ProgressBar(progress_value, orientation='h', size=(100, 20), border_width=4, key='-PROGRESS_BAR-',
                          bar_color=("Blue", "Yellow"))],
          [sg.Button('Change Progress'), sg.Button('Start Progress'), sg.Button('Stop Progress')]]

window = sg.Window("Progress Bar", layout)
progress_started, counter, timeout = False, 0, None
while True:
    event, values = window.read(timeout=timeout)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    if event == "Change Progress":
        progress_value = int(values['-PROGRESS_VALUE-'])
        # NOTE - must set a current count when changing the max value
        window['-PROGRESS_BAR-'].update(current_count= 0, max=progress_value)
    elif event == 'Start Progress':
        progress_started = True
        counter = 0
        timeout = 1000
    elif event == 'Stop Progress':
        progress_started = False
        timeout = None
    if progress_started:
        window['-PROGRESS_BAR-'].update(counter)
        counter += 1
        if counter > progress_value:
            progress_started = False