from tkinter import *
import requests

#ключ openweather
key = 'ceb0bd8f8cd3ba0ad04a3dae3fbc747d'

# получить "красивый" словарь
def getDict (data):
    if data.get('list') is None:
        weather_info = dict(
            s_city=data['name'],
            desc=data['weather'][0]['description'],
            main=data['weather'][0]['main'],
            temp=round(data['main']['temp']),
            maxTemp=round(data['main']['temp_min']),
            minTemp=round(data['main']['temp_max']),
            windSpeed=round(data["wind"]["speed"]),
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            visibility=data['visibility'],
            date=data['dt']/60/60/24
        )
    else:
        weather_info = {}
        for d in data['list']:
            if "12:00:00" in d['dt_txt']:
                weather_info[d['dt_txt']] = dict(
                    s_city=data['city']['name'],
                    desc=d['weather'][0]['description'],
                    main=d['weather'][0]['main'],
                    temp=round(d['main']['temp']),
                    maxTemp=round(d['main']['temp_min']),
                    minTemp=round(d['main']['temp_max']),
                    windSpeed=round(d["wind"]["speed"]),
                    humidity=d['main']['humidity'],
                    pressure=d['main']['pressure'],
                    visibility=d['visibility'],
                    date=d['dt_txt'],
                )
            if len(weather_info.keys()) == 7:
                break

    return weather_info

# получить погоду на день
def getWeatherDay():
    try:
        city = cityField.get()
        weather = getDict(requests.get('http://api.openweathermap.org/data/2.5/weather',
                            params={'APPID': key, 'q': city, 'units': 'metric', 'lang': 'en'}).json())
        # Полученные данные добавляем в текстовую надпись для отображения пользователю
        info['text'] = f"{weather['s_city']} weather information."
        weatherLabel['text'] = f"In {weather['s_city']} {weather['desc']} today\n" \
                               f"Temperature {weather['temp']} °C\n" \
                               f"Wind speed {weather['windSpeed']} m/s\n" \
                               f"Max. temp {weather['maxTemp']} °C\n" \
                               f"Min. temp {weather['minTemp']} °C\n" \
                               f"Humidity {weather['humidity']} g/m\n" \
                               f"Visibility {weather['visibility']} m"
    except:
        weatherLabel['text'] = "Weather not found"

# получить погоду на неделю
def getWeatherWeek():
    try:
        city = cityField.get()
        weather = getDict(requests.get('http://api.openweathermap.org/data/2.5/forecast',
                                       params={'APPID': key, 'q': city, 'units': 'metric', 'lang': 'en'}).json())
        weatherLabel['text'] = ""

        for i in weather.keys():
            info['text'] = f"{weather[i]['s_city']} weather information."
            weatherLabel['text'] += f"{weather[i]['date'][:10]}:                      \n" \
                                    f"{weather[i]['main']}, {weather[i]['temp']} °C\n" \
                                    f"{weather[i]['windSpeed']} m/s, {weather[i]['visibility']} m\n\n"
    except:
        weatherLabel['text'] = "Weather not found"

# Настройки главного окна tKinter
root = Tk()
root.title('Weather forecast')
root.geometry('350x580')
root.resizable(width=False, height=False)

# настройки интерфейса
menuSize = 0.26
colorTop = '#00a8b4'
colorBot = '#00c8d4'
colorLight = '#00d8e4'
colorBtActBg ="#0098a4"
fontMain = "Helvetica 10"
btnWidth = 26

# фрейм
frame_top = Frame(root, bg=colorTop, bd=0)
frame_top.place(relwidth=1, relheight=menuSize)
frame_bottom = Frame(root, bg=colorBot, bd=0)
frame_bottom.place(rely=menuSize, relwidth=1, relheight=1 - menuSize)

# поле ввода
cityField = Entry(frame_top, bg=colorLight, font="Helvetica 15", width=24)
cityField.pack(pady=20)

# кнопки
btn = Button(frame_top, text='Weather for today', command=getWeatherDay, bg=colorLight, font=fontMain, activebackground=colorBtActBg, width=btnWidth)
btn.pack(pady=0)
btn2 = Button(frame_top, text='Weather for the week', command=getWeatherWeek, bg=colorLight, font=fontMain, activebackground=colorBtActBg, width=btnWidth)
btn2.pack(pady=10)

# текст
info = Label(frame_bottom, text='Enter a city to search for weather',fg="#ffffff", bg=colorBot, font="Helvetica 12")
info.pack(pady=10)
weatherLabel = Label(frame_bottom, justify=LEFT, text='Weather information',fg="#ffffff", bg=colorBot, font="Helvetica 12")
weatherLabel.pack(pady=0)

root.mainloop()