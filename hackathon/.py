import tkinter as tk
import requests, base64

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
        return base64.encodebytes(response.raw.read())


class OWIconLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        weather_icon = kwargs.pop('weather_icon', None)
        if weather_icon is not None:
            self.photo = tk.PhotoImage(data=weather_icon)
            kwargs['image'] = self.photo

        super().__init__(parent, **kwargs)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("220x120+0+0")

        owm = OpenWeatherMap()
        owm.get_city('karachi')

        temperature = owm.get('temp')

        temp_icon = OWIconLabel(self, weather_icon=owm.get_icon_data())
        temp_icon.grid(row=900, column=900)


if __name__ == '__main__':
    App().mainloop()