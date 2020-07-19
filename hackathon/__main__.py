import os
from tkinter import Canvas, Tk
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import matplotlib.colors as colors
import numpy as np

WEATHER_KEY = "d4996d8ccefb306921a70705b6779e2a"

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]

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
        owm.get_city('Fremont,CA,USA')

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
            self._canvas.create_rectangle(0, 0, *self._dimensions, fill=hex)
        elif 65 <= temperature <= 85:
            self._canvas.create_rectangle(
                0, 0, *self._dimensions, fill=hex
            )
        else:
            self._canvas.create_rectangle(0, 0, *self._dimensions, fill=hex)
        xpos = 70 # this controls where the image appears on canvas in respect to X axis
        ypos = 80 # this controls where the image appears on canvas in respect to Y axis
        self._canvas.create_image((xpos, ypos), image=img, anchor='nw') # after canvas' color was updated we are drawing the image on it

        self._window.after(self._milliseconds, self._update)


if __name__ == "__main__":
    app = App()
