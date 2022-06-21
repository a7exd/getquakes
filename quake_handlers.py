# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Sequence
from quake_structures import Quake, QuakesStorage


def save_quakes(quakes: Sequence[Quake], storage: QuakesStorage) -> None:
    """Save quakes in the storage"""
    storage.save(quakes)


def format_common_attrs(quake: Quake) -> tuple[str, str, str, str, str, str]:
    origin_dt = datetime.strftime(quake.origin_dt, '%d.%m.%Y %H:%M:%S.%f')[:-3]
    lat = f'{quake.lat:.2f}' if quake.lat else '-'
    lon = f'{quake.lon:.2f}' if quake.lon else '-'
    mag = quake.get_magnitude()
    avg_ml = f'{mag.ML:.1f}' if mag.ML else '-'
    avg_mpsp = f'{mag.MPSP:.1f}' if mag.MPSP else '-'
    depth = f'{quake.depth:.2f}' if quake.depth else '-'
    return origin_dt, lat, lon, avg_ml, avg_mpsp, depth


def format_to_str(columns_data: Sequence, hdr_type_config: Sequence) -> str:
    """Return formatted string accordingly layout of hdr_type_config"""
    if len(columns_data) != len(hdr_type_config):
        raise IndexError('_format_to_str(): len(columns_data) is'
                         ' not equal len(hdr_type_config)')
    res = ''
    for i in range(len(hdr_type_config)):
        res += f'{columns_data[i]:<{hdr_type_config[i]}}'
    return res
