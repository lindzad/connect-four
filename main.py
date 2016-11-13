from graphics import Point, GraphWin, Circle, Text, Entry
from time import sleep
from logic import ai_choose_col

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
    if y == -1: return
    circle = circles[col][y]
    player_color = player[1]
    circle.setFill(player_color)
    print(circle)

# called with Point on click
def on_click(pnt, circles, pieces, player):
    # determine which column got clicked
    click_x = pnt.x
    x = int((click_x-15)//130)
    if x > max_y: return
    place_in_col(x, circles, pieces, player)


#loops forever getting clicks
def game_loop(win, circles, pieces, turn_text, names):
    count = 0
    colors = ["red", "yellow", "green", "blue"]
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
            place_in_col(x, circles, pieces, player)
        else: # human
            on_click(win.getMouse(), circles, pieces, player)
        count+=1

#setup pieces
def pieces_setup():
    return [ [ -1 for y in range(max_y)] for x in range(max_x)] # -1 means unpopulated

#sets up the graphics
def graphics_setup():
    circle_margin = 30
    circle_radius = 50
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
    turn_text = Text(Point(int(total_width//2), 40), "\'s Turn")
    turn_text.setSize(24)
    turn_text.setStyle("bold")
    turn_text.draw(win)
    return (win, circles, turn_text)

#screen to choose game settings
def pregame():
    # Number of Players
    num_players_win = GraphWin("Connect L&G - Number of Players", 300, 100)
    num_players_label = Text(Point(75, 25), "Number of Players:")
    num_players_label.draw(num_players_win)
    num_players_entry = Entry(Point(175, 25), 5)
    num_players_entry.draw(num_players_win)
    num_players_win.getMouse() # wait for mouse
    num_players = int(num_players_entry.getText())
    num_players_win.close()
    #TODO add continue buttons
    # Player names
    names_win = GraphWin("Connect L&G - Names", 500, 50*num_players)
    name_entries = []
    for i in range(num_players):
        name_label = Text(Point(75, 25*(i+1)), "Name or AI_#:")
        name_label.draw(names_win)
        name_entry = Entry(Point(250, 25*(i+1)), 20)
        name_entry.draw(names_win)
        name_entries.append(name_entry)
    names_win.getMouse()
    names = []
    for name_entry in name_entries:
        name = name_entry.getText()
        names.append(name)
    names_win.close()
    return names

#main / initialize
def main():
    names = pregame()
    win, circles, turn_text = graphics_setup()
    pieces = pieces_setup()

    game_loop(win, circles, pieces, turn_text, names)
    win.close()    # Close window when done

if __name__ == "__main__":
    main()
