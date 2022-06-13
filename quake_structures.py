# -*- coding: utf-8 -*-
import decimal
from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple


@dataclass(slots=True)
class Sta:
    name: str
    dist: float
    azimuth: float
    phase: str
    entry: str
    phase_dt: datetime
    ampl: decimal
    period: float
    mag_ML: float
    mag_MPSP: float


class Magnitude(NamedTuple):
    ML: float | None
    MPSP: float | None
    preferred: float | None


@dataclass(slots=True)
class Quake:
    id: str
    origin_dt: datetime
    lat: float
    lon: float
    depth: float
    reg: str
    stations: list[Sta]

    def get_stations_name(self) -> set[Sta.name]:
        stations_name = set()
        for sta in self.stations:
            stations_name.add(sta.name)
        return stations_name

    def get_magnitude(self) -> Magnitude:
        ML = n_ML = MPSP = n_MPSP = 0
        avg_ML = avg_MPSP = None
        for sta in self.stations:
            if sta.mag_ML:
                ML += sta.mag_ML
                n_ML += 1
            if sta.mag_MPSP:
                MPSP += sta.mag_MPSP
                n_MPSP += 1
        if n_ML != 0:
            avg_ML = round(ML / n_ML, 1)
        if n_MPSP != 0:
            avg_MPSP = round(MPSP / n_MPSP, 1)
        preferred = avg_ML if avg_ML else avg_MPSP
        return Magnitude(avg_ML, avg_MPSP, preferred)


class Catalog(NamedTuple):
    origin_d: str
    origin_t: str
    lat: str
    lon: str
    depth: str
    reg: str
    mag: str
    stations_name: str
    avg_mag_ML: str
    avg_mag_MPSP: str


StaString = str(Sta)


class Bulletin(NamedTuple):
    quake_id: str
    quake_header_describe: str
    quake_header: str
    station_header_describe: str
    station_strings: list[StaString]
