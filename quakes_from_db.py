# -*- coding: utf-8 -*-
from typing import Tuple, List, NamedTuple, Set
from mysql.connector import connect, Error
import config
from exceptions import ConnectDatabaseError
from quake_structures import Quake, Sta
from datetime import datetime


class QueryParams(NamedTuple):
    from_dt: str
    to_dt: str
    comment: str
    sta: str
    from_mag: str
    to_mag: str


def get_sql_query(params: QueryParams) -> str:
    sta = '' if params.sta.lower() == 'all' else params.sta
    return f"SELECT" \
           f" o.EVENTID, FROM_UNIXTIME(o.ORIGINTIME), o.LAT, o.LON," \
           f" o.`DEPTH`, SUBSTR(o.COMMENTS, 20), a.STA, ROUND(a.DIST, 3)," \
           f" ROUND(a.AZIMUTH, 3), a.IPHASE, CONCAT(a.IM_EM, a.FM)," \
           f" FROM_UNIXTIME(a.ITIME), ROUND(a.AMPL, 3), ROUND(a.PER, 2)," \
           f" ROUND(a.ML, 1), ROUND(a.MPSP, 1) " \
           f"FROM origin o " \
           f"INNER JOIN arrival a ON a.EVENTID = o.EVENTID " \
           f"WHERE" \
           f" (o.COMMENTS LIKE '%{params.comment}%')" \
           f" AND" \
           f" (FROM_UNIXTIME(o.ORIGINTIME) BETWEEN '{params.from_dt}' AND " \
           f"                                       '{params.to_dt}')" \
           f" AND (a.STA LIKE '%{sta}%')" \
           f" ORDER BY o.ORIGINTIME"


def get_data(params: QueryParams) -> List[tuple]:
    """Returns data of quakes from DB"""
    sql = get_sql_query(params)
    try:
        with connect(**config.DB, connection_timeout=2) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
    except Error as exc:
        raise ConnectDatabaseError(exc.msg)


def get_quakes(params: QueryParams) -> Tuple[Quake, ...]:
    """Return tuple of Quake data structures from db records"""
    quakes = []
    _id, origin_dt, lat, lon, depth, reg =\
        '', datetime(year=1, month=1, day=1), 0.0, 0.0, 0.0, ''
    stations: Set[Sta] = set()
    quake_records = get_data(params)
    for quake_record in quake_records:
        if quake_record[0] != _id:
            if len(stations) != 0:
                quakes.append(
                    Quake(_id, origin_dt, lat, lon, depth, reg,
                          tuple(stations)))
                stations.clear()
            _id, origin_dt, lat, lon, depth, reg = quake_record[:6]
        stations.add(Sta(*quake_record[6:]))
    quakes.append(Quake(_id, origin_dt, lat, lon, depth, reg, tuple(stations)))
    return tuple(quakes)
