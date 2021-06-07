import numpy as np
import ephem
import math
import spacetrack.operators as op
from datetime import datetime, date, timedelta, timezone
from spacetrack import SpaceTrackClient
from app.trajectory import get_spacetrack_tle, get_position_in_time

username = 'Jhenyaik3d@yandex.ru'
password = 'Donttouchthis!7'

def create_orbital_track(norad, username, password):
    tle_1, tle_2 = get_spacetrack_tle(norad, username, password, True)
    if not tle_1 or not tle_2:
        return ([])
    num_timestamp = 1440 // 5
    utc_hh = np.zeros((num_timestamp, 1))
    utc_mm = np.zeros((num_timestamp, 1))
    utc_ss = np.zeros((num_timestamp, 1))
    utc_now = datetime.now(timezone.utc)
    lat = []
    lon = []

    i = 0
    minutes = 0
    while minutes < 1440:
        utc_hour = int(minutes // 60)
        utc_minutes = int((minutes - (utc_hour * 60)) // 1)
        utc_seconds = int(round((minutes - (utc_hour * 60) - utc_minutes) * 60))
        utc_hh[i] = utc_hour
        utc_mm[i] = utc_minutes
        utc_ss[i] = utc_seconds

        utc_time = datetime(utc_now.year, utc_now.month, utc_now.day, utc_hour, utc_minutes, utc_seconds)
        loc = get_position_in_time(tle_1, tle_2, utc_time)
        lon.append(loc[0])
        lat.append(loc[1])
        i += 1
        minutes += 5
    return lon, lat

def psi_s_13(lat, lat_s, lon, lon_s):
    internal = np.sin(lat) * np.sin(lat_s) + np.cos(lat) * np.cos(lat_s) * np.cos(lon_s - lon)
    return np.arccos(internal)


def alpha_s_13(lat, lat_s, psi_s, lon, lon_s):
    num = np.sin(lat_s)-np.sin(lat)*np.cos(psi_s)
    denum = np.sin(psi_s)*np.cos(lat)
    ret = np.arccos(num/denum)
    for i in range(len(ret)):
        if lon_s[i] < lon:
            ret[i] = 2*np.pi - ret[i]
    return ret

def tet_s_13(psi_s, r_e, r_s):
    num = np.cos(psi_s)-r_e*1.0/r_s
    denum = np.sin(psi_s)
    return np.arctan(num/denum)

def psi_p_14(tet_s, r_e, h_max):
    internal = (r_e/(r_e + h_max))*np.cos(tet_s)
    return np.pi/2 - tet_s - np.arcsin(internal)

def fp_14(lat, psi_p, alpha_s):
    internal = np.sin(lat)*np.cos(psi_p)+np.cos(lat)*np.sin(psi_p)*np.cos(alpha_s)
    return np.arcsin(internal)

def lp_14(lon, psi_p, alpha_s, fp):
    internal = np.sin(psi_p)*np.sin(alpha_s)/np.cos(fp)
    return lon + np.arcsin(internal)

class site_class:
    def __init__(self):
        self.ID = 0
        self.Name = "noname"
        self.Lat = 0
        self.Lon = 0
        self.Alt = 0

def find_corresponding_ionosphere_spots(site, latitude, longitude):
    latitude_rad_copy = np.deg2rad(np.copy(latitude))
    longitude_rad_copy = np.deg2rad(np.copy(longitude))
    site_lat_copy = np.deg2rad(site.Lat)
    site_lon_copy = np.deg2rad(site.Lon)
    r_e = 6378137
    r_s = 20180000
    h_max = 280000

    psi_s = psi_s_13(site_lat_copy, latitude_rad_copy,site_lon_copy, longitude_rad_copy)
    alpha_s = alpha_s_13(site_lat_copy, latitude_rad_copy, psi_s, site_lon_copy, longitude_rad_copy)
    tet_s = tet_s_13(psi_s, r_e, r_s)

    psi_p = psi_p_14(tet_s, r_e, h_max)
    fp = fp_14(site_lat_copy, psi_p, alpha_s)
    lp = lp_14(site_lon_copy, psi_p, alpha_s, fp)

    return np.rad2deg(fp), np.rad2deg(lp)


def create_ion_track(norad):
    prev = [0, 0]
    coordinates = []
    longitude, latitude = create_orbital_track(norad, username, password)
    kzn = site_class()
    kzn.ID = 'GNSS1'
    kzn.Name = 'Казань'
    kzn.Lat = 55.7916
    kzn.Lon = 49.1181
    kzn.Alt = 96.441
    ion_sp_lat, ion_sp_lon = find_corresponding_ionosphere_spots(kzn, latitude, longitude)

    for i in range(0, len(ion_sp_lon) - 1):
        loc = [ion_sp_lon[i], ion_sp_lat[i]]
        if (prev and loc[0] > prev[0]):
            coordinates.append([prev, loc])
        prev = loc

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "id": 1
                },
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": coordinates,
                },
            },
        ],
    }


def get_ion(norad):
    return create_ion_track(norad)