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

class ConnectClient(protocol.Protocol):

    def connectionMade(self):
        print("Connected to Server!")
        #self.transport.write(b"hello, world!")
        self.factory.waiting_win.close()
        self.win, self.circles, self.turn_text, self.circles_margin, self.col_width = graphics_setup()
        self.pieces = pieces_setup()
        self.player = (1, "red")
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
        x,y = struct.unpack("<BB", data)
        self.circles[x][y].setFill("yellow")
        self.pieces[x][y] = 2
        #check for their win
        winner=board_won(self.pieces, 2)
        if winner==2:
            self.turn_text.setText("They Won!")
            self.turn_text.setTextColor("yellow")
            while True:
                self.transport.write(data)
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
        if winner==1:
            self.turn_text.setText("You Won!")
            self.turn_text.setTextColor("red")
            # while True:
            #     self.transport.write(data)
            return

    def connectionLost(self, reason):
        print("connection lost")

class ConnectClientFactory(protocol.ClientFactory):
    protocol = ConnectClient

    def __init__(self, waiting_win):
        self.waiting_win = waiting_win

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed. Reverting to Server...")
        make_server(self.waiting_win)

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

class ConnectServer(protocol.Protocol):

    def __init__(self, waiting_win):
        self.waiting_win = waiting_win

    def connectionMade(self):
        print("Connected to Client!")
        self.waiting_win.close()
        self.win, self.circles, self.turn_text, self.circles_margin, self.col_width = graphics_setup()
        self.pieces = pieces_setup()
        self.turn_text.setText("Their Turn")
        self.player = (2, "yellow")

    def dataReceived(self, data):
        print("Client Said: {}".format(data))
        x,y = struct.unpack("<BB", data)
        self.circles[x][y].setFill("red")
        self.pieces[x][y] = 1
        #check for their win
        winner=board_won(self.pieces, 2)
        if winner==1:
            self.turn_text.setText("They Won!")
            self.turn_text.setTextColor("red")
            while True:
                self.transport.write(data)
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
        if winner==2:
            self.turn_text.setText("You Won!")
            self.turn_text.setTextColor("yellow")
            while True:
                self.transport.write(data)
            return


class ConnectServerFactory(protocol.ServerFactory):
    protocol = ConnectServer

    def __init__(self, waiting_win):
        self.waiting_win = waiting_win

    def buildProtocol(self, addr):
        return self.protocol(self.waiting_win)
