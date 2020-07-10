import tkinter

import requests
from PIL import Image as PILImage
from PIL import ImageTk as PILImageTk

KEY = "d4996d8ccefb306921a70705b6779e2a"


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


def get_weather(latitude, longitude, units="imperial"):
    return requests.get(
        f"""https://api.openweathermap.org/data/2.5/weather?lat={
            latitude
        }&lon={longitude}&appid={KEY}&units={units}"""
    ).json()


def get_location():
    return requests.get("https://ipinfo.io/").json()["loc"].split(",")


root = tkinter.Tk()
root.geometry(f"80x80")
canvas = tkinter.Canvas(root, width=80, height=80)
canvas.pack(expand=True, fill="both")
root.resizable(False, False)


def update():
    temperature = float(get_weather(*get_location())["main"]["temp"])
    print(temperature)

    if 70 <= temperature <= 80:
        canvas.create_rectangle(0, 0, 80, 80, fill="green")
    elif 65 <= temperature <= 85:
        canvas.create_rectangle(0, 0, 80, 80, fill="yellow")
    else:
        canvas.create_rectangle(0, 0, 80, 80, fill="red")

    root.after(2000, update)


update()
root.after(2000, update)
root.mainloop()
