# -*- coding: utf-8 -*-
from typing import Tuple, List, NamedTuple
from mysql.connector import connect, Error  # type: ignore
import config
from exceptions import ConnectDatabaseError
from quake_structures import Quake, Sta
from datetime import datetime


class QueryParams(NamedTuple):
    from_dt: str
    to_dt: str
    sta: str
    from_mag: str
    to_mag: str
    comment: str


def _get_sql_query(params: QueryParams) -> str:
    sta = '' if params.sta.lower() == 'all' else params.sta
    from_dt = datetime.strptime(params.from_dt, '%Y-%m-%d %H:%M:%S').timestamp()
    to_dt = datetime.strptime(params.to_dt, '%Y-%m-%d %H:%M:%S').timestamp()
    key_words = params.comment.split()
    key_words_count = len(key_words)
    if key_words_count > 1:
        comment_query = "%' OR o.COMMENTS LIKE '%".join(key_words)
    elif key_words_count == 1:
        comment_query = key_words[0]
    else:
        comment_query = ""
    return f"SELECT" \
           f" o.EVENTID, o.ORIGINTIME, o.LAT, o.LON," \
           f" o.`DEPTH`," \
           f" CONCAT(SUBSTR(o.COMMENTS, 1, INSTR(o.COMMENTS, '.') - 3),"\
           f"        SUBSTR(o.COMMENTS, 20))," \
           f" a.ITIME, a.STA, ROUND(a.DIST, 3)," \
           f" ROUND(a.AZIMUTH, 3), a.IPHASE, CONCAT(a.IM_EM, a.FM)," \
           f" ROUND(a.AMPL, 4), ROUND(a.PER, 3)," \
           f" a.ML, a.MPSP " \
           f"FROM origin o " \
           f"INNER JOIN arrival a ON a.EVENTID = o.EVENTID " \
           f"WHERE" \
           f" (o.COMMENTS LIKE '%{comment_query}%')" \
           f" AND" \
           f" (o.ORIGINTIME BETWEEN '{from_dt}' AND " \
           f"                                       '{to_dt}')" \
           f" AND (a.STA LIKE '%{sta}%')" \
           f" ORDER BY a.ITIME"


def get_data(params: QueryParams) -> List[tuple]:
    """Returns data of quakes from DB"""
    sql = _get_sql_query(params)
    try:
        with connect(**config.DB, connection_timeout=2) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
    except Error as exc:
        raise ConnectDatabaseError(exc.msg)


def get_quakes(params: QueryParams) -> Tuple[Quake, ...]:
    """Return tuple of Quake from db records"""
    quakes = []
    stations: List[Sta] = []
    origin_dt = datetime(year=1, month=1, day=1)
    _id, origin_dtime, lat, lon, depth, reg = \
        '', 0.0, 0.0, 0.0, 0.0, ''
    quake_records = get_data(params)
    prev_sta = None
    for quake_record in quake_records:
        if quake_record[0] != _id:
            if len(stations) != 0:
                stations = sorted(stations, key=sort_stations)
                quake = Quake(_id, origin_dt, lat,
                              lon, depth, reg, tuple(stations))
                quakes.append(quake)
                stations.clear()
                prev_sta = None
            _id, origin_dtime, lat, lon, depth, reg = quake_record[:6]
            origin_dt = datetime.utcfromtimestamp(origin_dtime)

        sta_dt = datetime.utcfromtimestamp(quake_record[6])
        sta = Sta(sta_dt, *quake_record[7:])
        prev_sta = _add_sta(sta, stations, prev_sta)
    stations = sorted(stations, key=sort_stations)
    quakes.append(Quake(_id, origin_dt, lat, lon,
                        depth, reg, tuple(stations)))
    return tuple(_filter_magnitude(quakes, params))


def _add_sta(sta: Sta, stations: List[Sta], prev_sta: Sta | None):
    if sta.name in config.STA_RENAME:
        sta.name += 'R'
    if prev_sta is not None and sta.name == prev_sta.name \
            and sta.dist is not None:
        prev_sta.dist = sta.dist
    if prev_sta is None or (sta.phase_dt != prev_sta.phase_dt) \
            or (sta.name != prev_sta.name):
        stations.append(sta)
        out_sta = sta
    else:
        if sta.dist is not None:
            prev_sta.dist = sta.dist
        if sta.azimuth is not None:
            prev_sta.azimuth = sta.azimuth
        if sta.ampl is not None:
            prev_sta.ampl = sta.ampl
        if sta.period is not None:
            prev_sta.period = sta.period
        if sta.mag_ML is not None:
            prev_sta.mag_ML = sta.mag_ML
        if sta.mag_MPSP is not None:
            prev_sta.mag_MPSP = sta.mag_MPSP
        out_sta = prev_sta
    return out_sta


def sort_stations(sta: Sta) -> float:
    return sta.dist if sta.dist else 0.0


def _filter_magnitude(quakes: List[Quake], params: QueryParams) -> List[Quake]:
    from_mag, to_mag = float(params.from_mag), float(params.to_mag)
    return [quake for quake in quakes
            if (from_mag <= quake.magnitude.ML <= to_mag)
            or (from_mag <= quake.magnitude.MPSP <= to_mag)]
