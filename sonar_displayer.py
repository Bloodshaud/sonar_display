import math
import time
import tkinter as tk

import serial


class Point:
    """
    Simple point class
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Radar:

    def __init__(self, hardware_port: str, baudrate: int, point_lifetime: int):
        """
        Application for displaying distance information from a sonar or a radar on arduino or a similar device.

        :param hardware_port: port to read input from. Usually COM or dev/tty
        :param baudrate: baudrate for readings
        :param point_lifetime: how long a point is displayed after detection
        """
        self.serial = serial.Serial(hardware_port, baudrate)
        self.point_lifetime = point_lifetime
        root = tk.Tk()
        root.title('Radar')
        canvas = tk.Canvas(root, width=600, height=310)
        canvas.pack(expand=True, fill=tk.BOTH)

        self.canvas = canvas
        self.points = []
        self.draw()
        self.read_loop()

    def draw(self):
        """
        Method for drawing point onto canvas

        Points are read from field var points.
        They are displayed for a fixed number of seconds, defined in class constructor
        """
        self.canvas.delete("all")
        self.draw_basis()

        new_points = []
        now = time.time()

        for (point, ts) in self.points:
            x = point.x + 300
            y = 300 - point.y
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, width=1, fill='red')

            if now < (ts + self.point_lifetime):
                new_points.append((point, ts))

        self.points = new_points
        self.canvas.update()

    def draw_basis(self):
        """
            Method for drawing background
        """
        self.canvas.create_oval(0, 0, 600, 600, width=4, fill='darkgreen', outline='green')
        self.canvas.create_line(300, 300, 300, 0, width=1, fill='green')
        self.canvas.create_line(300, 300, 600, 300, width=1, fill='green')
        self.canvas.create_line(300, 300, 512, 88, width=1, fill='green')
        self.canvas.create_line(300, 300, 88, 88, width=1, fill='green')
        self.canvas.create_line(300, 300, 0, 300, width=1, fill='green')
        self.canvas.create_oval(100, 100, 500, 500, width=1, outline='green')
        self.canvas.create_oval(200, 200, 400, 400, width=1, outline='green')
        self.canvas.create_oval(300, 300, 300, 300, width=4, outline='green')

    def read_loop(self):
        """
            Reads in an infinite loop from the serial port. Each iteration reads two lines:
                - distance in cm
                - angle in degrees
            These lines are translated into x,y coordinates and drawn onto the canvas
        """
        while True:
            distance = int(self.serial.readline())
            angle = int(self.serial.readline())
            print("distance=" + str(distance) + ", angle=" + str(angle))

            y = int(min(distance, 300) * math.cos(math.radians(angle)))
            x = int(distance * math.sin(math.radians(angle)))

            self.points.append((Point(x, y), time.time()))

            self.draw()


if __name__ == "__main__":
    radar = Radar("COM3", 9600, 5)
