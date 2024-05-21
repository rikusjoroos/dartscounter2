import PySimpleGUI as sg

pointFont = ("Arial", 60)
playerFont = ("Arial", 30)

class Game:
    def __init__(self):
        self.number_of_players = 0
        self.player_list = []
        self.turn_idx = 0
        self.started_idx = 0

    
    def create_players(self, number_of_players, points, window):
        self.number_of_players = number_of_players
        
        for player in range(number_of_players):
            player = Player(points)
            self.player_list.append(player)
        print(self.player_list)
        window['-TURN-'].update("Player 1 points")
        window['-POINTSLEFT1-'].update(background_color = 'white', text_color = 'black')

    def change_turn(self, window):
        self.turn_idx += 1
        if self.turn_idx > self.number_of_players -1:
            self.turn_idx = 0
        for i in range(self.number_of_players):
            window[f'-POINTSLEFT{i+1}-'].update(background_color = sg.theme_background_color(), text_color = sg.theme_text_color())
            
        window['-TURN-'].update(f"Player {self.turn_idx+1} points")
        window[f'-POINTSLEFT{self.turn_idx+1}-'].update(background_color = 'white', text_color = 'black')

    def scored(self, window):
        try:
            points_scored = int(window[f'-POINTS-'].get())
        except ValueError:
            return False

        self.player_list[self.turn_idx].points -= points_scored
        window[f'-POINTSLEFT{self.turn_idx+1}-'].update(str(self.player_list[self.turn_idx].points))
        window['-POINTS-'].update("")
        return True



    def check_winner(self):
        self.started_idx += 1

class Player:
    def __init__(self, points: int):
        self.points = points
        self.turn = False
        self.avg = 0
        self.match_avg = 0
        self.firstnine = 0

    def scored(self, scored_points: int):
        self.points = self.points - scored_points

def create_layout_for_players(window, num_players, startingpoints):
    # Luodaan layout pelaajien määrän perusteella
    layout = []
    menu_def = [['File', ['New Game']]]
    layout.append([sg.Menu(menu_def, tearoff = False)])
    players = []
    result = []
    xpad = 50
    ypad = 50
    if num_players > 0 and num_players < 4:
        xpad = 100
        ypad = 50
    elif num_players == 5:
        xpad = 10

    for i in range(num_players):
        player_layout = [[sg.Text(f"Player {i+1}")],
        [sg.InputText(size=(10,1), font=playerFont, key = f'-PLAYER{i+1}NAME-'), sg.Text("0", font=playerFont, key = f'-PLAYER{i+1}LEGWIN-')],
        [sg.Text(startingpoints, key = f'-POINTSLEFT{i+1}-', font = pointFont, enable_events=True)],
        [sg.Text("AVG:"),sg.Text("0", key = f'-P{i+1}AVG-')],
        [sg.Text("Match AVG:"), sg.Text("0", key = f'-P{i+1}MATCHAVG-')]
        ]
            
            # Tässä voit lisätä muita pelaajaa koskevia komponentteja
        
        players.append(sg.Column(player_layout,justification='c', pad=(xpad,ypad)))
    
    result_column = [[sg.Text("Player 1 points", key = '-TURN-')],
    [sg.InputText(size=(15,1), key = '-POINTS-'),sg.Button('Subtract', visible= True, bind_return_key=True), sg.Button("Remains", visible = True)],
    [sg.Button('Back', visible = True)]
    ]

    result.append(sg.Column(result_column, justification='c'))
    layout.append(players)
    layout.append(result)
    window.close()
    
    return layout

def new_game():
    numberofplayers = 1
    startingpoints = 501
    values = [1,2,3,4,5]
    column1 = [[sg.Text('Number of players')],
               [sg.Text("Starting points")]]
    column2 = [[sg.Combo(values,default_value = 1, expand_x = True, readonly = True, key = '-NUMBEROFPLAYERS-')],
               [sg.InputText(size = (10,1), key = '-STARTINGPOINTS-')]]
    column3 = [[sg.Button('OK')]]
    new_game_window_layout = [[sg.Column(column1), sg.Column(column2)],[sg.Column(column3)]]
    window = sg.Window("New Game", new_game_window_layout, modal = True)
    while True:
        event, values = window.read()
        if event == exit or event == sg.WIN_CLOSED:
            break
        elif event == 'OK':
            numberofplayers = int(window['-NUMBEROFPLAYERS-'].get())
            try:
                startingpoints = int(window['-STARTINGPOINTS-'].get())
            except ValueError:
                continue
            if startingpoints < 0:
                startingpoints = 501
            break


    window.close()
    return numberofplayers, startingpoints

def main():
    sg.theme('Black')

    game = Game()
    menu_def = [['File', ['New Game']]]
    window = sg.Window('Darts Counter', layout=[[sg.Menu(menu_def, tearoff=False,key='-MENU BAR-')]], resizable=True)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'New Game':
            numberofplayers, startingpoints = new_game()
            if numberofplayers is not None:
                game_layout = create_layout_for_players(window, numberofplayers, str(startingpoints))
                window = sg.Window('Darts Counter', layout = game_layout, resizable=True, finalize=True)
            game.create_players(numberofplayers, int(startingpoints), window)
            print(numberofplayers, startingpoints)
        elif event == 'Subtract':

            if game.scored(window) == False:
                continue
            game.change_turn(window)

    window.close()

main()