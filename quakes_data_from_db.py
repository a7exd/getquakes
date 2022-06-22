# -*- coding: utf-8 -*-
from typing import Iterable
from mysql.connector import connect, Error
from mysql.connector.abstracts import MySQLConnectionAbstract
import config
from exceptions import ConnectDatabaseError
from quake_structures import Quake, Sta


def connect_decorator(func):
    
    def wrapper(args):
        try:
            with connect(**config.DB) as conn:
                return func(*args, conn=conn)
        except Error as exc:
            print(exc)  # TODO to log
            raise ConnectDatabaseError

    return wrapper


def get_sql_query(from_dt, to_dt, comment, sta, from_mag, to_mag: str) -> str:
    sta = '' if sta == 'ALL' else sta
    return f"SELECT" \
           f" o.EVENTID, FROM_UNIXTIME(o.ORIGINTIME), o.LAT, o.LON," \
           f" o.`DEPTH`, o.COMMENTS, a.STA, a.DIST, a.AZIMUTH, a.IPHASE," \
           f" CONCAT(a.IM_EM, a.FM), FROM_UNIXTIME(a.ITIME), a.AMPL, a.PER," \
           f" a.ML, a.MPSP " \
           f"FROM origin o " \
           f"INNER JOIN arrival a ON a.EVENTID = o.EVENTID " \
           f"WHERE" \
           f" (o.COMMENTS LIKE '%{comment}%')" \
           f" AND" \
           f" (FROM_UNIXTIME(o.ORIGINTIME) BETWEEN '{from_dt}' AND '{to_dt}')" \
           f" AND (a.STA LIKE '%{sta}%')" \
           f" AND ((a.ML BETWEEN {from_mag} AND {to_mag}) OR" \
           f"    (a.MPSP BETWEEN {from_mag} AND {to_mag}))" \
           f" ORDER BY o.ORIGINTIME"


@connect_decorator
def get_data(from_dt, to_dt, comment, sta, from_mag, to_mag: str,
             conn: MySQLConnectionAbstract)\
        -> list[tuple]:
    """Returns data of quakes from DB"""
    sql = get_sql_query(from_dt, to_dt, comment, sta, from_mag, to_mag)
    print(sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    return data


def get_quakes(data_lst: Iterable[tuple]) -> tuple[Quake]:
    quakes = []
    _id = origin_dt = lat = lon = depth = reg = ''
    sta_lst = []
    for data in data_lst:
        if data[0] != _id:
            if len(sta_lst) != 0:
                quakes.append(
                    Quake(_id, origin_dt, lat, lon, depth, reg, sta_lst))
            _id, origin_dt, lat, lon, depth, reg = data[:6]
        sta_lst.append(Sta(*data[6:]))
    return tuple(quakes)
