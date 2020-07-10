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


root.geometry(f"200x200")
root.overrideredirect(True)
root.withdraw()
root.overrideredirect(False)
root.deiconify()
root.update()
root.resizable(False, False)


canvas = tkinter.Canvas(root)
canvas.pack(expand=True, fill="both")


# x = None
# y = None

# def start_move(event):
#     global x, y

#     x = event.x
#     y = event.y

# def stop_move(event):
#     global x, y

#     x = None
#     y = None

# def do_move(event):
#     global x, y

#     new_x = root.winfo_x() + (event.x - x)
#     new_y = root.winfo_y() + (event.y - y)
#     root.geometry(f"+{new_x}+{new_y}")

# canvas.bind("<ButtonPress-1>", start_move)
# canvas.bind("<ButtonRelease-1>", stop_move)
# canvas.bind("<B1-Motion>", do_move)

def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

canvas.bind("<B1-Motion>", move_window)


def update():
    temperature = float(get_weather(*get_location())["main"]["temp"])
    print(temperature)

    if 70 <= temperature <= 80:
        canvas.create_rectangle(0, 0, 200, 200, fill="green")
    elif 65 <= temperature <= 85:
        canvas.create_rectangle(0, 0, 200, 200, fill="yellow")
    else:
        canvas.create_rectangle(0, 0, 200, 200, fill="red")

    root.after(2000, update)


update()
root.after(2000, update)
root.mainloop()
