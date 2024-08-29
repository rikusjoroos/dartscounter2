import PySimpleGUI as sg

scale = "Normal"


class Game:
    def __init__(self):
        """Initializes the Game class."""
        self.number_of_players = 0
        self.player_list = []
        self.turn_idx = 0
        self.started_idx = 0
        self.starting_points = 0

    def create_players(self, number_of_players, points, window):
        """
        Creates players and updates the window.

        Args:
            number_of_players (int): Number of players.
            points (int): Starting points for each player.
            window (sg.Window): The PySimpleGUI window object.
        """
        self.number_of_players = number_of_players
        self.starting_points = points
        self.player_list = []
        self.turn_idx = 0
        for player in range(number_of_players):
            player = Player(points)
            self.player_list.append(player)
        window['-TURN-'].update("Player 1 points")
        window['-POINTSLEFT1-'].update(background_color = 'white', text_color = 'black')

    def change_turn(self, window):
        """
        Changes the turn to the next player.

        Args:
            window (sg.Window): The PySimpleGUI window object.
        """
        self.turn_idx += 1
        if self.turn_idx > self.number_of_players -1:
            self.turn_idx = 0
        for i in range(self.number_of_players):
            window[f'-POINTSLEFT{i+1}-'].update(background_color = sg.theme_background_color(), text_color = sg.theme_text_color())
            
        window['-TURN-'].update(f"Player {self.turn_idx+1} points")
        window[f'-POINTSLEFT{self.turn_idx+1}-'].update(background_color = 'white', text_color = 'black')

    def scored(self, window):
        """
        Processes the score input from the player and updates statistics.

        Args:
            window (sg.Window): The PySimpleGUI window object.

        Returns:
            bool: Whether the score input was successful.
        """
        try:
            points_scored = int(window[f'-POINTS-'].get())
        except ValueError:
            return False
        if points_scored > 180:
            return False
        player = self.player_list[self.turn_idx]
        player.points -= points_scored
        player.leg_scores.append(points_scored)
        player.match_scores.append(points_scored)
        window[f'-POINTSLEFT{self.turn_idx+1}-'].update(str(player.points))
        window['-POINTS-'].update("")
        self.update_stats(window)
        return True

    def check_winner(self, window):
        player = self.player_list[self.turn_idx]
        if player.points == 0:
            playername = window[f'-PLAYER{self.turn_idx+1}NAME-'].get()
            answer = sg.popup_yes_no(playername + " won?", title = "Winner?")
            if answer == "Yes":
                self.started_idx += 1
                if self.started_idx > self.number_of_players - 1:
                    self.started_idx = 0
                player.legwins += 1
                window[f'-PLAYER{self.turn_idx + 1}LEGWIN-'].update(str(player.legwins))
                if player.hco < player.leg_scores[-1]:
                    player.hco = player.leg_scores[-1]
                self.turn_idx = self.started_idx -1
                for i in range(self.number_of_players):
                    window[f'-POINTSLEFT{i+1}-'].update(str(self.starting_points))
                    self.player_list[i].points = self.starting_points
                    self.player_list[i].leg_scores = []

                self.update_stats(window)

            if answer == "No":
                player.leg_scores.pop()
                player.match_scores.pop()
                player.leg_scores.append(0)
                player.match_scores.append(0)
    
    def update_stats(self, window):
        for i in range(self.number_of_players):
            player = self.player_list[i]
            if len(player.leg_scores) > 0:
                player.firstnine = sum(player.leg_scores[:3]) / len(player.leg_scores[:3])
                player.avg = sum(player.leg_scores) / len(player.leg_scores)
                player.lscore = player.leg_scores[-1]
            if len(player.match_scores) > 0:
                player.match_avg = sum(player.match_scores) / len(player.match_scores)

            window[f'-P{i + 1}AVG-'].update(str(round(player.avg, 2)))
            window[f'-P{i + 1}MATCHAVG-'].update(str(round(player.match_avg, 2)))
            window[f'-P{i + 1}FIRSTNINEAVG-'].update(str(round(player.firstnine, 2)))
            window[f'-P{i + 1}CO-'].update(str(player.hco))
            window[f'-P{i + 1}LSCORE-'].update(str(player.lscore))
    
    def go_back(self, window):
        print(self.turn_idx)
        if len(self.player_list[self.turn_idx-1].leg_scores) == 0:
            return

        if self.turn_idx == 0:
            self.turn_idx = self.number_of_players - 1
        else:
            self.turn_idx -= 1

        player = self.player_list[self.turn_idx]
        if len(player.leg_scores) > 0:
            player.lscore = player.leg_scores.pop()
            player.points += player.lscore

        if len(player.match_scores) > 0:
            player.match_scores.pop()
        for i in range(self.number_of_players):
            window[f'-POINTSLEFT{i+1}-'].update(background_color = sg.theme_background_color(), text_color = sg.theme_text_color())

        window[f'-P{self.turn_idx + 1}LSCORE-'].update(str(player.lscore))
        window[f'-POINTSLEFT{self.turn_idx + 1}-'].update(str(player.points), background_color = 'white', text_color = 'black')
        window['-TURN-'].update(f"Player {self.turn_idx+1} points")
        window[f'-POINTS-'].update(str(player.lscore))
        
class Player:
    def __init__(self, points: int):
        self.points = points
        self.match_scores = []
        self.leg_scores = []
        self.turn = False
        self.avg = 0
        self.match_avg = 0
        self.firstnine = 0
        self.legwins = 0
        self.hco = 0
        self.lscore = 0


def create_layout_for_players(window, num_players, startingpoints):
    # Luodaan layout pelaajien määrän perusteella
    if scale == 'Normal':
        print(scale)
        pointFont = ("Arial", 60)
        playerFont = ("Arial", 30)
        inputFont = ("Arial", 40)
    elif scale == 'Tight':
        print(scale)
        pointFont = ("Arial", 20)
        playerFont = ("Arial", 10)
        inputFont = ("Arial", 20)
    layout = []
    menu_def = [['File', ['New Game']]]
    layout.append([sg.Menu(menu_def, tearoff = False)])
    players = []
    result = []
    xpad = 10
    ypad = 50
    if num_players > 0 and num_players < 3:
        xpad = 100
    elif num_players > 3:
        xpad = 1

    for i in range(num_players):
        player_layout = [[sg.Text(f"Player {i+1}")],
        [sg.InputText(size=(8,1), font=playerFont, key = f'-PLAYER{i+1}NAME-'), sg.Text("0", font=playerFont, key = f'-PLAYER{i+1}LEGWIN-')],
        [sg.Text(startingpoints, key = f'-POINTSLEFT{i+1}-', font = pointFont, enable_events=True)],
        [sg.Text("AVG:"),sg.Text("0", key = f'-P{i+1}AVG-')],
        [sg.Text("Match AVG:"), sg.Text("0", key = f'-P{i+1}MATCHAVG-')],
        [sg.Text("F9 AVG:"), sg.Text("0", key = f'-P{i+1}FIRSTNINEAVG-')],
        [sg.Text("Highest CO:"), sg.Text("0", key = f'-P{i+1}CO-')],
        [sg.Text("Latest Score:"), sg.Text("0", key = f'-P{i+1}LSCORE-')]
        ]
            
        
        players.append(sg.Column(player_layout,justification='c', pad=(xpad,ypad)))
    
    result_column = [[sg.Text("Player 1 points", key = '-TURN-')],
    [sg.InputText(size=(5,1), font = inputFont, key = '-POINTS-'),sg.Button('Subtract', visible= True, bind_return_key=True), sg.Button("Remains", visible = False)],
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
        if event == 'exit' or event == sg.WIN_CLOSED:
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
    global scale
    game = Game()
    menu_def = [['File', ['New Game']],['Scale', ['Tight', 'Normal']]]
    window = sg.Window('Darts Counter', layout=[[sg.Menu(menu_def, tearoff=False,key='-MENU BAR-')]], resizable=True, finalize=True, size=(200,200))
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
            game.check_winner(window)
            game.change_turn(window)
        elif event == "Back":
            game.go_back(window)
        elif event == 'Tight':
            scale = 'Tight'
            print(scale)
        elif event == 'Normal':
            scale = 'Normal'
            print(scale)


    window.close()

main()