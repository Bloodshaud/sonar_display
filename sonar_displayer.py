import math
import tkinter as tk
import serial


class Point:
    """
    Simple point class for pretty code
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"


def limit(value: int, bound: int):
    """
    Simple helper-method for limiting a value to stay inside radar

    :param value: value to be limited
    :param bound: limit to be respected. Must be positive
    :return: max(min(value, limit), -limit)
    """
    return max(min(value, bound), -bound)


class Radar:

    def __init__(self, com_port: str, baudrate: int):
        self.serial = serial.Serial(com_port, baudrate)

        root = tk.Tk()
        root.title('Radar')
        canvas = tk.Canvas(root, width=600, height=600)
        canvas.pack(expand=True, fill=tk.BOTH)

        self.canvas = canvas
        self.read_loop()

    def draw(self, point):
        """
        Method for drawing point onto canvas

        :param point: point to draw
        """
        self.canvas.delete("all")

        self.canvas.create_oval(0, 0, 600, 600, width=4, fill='darkgreen', outline='green')
        self.canvas.create_oval(200, 200, 400, 400, width=1, outline='green')
        self.canvas.create_oval(100, 100, 500, 500, width=1, outline='green')
        self.canvas.create_oval(300, 300, 300, 300, width=4, outline='green')

        if point is not None:
            x = point.x + 300
            y = 300 - point.y
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, width=1, fill='red')
        self.canvas.update()

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

            x = int(min(distance, 300) * math.cos(math.radians(angle)))
            y = int(distance * math.sin(math.radians(angle)))

            self.draw(Point(x, y))


if __name__ == "__main__":
    radar = Radar("COM3", 9600)
