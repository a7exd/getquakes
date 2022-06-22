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
    """Contain average values of magnitude: ML, MPSP"""
    ML: float
    MPSP: float


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
        ml = n_ml = mpsp = n_mpsp = 0
        avg_ml = avg_mpsp = None
        for sta in self.stations:
            if sta.mag_ML:
                ml += sta.mag_ML
                n_ml += 1
            if sta.mag_MPSP:
                mpsp += sta.mag_MPSP
                n_mpsp += 1
        if n_ml != 0:
            avg_ml = round(ml / n_ml, 1)
        if n_mpsp != 0:
            avg_mpsp = round(mpsp / n_mpsp, 1)
        return Magnitude(avg_ml, avg_mpsp)
