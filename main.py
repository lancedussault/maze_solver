from classes import Window, Point, Line

def main ():
    win = Window(800, 600)
    line = Line(Point(50, 50), Point(400, 400))
    line_2 = Line(Point(100, 20), Point(69, 69))
    win.draw_line(line, "black")
    win.draw_line(line_2, "red")
    win.wait_for_close()


main()