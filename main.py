from graphics import *

def main():
    win = GraphWin("Connect L&G", 940, 810) # x, y
    c = Circle(Point(80,80), 50) # Point(x,y), radius
    c2 = Circle(Point(210,80), 50)
    c.draw(win)
    c2.draw(win)
    print(win.getMouse()) # Pause to view result
    win.close()    # Close window when done

main()
