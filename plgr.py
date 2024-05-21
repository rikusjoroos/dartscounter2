import PySimpleGUI as sg
pointFont = ("Arial", 60)
playerFont = ("Arial", 30)
col1 = [[sg.Text("Player 1")],
        [sg.InputText(size=(10,1), font=playerFont, key = '-PLAYER1NAME-'), sg.Text("0", font=playerFont, key = '-PLAYER1LEGWIN-')],
        [sg.Text("501", key = '-POINTSLEFT1-', font = pointFont, enable_events=True, background_color="white", text_color="black")],
        [sg.Text("AVG:"),sg.Text("0", key = '-P1AVG-')],
        [sg.Text("Match AVG:"), sg.Text("0", key = '-P1MATCHAVG-')]
        ]

col2 = [[sg.Text("Player 2")],
        [ sg.InputText(size=(10,1), font = playerFont, key = '-PLAYER2NAME-'), sg.Text("0", font=playerFont, key = '-PLAYER2LEGWIN-') ],
        [sg.Text("501",key = '-POINTSLEFT2-', font = pointFont, enable_events= True)],
        [sg.Text("AVG:"), sg.Text("0", key = '-P2AVG-')],
        [sg.Text("Match AVG:"), sg.Text("0", key = '-P2MATCHAVG-')]
        ]

col3 = [[sg.Text("Player 1 points", key = '-TURN-')],
        [sg.InputText(size=(15,1), key = '-POINTS-', font = playerFont),sg.Button('Subtract', visible= True, bind_return_key=True), sg.Button("Remains", visible = True)],
        [sg.Button('Back', visible = True)]
        ]
layout = []
players = []
result = []
players.append(sg.Column(col1))
players.append(sg.Column(col2))
result.append(sg.Column(col3))

layout.append(players)
layout.append(result)
print(layout)

#leiska = [[sg.Column(col1), sg.Column(col2)], [sg.Column(col3)]]
#print(leiska)

while True:
    window = sg.Window("Darts Counter", layout, resizable=True)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()