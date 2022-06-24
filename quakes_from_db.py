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
            raise ConnectDatabaseError(exc.msg)

    return wrapper


def get_sql_query(from_dt, to_dt, comment, sta, from_mag, to_mag: str) -> str:
    sta = '' if sta == 'ALL' else sta
    return f"SELECT" \
           f" o.EVENTID, FROM_UNIXTIME(o.ORIGINTIME), o.LAT, o.LON," \
           f" o.`DEPTH`, SUBSTR(o.COMMENTS, 20), a.STA, ROUND(a.DIST, 3)," \
           f" ROUND(a.AZIMUTH, 3), a.IPHASE, CONCAT(a.IM_EM, a.FM)," \
           f" FROM_UNIXTIME(a.ITIME), ROUND(a.AMPL, 3), ROUND(a.PER, 2)," \
           f" ROUND(a.ML, 1), ROUND(a.MPSP, 1) " \
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
    with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def get_quakes(data_lst: Iterable[tuple]) -> tuple[Quake]:
    quakes = []
    _id = origin_dt = lat = lon = depth = reg = ''
    sta_lst = []
    for data in data_lst:
        if data[0] != _id:
            if len(sta_lst) != 0:
                quakes.append(
                    Quake(_id, origin_dt, lat, lon, depth, reg, tuple(sta_lst)))
                sta_lst.clear()
            _id, origin_dt, lat, lon, depth, reg = data[:6]
        sta_lst.append(Sta(*data[6:]))
    quakes.append(Quake(_id, origin_dt, lat, lon, depth, reg, tuple(sta_lst)))
    return tuple(quakes)
