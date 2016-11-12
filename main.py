from graphics import *

def main():
    win = GraphWin("Connect L&G", 940, 810) # x, y
    #c = Circle(Point(80,80), 50) # Point(x,y), radius
    circles = [ [ Circle(Point(80+x*130, 80+y*130), 50) for y in range(6)] for x in range(7)]
    for col in circles:
        for circle in col:
            circle.draw(win)

    print(win.getMouse()) # Pause to view result
    win.close()    # Close window when done

main()
