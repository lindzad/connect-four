from time import sleep
import struct
import socket

from graphics import Point, GraphWin, Circle, Text, Entry, Rectangle
from twisted.internet import reactor, protocol

from logic import ai_choose_col, board_won
from chunking import get_ai_move
from networking import *

#globals, I hate globals
max_x = 7
max_y = 6

#places in appropriate row of col
def place_in_col(col, circles, pieces, player):
    player_int = player[0]
    #fills in piece
    y = -1
    for i, spot in enumerate(pieces[col]):
        if spot == -1: # empty
            pieces[col][i] = player_int
            y = i
            break
    #colors circle according to player
    if y == -1: return (-1, -1)
    circle = circles[col][y]
    player_color = player[1]
    circle.setFill(player_color)
    return (col, y)

# called with Point on click
def on_click(pnt, circles, pieces, player, circles_margin, col_width):
    # determine which column got clicked
    click_x = pnt.x
    x = int((click_x-(circles_margin))//col_width)
    if x > max_y or x < 0: return (-1, -1)
    return place_in_col(x, circles, pieces, player)

#loops forever getting clicks
def game_loop(win, circles, pieces, turn_text, names, circles_margin, col_width):
    count = 0
    colors = ["red", "yellow", "green", "blue", "purple", "cyan", "brown", "black"]
    players = []
    for i, name in enumerate(names):
        players.append((colors[i], name))
    num_players = len(players)
    while True:
        cur_player_num = count%num_players
        player = (cur_player_num, players[cur_player_num][0])
        player_type = players[cur_player_num][1]
        turn_text.setText("{}\'s Turn".format(player_type, cur_player_num))
        if "AI" in players[cur_player_num][1]:
            x = ai_choose_col(pieces, cur_player_num, num_players)
            #x = get_ai_move(pieces, cur_player_num, num_players)
            sleep(0.5)
            place_in_col(x, circles, pieces, player)
        else: # human
            on_click(win.getMouse(), circles, pieces, player, circles_margin, col_width)
        winner=board_won(pieces, num_players)
        if winner!=-1:
            turn_text.setText("Winner is {}!".format(players[winner][1]))
            turn_text.setTextColor(players[winner][0])
            sleep(3)
            win.getMouse()
            return
        count+=1

#setup pieces
def pieces_setup():
    return [ [ -1 for y in range(max_y)] for x in range(max_x)] # -1 means unpopulated

def wait_for_enter_or_click(win):
    while True:
        pt = win.checkMouse()
        if pt is not None:
            return
        key = win.checkKey()
        if key is not None and "Return" in key:
            return

#sets up the graphics
def graphics_setup():
    circle_margin = 20
    circle_radius = 40
    circles_width = max_x*circle_radius*2+(max_x+1)*circle_margin
    circles_height = max_y*circle_radius*2+(max_y+1)*circle_margin
    margin_width = 0
    margin_height = 50
    total_width = circles_width + margin_width
    total_height = circles_height + margin_height
    win = GraphWin("Connect L&G", total_width, total_height)
    _circle_start_x = margin_width+circle_margin+circle_radius
    _circle_start_y = margin_height+circle_margin+circle_radius
    _circle_diff = circle_radius*2+circle_margin
    circles = [ [ Circle(Point(_circle_start_x+x*_circle_diff, _circle_start_y+y*_circle_diff), circle_radius) for y in range(max_y-1, -1, -1)] for x in range(max_x)]
    for col in circles:
        for circle in col:
            circle.draw(win)
    turn_text = Text(Point(int(total_width//2), int(margin_height//2)+10), "\'s Turn")
    turn_text.setSize(24)
    turn_text.setStyle("bold")
    turn_text.draw(win)
    col_width = circle_radius*2+circle_margin
    return (win, circles, turn_text, circle_margin, col_width)

def num_players_ui():
    # Number of Players
    num_players_win = GraphWin("Connect L&G - Number of Players", 300, 100)
    num_players_label = Text(Point(75, 25), "Number of Players:")
    num_players_label.draw(num_players_win)
    num_players_entry = Entry(Point(175, 25), 5)
    num_players_entry.draw(num_players_win)
    num_continue_button = Rectangle(Point(50, 50), Point(275, 75))
    button_center = num_continue_button.getCenter()
    button_text = Text(button_center, "Continue")
    button_text.draw(num_players_win)
    num_continue_button.draw(num_players_win)
    wait_for_enter_or_click(num_players_win)
    num_players = 2
    num_players_entry_val = num_players_entry.getText()
    if num_players_entry_val != '':
        num_players = int(num_players_entry_val)
    num_players_win.close()
    return num_players

def player_names_ui(num_players):
    # Player names
    names_win = GraphWin("Connect L&G - Names", 500, 75+25*num_players)
    name_entries = []
    for i in range(num_players-1, -1, -1):
        name_label = Text(Point(75, 25*(i+1)), "Name or AI_#:")
        name_label.draw(names_win)
        name_entry = Entry(Point(250, 25*(i+1)), 20)
        name_entry.draw(names_win)
        name_entries.append(name_entry)
    names_continue_button = Rectangle(Point(75, 25*(num_players+1)), Point(275, 25+25*(num_players+1)))
    button_center = names_continue_button.getCenter()
    button_text = Text(button_center, "Continue")
    button_text.draw(names_win)
    names_continue_button.draw(names_win)
    wait_for_enter_or_click(names_win)
    names = []
    for name_entry in name_entries:
        name = name_entry.getText()
        names.append(name)
    names_win.close()
    return names

#screens to choose game settings
def pregame():
    num_players = num_players_ui()
    names = player_names_ui(num_players)
    return names

def type_ui():
    net_win = GraphWin("Connect L&G - Multiplayer Type", 500, 200)
    local_text = Text(Point(125, 100), "Local Multiplayer")
    online_text = Text(Point(375, 100), "Online 2-player")
    local_text.draw(net_win)
    online_text.draw(net_win)
    click = net_win.getMouse()
    net_win.close()
    return click.x > 250

def waiting_ui():
    win = GraphWin("Connect L&G - Waiting for Online Connection", 300, 200)
    text = Text(Point(150, 100), "Waiting for a connection...")
    text.draw(win)
    return win


#main / initialize
def main():
    online = type_ui()

    if online:
        waiting_win = waiting_ui()
        f = ConnectClientFactory(waiting_win)
        reactor.connectTCP("localhost", 8000, f)
        reactor.run()
    else:
        names = pregame()
        win, circles, turn_text, circles_margin, col_width = graphics_setup()
        pieces = pieces_setup()
        game_loop(win, circles, pieces, turn_text, names, circles_margin, col_width)
        win.close()    # Close window when done

if __name__ == "__main__":
    main()
