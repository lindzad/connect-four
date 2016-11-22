import struct
from time import sleep

from twisted.internet import reactor, protocol

from main import graphics_setup, pieces_setup, on_click
from logic import board_won


def make_server(waiting_win):
    port = 8000
    factory = ConnectServerFactory(waiting_win)
    factory.protocol = ConnectServer
    reactor.listenTCP(port,factory)
    print("Listening as Server on port {}".format(port))

def on_receive(self, data):
    x,y = struct.unpack("<BB", data)
    self.circles[x][y].setFill(self.other[1])
    self.pieces[x][y] = self.other[0]
    #check for their win
    winner=board_won(self.pieces, 2)
    if winner==self.other[0]:
        self.turn_text.setText("They Won!")
        self.turn_text.setTextColor(self.other[1])
        if not self.win.isClosed():
            self.win.getMouse()
            self.win.close()
            reactor.stop()
        return
    #make our move
    self.turn_text.setText("Your Turn")
    pnt = self.win.getMouse() # wait for click
    pt = on_click(pnt, self.circles, self.pieces, self.player, self.circles_margin, self.col_width)
    while pt == (-1,-1):
        pnt = self.win.getMouse()
        pt = on_click(pnt, self.circles, self.pieces, self.player, self.circles_margin, self.col_width)
    data = struct.pack("BB", pt[0], pt[1])
    self.transport.write(data)
    self.turn_text.setText("Their Turn")
    #check for our win
    winner=board_won(self.pieces, 2)
    if winner==self.player[0]:
        self.turn_text.setText("You Won!")
        self.turn_text.setTextColor(self.player[1])

def on_connect(self):
    self.transport.setTcpNoDelay(True)
    self.factory.waiting_win.close()
    self.win, self.circles, self.turn_text, self.circles_margin, self.col_width = graphics_setup()
    self.pieces = pieces_setup()

def on_lost(self):
    text = self.turn_text.getText()
    self.turn_text.setText(text+" Connection Lost")
    if not self.win.isClosed():
        self.win.getMouse()
        self.win.close()
    if reactor.running:
        reactor.stop()


class ConnectClient(protocol.Protocol):

    def connectionMade(self):
        print("Connected to Server!")
        on_connect(self)
        self.player = (1, "red")
        self.other = (0, "yellow")
        # first turn of the game
        self.turn_text.setText("Your Turn")
        pnt = self.win.getMouse() # wait for click
        pt = on_click(pnt, self.circles, self.pieces, self.player, self.circles_margin, self.col_width)
        while pt == (-1,-1):
            pnt = self.win.getMouse()
            pt = on_click(pnt, self.circles, self.pieces, self.player, self.circles_margin, self.col_width)
        data = struct.pack("BB", pt[0], pt[1])
        self.transport.write(data)
        self.turn_text.setText("Their Turn")

    def dataReceived(self, data):
        print("Server said:", data)
        on_receive(self, data)

    def connectionLost(self, reason):
        print("Connection to Server lost")
        on_lost(self)

class ConnectClientFactory(protocol.ClientFactory):
    protocol = ConnectClient

    def __init__(self, waiting_win):
        self.waiting_win = waiting_win

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed. Reverting to Server...")
        make_server(self.waiting_win)


class ConnectServer(protocol.Protocol):

    def __init__(self, waiting_win):
        self.waiting_win = waiting_win

    def connectionMade(self):
        print("Connected to Client!")
        on_connect(self)
        self.turn_text.setText("Their Turn")
        self.player = (0, "yellow")
        self.other = (1, "red")

    def dataReceived(self, data):
        print("Client Said: {}".format(data))
        on_receive(self, data)

    def connectionLost(self, reason):
        print("Connection to Client lost")
        on_lost(self)

class ConnectServerFactory(protocol.ServerFactory):
    protocol = ConnectServer

    def __init__(self, waiting_win):
        self.waiting_win = waiting_win

    def buildProtocol(self, addr):
        return self.protocol(self.waiting_win)
