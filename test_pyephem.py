from datetime import datetime, date, timedelta
import spacetrack.operators as op
import ephem
import numpy as np
import math
import matplotlib.pyplot as plt

# Главный класс для работы с space-track
from spacetrack import SpaceTrackClient

username = 'Jhenyaik3d@yandex.ru'
password = 'Donttouchthis!7'
 
# На вход она потребует идентификатор спутника, диапазон дат, имя
# пользователя и пароль. Опциональный флаг для последних данных tle
def get_spacetrack_tle (sat_id, start_date, end_date, username, password, latest=False):
    st = SpaceTrackClient(identity=username, password=password)
    if not latest:
        # Определяем диапазон дат через оператор библиотеки
        daterange = op.inclusive_range(start_date, end_date)
        # Собственно выполняем запрос через st.tle
        data = st.tle(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle', epoch = daterange)
    else:
        # Выполнение запроса для актуального состояния
        # Выполняем запрос через st.tle_latest
        data = st.tle_latest(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle')
    if not data:
        return 0, 0
    tle_1 = data[0:69]
    tle_2 = data[70:139]
    # 1 43647U 18078A   20106.75264258 -.00000123 +00000-0 +10000-3 0  9997
    # 2 43647 055.1906 017.7776 0007807 342.6828 230.8394 01.86232803010207
    return tle_1, tle_2
  
# задаем количество отсчетов
step = 5 
num_timestamp = 1440 // step

longitude = np.zeros((num_timestamp,1))
latitude = np.zeros((num_timestamp,1))

utc_hh = np.zeros((num_timestamp,1))
utc_mm = np.zeros((num_timestamp,1))
utc_ss = np.zeros((num_timestamp,1))

name = "GPS";

# На вход будем требовать идентификатор спутника, день (в формате date (y,m,d))
# шаг в минутах для определения положения спутника, путь для результирующего файла
def create_orbital_track_for_day(sat_id, track_day, step_minutes):
    # Если запрошенная дата наступит в будущем, то запрашиваем самые последний набор TLE 
    if track_day > date.today():
        tle_1, tle_2 = get_spacetrack_tle (sat_id, None, None, username, password, True)
    # Иначе на конкретный период, формируя запрос для указанной даты и дня после неё
    else:
        tle_1, tle_2 = get_spacetrack_tle (sat_id, track_day, track_day + timedelta(days = 1), username, password, False)
    if not tle_1 or not tle_2:
        print('Impossible to retrieve TLE')        
        exit(1)
 
    i = 0
    minutes = 0
    while minutes < 1440:
        # Расчитаем час, минуту, секунду (для текущего шага)
        utc_hour = int(minutes // 60)
        utc_minutes = int((minutes - (utc_hour * 60)) // 1)
        utc_seconds = int(round((minutes - (utc_hour * 60) - utc_minutes) * 60))
        utc_hh[i]= utc_hour
        utc_mm[i]= utc_minutes
        utc_ss[i]= utc_seconds
 
        # Сформируем строку для атрибута
        utc_string = str(utc_hour) + '-' + str(utc_minutes) + '-' + str(utc_seconds)
        # И переменную с временем текущего шага в формате datetime
        utc_time = datetime(track_day.year,track_day.month,track_day.day,utc_hour,utc_minutes,utc_seconds)
 
        # Считаем положение спутника
        tle_rec = ephem.readtle(name, tle_1, tle_2);
        tle_rec.compute(utc_time);

        longitude[i] = tle_rec.sublong * 180 / math.pi
        latitude[i]  = tle_rec.sublat * 180 / math.pi

        # Не забываем про счётчики
        i += 1
        minutes += step_minutes

create_orbital_track_for_day(43647, date(2020, 4, 15), 5)
utc_sec=np.zeros((num_timestamp,2))
i = 0
while i < num_timestamp:
    utc_sec[i, 0] = (utc_hh[i, 0] * 3600) + (utc_mm[i, 0] * 60) + (utc_ss[i, 0])
    time = str(math.floor(utc_hh[i, 0])) + ':' + str(math.floor(utc_mm[i, 0])) + ':' + str(math.floor(utc_ss[i, 0]))
    i += 1  

#рисунок 1
dpi = 150     
fig = plt.figure(dpi = dpi, figsize = (1920 / dpi, 1080/ dpi) )

plt.title('Track BEIDOU 3M15 15.04.2020')
plt.ylabel('Широта')
plt.xlabel('Долгота')
plt.scatter(longitude[0:num_timestamp, 0], latitude[0:num_timestamp, 0], color = 'blue', linestyle = 'solid',
label = 'Track BEIDOU 3M15 NORAD ID: 43647')
for i, txt in enumerate(utc_sec):
    plt.annotate(str(math.floor(utc_hh[i, 0])) + ':' + str(math.floor(utc_mm[i, 0])) + ':' + str(math.floor(utc_ss[i, 0])), (longitude[i] + 0.15, latitude[i] + 0.15))
plt.scatter(46.10, 56.15, color = 'red', linestyle = 'solid')
plt.text(46.20, 56.30,  'Sura')

plt.scatter(49.1181, 55.7916, color = 'red', linestyle = 'solid')
plt.text(49.1181, 55.7916,  'Казань')

plt.legend(loc = 'upper right')
fig.savefig('Track_BEIDOU 3M15 15042020.png')
