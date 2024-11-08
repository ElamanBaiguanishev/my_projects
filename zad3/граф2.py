for i in range(int(values['num1'])):
                    window.extend_layout(window['day1'],
                        [[sg.Text('Start time:'), sg.Input(size=(3,1), key=f'start{1}{i}'),
                        sg.Text('End time:') , sg.Input(size=(3,1), key=f'end{1}{i}')]])