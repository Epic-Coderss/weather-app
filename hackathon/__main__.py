from io import BytesIO
from tkinter import Canvas, Tk

import requests
from PIL import Image, ImageTk

WEATHER_KEY = "d4996d8ccefb306921a70705b6779e2a"


def rgb2hex(red, green, blue):
    return f"#{red:02x}{green:02x}{blue:02x}"


def weather(latitude, longitude, units="imperial"):
    result = requests.get(
        f"""https://api.openweathermap.org/data/2.5/weather?lat={
            latitude
        }&lon={longitude}&appid={WEATHER_KEY}&units={units}"""
    ).json()

    icon = requests.get(
        f"""http://openweathermap.org/img/wn/{
            result["weather"][0]["icon"]
        }@4x.png"""
    )

    return {
        "temperature": result["main"]["temp"],
        "icon": icon.content,
    }


def coordinates():
    result = requests.get("https://ipinfo.io/").json()["loc"].split(",")

    return float(result[0]), float(result[1])


class App(object):
    def __init__(self, dimensions=(150, 150)):
        self._window = Tk()
        self._dimensions = dimensions

        self._window.geometry(f"{self._dimensions[0]}x{self._dimensions[1]}")
        self._window.resizable(False, False)
        self._window.title("Weather")

        self._canvas = Canvas(self._window)
        self._canvas.pack(expand=True, fill="both")

        self._milliseconds = 60000
        # cache coordinates
        self._coordinates = coordinates()

        # property for keeping a reference to original image
        self._icon = None

        self._update()
        self._window.mainloop()

    def _update(self):
        weather_result = weather(*self._coordinates)

        temperature = weather_result["temperature"]

        low_temperature = 0
        high_temperature = 100

        red = max(min(high_temperature, temperature), low_temperature)
        green = 0
        blue = max(min(high_temperature, temperature), low_temperature)

        red = (red - low_temperature) / (high_temperature - low_temperature)
        blue = 1.0 - (
            (blue - low_temperature) / (high_temperature - low_temperature)
        )

        final_hex = rgb2hex((red, green, blue))
        icon_size = min(self._dimensions)

        # use property to prevent garbage collection of icon before display
        self._icon = BytesIO(weather_result["icon"])
        self._icon = Image.open(self._icon)
        self._icon = self._icon.resize((icon_size, icon_size))
        self._icon = ImageTk.PhotoImage(self._icon)

        self._canvas.delete("all")

        self._canvas.create_rectangle(0, 0, *self._dimensions, fill=final_hex)

        self._canvas.create_image(
            (self._dimensions[0] / 2) - (icon_size / 2),
            (self._dimensions[1] / 2) - (icon_size / 2),
            image=self._icon,
            anchor="nw",
        )

        self._window.after(self._milliseconds, self._update)


if __name__ == "__main__":
    app = App()
