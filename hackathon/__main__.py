import os
from tkinter import Canvas, Tk

import requests
from PIL import Image as PILImage
from PIL import ImageTk as PILImageTk
import random

r= random.randint(255)
b= random.randint(255)
g= random.randint(255)

rgb=(r,b,g)

WEATHER_KEY = "d4996d8ccefb306921a70705b6779e2a"

RED = "#FF4136"
GREEN = "#2ECC40"
YELLOW = "#FFDC00"


def weather(latitude, longitude, units="imperial"):
    result = requests.get(
        f"""https://api.openweathermap.org/data/2.5/weather?lat={
            latitude
        }&lon={longitude}&appid={WEATHER_KEY}&units={units}"""
    ).json()

    return {"temperature": result["main"]["temp"]}


def coordinates():
    result = requests.get("https://ipinfo.io/").json()["loc"].split(",")

    return float(result[0]), float(result[1])


class Image(object):
    def __init__(self, path, dimensions=(None, None)):
        self._image = PILImage.open(path)

        if tuple(dimensions) != (None, None):
            self.resize(dimensions)

        self._tk_image = None

    def resize(self, dimensions):
        self._image = self._image.resize(dimensions)

        try:
            self._tk_image = PILImageTk.PhotoImage(self._image)
        except RuntimeError:
            self._tk_image = None

    def tk_image(self):
        if self._tk_image is None:
            try:
                self._tk_image = PILImageTk.PhotoImage(self._image)
            except RuntimeError:
                self._tk_image = None

        return self._tk_image


class App(object):
    def __init__(self, dimensions=(200, 200)):
        self._window = Tk()
        self._dimensions = dimensions

        self._window.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self._window.resizable(False, False)

        self._canvas = Canvas(self._window)
        self._canvas.pack(expand=True, fill="both")

        self._image = Image(
            os.path.sep.join(
                (
                    os.path.dirname(os.path.abspath(__file__)),
                    "Picture",
                    "Show weather in Bear.png",
                )
            )
        )
        self._image.resize(self._dimensions)

        self._milliseconds = 60000
        self._coordinates = coordinates()

        self._update()
        self._window.mainloop()

    def _update(self):
        temperature = weather(*self._coordinates)["temperature"]
        self._canvas.delete("all")

        if 70 <= temperature <= 80:
            self._canvas.create_rectangle(0, 0, *self._dimensions, fill="green")
        elif 65 <= temperature <= 85:
            self._canvas.create_rectangle(
                0, 0, *self._dimensions, fill="yellow"
            )
        else:
            self._canvas.create_rectangle(0, 0, *self._dimensions, fill="red")

        # image
        self._canvas.create_image(
            0, 0, image=self._image.tk_image(), anchor="nw"
        )

        # emoji
        # canvas.create_text(
        #     self.dimensions[0] / 2,
        #     self.dimensions[1] / 2,
        #     text="☀️",
        #     font=("Helvetica", self.dimensions[1]),
        # )

        self._window.after(self._milliseconds, self._update)


if __name__ == "__main__":
    app = App()
