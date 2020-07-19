<<<<<<< HEAD
import os
from tkinter import Canvas, Tk
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

WEATHER_KEY = "d4996d8ccefb306921a70705b6779e2a"

RED = "#FF4136"
GREEN = "#2ECC40"
YELLOW = "#FFDC00"

class OpenWeatherMap:
    APPID = 'c73d9cdb31fd6a386bee66158b116cd0'

    def __init__(self):
        self.url = "http://api.openweathermap.org/data/2.5/weather?appid={appid}&q={city}&units=metric"
        self.json = {}

    def get_city(self, city):
        url = self.url.format(appid=OpenWeatherMap.APPID, city=city)
        self.json = requests.get(url).json()
        return self.json

    def get(self, key):
        return self.json['main'][key]

    def get_icon_data(self):
        icon_id = self.json['weather'][0]['icon']
        url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)
        response = requests.get(url, stream=True)
        return response.content

def weather(latitude, longitude, units="imperial"):
    result = requests.get(
        f"""https://api.openweathermap.org/data/2.5/weather?lat={
            latitude
        }&lon={longitude}&appid={WEATHER_KEY}&units={units}"""
    ).json()

    return {"temperature": result["main"]["temp"], "icon": result['weather'][0]['icon']}

def coordinates():
    result = requests.get("https://ipinfo.io/").json()["loc"].split(",")

    return float(result[0]), float(result[1])


class App(object):
    def __init__(self, dimensions=(200, 200)):
        self._window = Tk()
        self._dimensions = dimensions

        self._window.geometry(f"{dimensions[0]}x{dimensions[1]}")
        self._window.resizable(False, False)

        self._canvas = Canvas(self._window)
        self._canvas.pack(expand=True, fill="both")
        
        owm = OpenWeatherMap()
        owm.get_city('Fremont,ca,uas')

        temperature = owm.get('temp') # this doesn't do anything right now but I left it
        
        icon = owm.get_icon_data()
        img = Image.open(BytesIO(icon)) # this opens normal PIL Image
        img = ImageTk.PhotoImage(img) # this opens ImageTk from earlier image

        self._milliseconds = 60000
        self._coordinates = coordinates()

        self._update(img) # update gets the image created earlier
        self._window.mainloop()

    def _update(self, img):
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
        xpos = 70 # this controls where the image appears on canvas in respect to X axis
        ypos = 70 # this controls where the image appears on canvas in respect to Y axis
        self._canvas.create_image((xpos, ypos), image=img, anchor='nw') # after canvas' color was updated we are drawing the image on it
        self._window.after(self._milliseconds, self._update)


if __name__ == "__main__":
    app = App()
=======
import os
from tkinter import Canvas, Tk

import requests
from PIL import Image as PILImage
from PIL import ImageTk as PILImageTk
import matplotlib.colors as colors
import numpy as np

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]


WEATHER_KEY = "d4996d8ccefb306921a70705b6779e2a"

def weather(latitude, longitude, units="imperial"):
    result = requests.get(
        f"""https://api.openweathermap.org/data/2.5/weather?lat={
            latitude
        }&lon={longitude}&appid={WEATHER_KEY}&units={units}"c"""
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
    def __init__(self,dimensions=(200, 200)):
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
    #def color(self):
        

    def _update(self):
        temperature = weather(*self._coordinates)["temperature"]
        low_temp = 55
        high_temp = 350
        r = temperature
        g = 0
        b = temperature

        r = max(min(high_temp, temperature), low_temp) # makes sure that r is within low_temp - high_temp range
        b = max(min(high_temp, temperature), low_temp) # makes sure that r is within low_temp - high_temp range
        r = (r - low_temp) / (high_temp - low_temp)
        b = 1.0 - ((b - low_temp) / (high_temp - low_temp))

        hex = colors.rgb2hex((r, g, b))
        print(str(r) + ' ' + str(g) + ' ' + str(b) + ' ')
        print(hex)
        print(temperature)
        self._canvas.delete("all")
        if 70 <= temperature <= 80:
            #if temperature > 70/;kin;l,j 
                #r += temperature
            self._canvas.create_rectangle(0, 0, *self._dimensions, fill=hex)
        elif 65 <= temperature <= 85:
            self._canvas.create_rectangle(
                0, 0, *self._dimensions, fill=hex
            )
        else:
           self._canvas.create_rectangle(0, 0, *self._dimensions, fill=hex)

        #image
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
>>>>>>> 9f586d2... to test on pycharm, so this is not the final code
