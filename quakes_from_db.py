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
    from_dt = datetime.strptime(params.from_dt + '+0000', '%Y-%m-%d %H:%M:%S%z')
    from_dt_timestamp = from_dt.timestamp()
    to_dt = datetime.strptime(params.to_dt + '+0000', '%Y-%m-%d %H:%M:%S%z')
    to_dt_timestamp = to_dt.timestamp()
    key_words = params.comment.split()
    key_words_count = len(key_words)
    if key_words_count > 1:
        comment_query = "%' OR o.COMMENTS LIKE '%".join(key_words)
    elif key_words_count == 1:
        comment_query = key_words[0]
    else:
        comment_query = ""
    return f"SELECT" \
           f" o.EVENTID, o.ORIGINTIME, ROUND(o.LAT, 2), ROUND(o.LON, 2)," \
           f" o.`DEPTH`," \
           f" CONCAT(SUBSTR(o.COMMENTS, 1, INSTR(o.COMMENTS, '.') - 3),"\
           f"        SUBSTR(o.COMMENTS, INSTR(o.COMMENTS, ':') + 4))," \
           f" a.ITIME, a.STA, ROUND(a.DIST, 2)," \
           f" ROUND(a.AZIMUTH, 2), a.IPHASE, CONCAT(a.IM_EM, a.FM)," \
           f" ROUND(a.AMPL, 4), ROUND(a.PER, 2)," \
           f" ROUND(a.ML, 1), ROUND(a.MPSP, 1) " \
           f"FROM origin o " \
           f"INNER JOIN arrival a ON a.EVENTID = o.EVENTID " \
           f"WHERE" \
           f" (o.COMMENTS LIKE '%{comment_query}%')" \
           f" AND" \
           f" (a.ITIME BETWEEN '{from_dt_timestamp}' AND " \
           f"                                       '{to_dt_timestamp}')" \
           f" ORDER BY o.EVENTID"


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
    for quake_record in quake_records:
        if quake_record[0] != _id:
            if len(stations) != 0:
                stations = _filter_stations(stations)
                quake = Quake(_id, origin_dt, lat,
                              lon, depth, reg, tuple(stations))
                quakes.append(quake)
                stations.clear()
            _id, origin_dtime, lat, lon, depth, reg = quake_record[:6]
            origin_dt = datetime.utcfromtimestamp(origin_dtime) \
                if origin_dtime is not None else datetime.min

        sta_dt = datetime.utcfromtimestamp(quake_record[6])
        sta = Sta(sta_dt, *quake_record[7:])
        stations.append(sta)
    stations = _filter_stations(stations)
    quakes.append(Quake(_id, origin_dt, lat, lon,
                        depth, reg, tuple(stations)))
    return tuple(_filter_quakes(quakes, params))


def _add_sta(sta: Sta, stations: List[Sta], prev_sta: Sta | None) -> Sta:
    if sta.name in config.STA_RENAME:
        sta.name += 'R'
    if prev_sta is not None and sta.name == prev_sta.name:
        if sta.dist is not None:
            prev_sta.dist = sta.dist
        else:
            sta.dist = prev_sta.dist
    if prev_sta is None or (sta.phase_dt != prev_sta.phase_dt) \
            or (sta.name != prev_sta.name):
        stations.append(sta)
        out_sta = sta
    else:
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


def _filter_stations(stations: List[Sta]) -> List[Sta]:
    sorted_by_time = sorted(stations, key=lambda x: x.phase_dt)
    sorted_by_name = sorted(sorted_by_time, key=lambda x: x.name)
    res: List[Sta] = []
    prev_sta: Sta | None = None
    for sta in sorted_by_name:
        prev_sta = _add_sta(sta, res, prev_sta)
    sorted_by_dist = sorted(res,
                            key=lambda x: x.dist if x.dist is not None else 0.0)
    return sorted_by_dist


def _filter_quakes(quakes: List[Quake], params: QueryParams) -> List[Quake]:
    sta_set = set(params.sta.split())
    from_mag, to_mag = float(params.from_mag), float(params.to_mag)
    res: List[Quake] = []
    for quake in quakes:
        mag_ml, mag_mpsp = quake.magnitude
        mag = mag_ml if mag_ml != 0.0 else mag_mpsp
        if from_mag <= mag <= to_mag:
            res.append(quake)
    if params.sta.lower() != 'all':
        res = [quake for quake in res
               if sta_set.issubset(quake.stations_name)]
    return sorted(res, key=lambda x: x.stations[0].phase_dt)
