# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
from typing import Sequence, Tuple

import openpyxl
from openpyxl.styles import Alignment

import config
from quake_structures import Quake, Catalog, Bulletin


def get_catalog(quake: Quake) -> Catalog:
    origin_dt, lat, lon, avg_ML, avg_MPSP, depth = format_common_attrs(quake)
    origin_d, origin_t = origin_dt.split()
    stations_name = ', '.join(quake.get_stations_name())
    return Catalog(origin_d, origin_t, lat, lon, depth, quake.reg,
                   avg_ML, avg_MPSP, stations_name)


def format_common_attrs(quake: Quake) -> tuple[str, str, str, str, str, str]:
    origin_dt = datetime.strftime(quake.origin_dt, '%d.%m.%Y %H:%M:%S.%f')
    lat = f'{quake.lat:.2f}' if quake.lat else '-'
    lon = f'{quake.lon:.2f}' if quake.lon else '-'
    mag = quake.get_magnitude()
    avg_ML = f'{mag.ML:.1f}' if mag.ML else '-'
    avg_MPSP = f'{mag.MPSP:.1f}' if mag.MPSP else '-'
    depth = f'{quake.depth:.2f}' if quake.depth else '-'
    return origin_dt, lat, lon, avg_ML, avg_MPSP, depth


def write_catalog(quakes: tuple[Quake], catalog_path: str = None,
                  amnt_processed: int = 0) -> None:
    if not Path(catalog_path).exists():
        raise FileExistsError(f'{catalog_path} does not exist!')
    wb = openpyxl.load_workbook(catalog_path)
    num_of_month = quakes[amnt_processed].origin_dt.month - 1
    sheet = wb.create_sheet(config.MONTHS[num_of_month], num_of_month)
    sheet.append(config.CATALOG_HEADER)

    for quake in quakes:
        if quake.origin_dt.month - 1 > num_of_month:
            write_catalog(quakes[amnt_processed:], catalog_path, amnt_processed)
        catalog = get_catalog(quake)
        if (catalog.lat != '-') and (catalog.lon != '-'):
            sheet.append(get_catalog(quake))
        columns = sheet.column_dimensions['A':'I']
        columns.alignment = Alignment(horizontal='center', vertical='center')
        amnt_processed += 1
    wb.save(catalog_path)


def get_bulletin(quake: Quake) -> Bulletin:
    quake_hdr_describe = get_quake_hdr_describe(quake)
    quake_hdr = get_quake_hdr(quake) + '\n'
    station_hdr_describe = \
        format_to_bul(config.STATION_HEADER_DESCRIBE,
                      config.AMNT_COLUMN_SYMBOLS['sta_hdr'])
    station_strings = get_stations_string(quake)
    return Bulletin(quake.id, quake_hdr_describe, quake_hdr,
                    station_hdr_describe, station_strings)


def get_quake_hdr_describe(quake: Quake) -> str:
    mag = quake.get_magnitude()
    mag_type = 'ML' if mag.ML else 'MPSP' if mag.MPSP else 'Mag'
    config.QUAKE_HEADER_DESCRIBE.insert(5, mag_type)
    return format_to_bul(config.QUAKE_HEADER_DESCRIBE,
                         config.AMNT_COLUMN_SYMBOLS['quake_hdr'])


def get_quake_hdr(quake: Quake) -> str:
    origin_dt, lat, lon, avg_ML, avg_MPSP, depth = format_common_attrs(quake)
    mag = avg_ML if avg_ML != '-' else avg_MPSP
    amnt_sta = str(len(quake.get_stations_name()))
    return format_to_bul(
        columns_data=(origin_dt, lat, lon, depth, amnt_sta, mag, quake.reg),
        hdr_type_config=config.AMNT_COLUMN_SYMBOLS['quake_hdr'])


def get_stations_string(quake: Quake) -> str:
    res = ''
    for sta in quake.stations:
        mag = sta.mag_ML if sta.mag_ML else \
              sta.mag_MPSP if sta.mag_MPSP else '-'
        mag_type = 'ML' if sta.mag_ML else 'MPSP' if sta.mag_MPSP else '-'
        sta_data = (sta.name, sta.dist, sta.azimuth, sta.phase, sta.entry,
                    sta.phase_dt, sta.ampl, sta.period, mag, mag_type)
        res += format_to_bul(sta_data,
                             config.AMNT_COLUMN_SYMBOLS['sta_hdr']) + '\n'
    return res + '\n'


def format_to_bul(columns_data: Sequence[str], hdr_type_config: tuple) -> str:
    """Return formatted string accordingly layout of bulletin"""
    res = ''
    for i in range(len(hdr_type_config)):
        res += f'{columns_data[i]:<{hdr_type_config[i]}}'
    return res


def write_bulletin(quakes: tuple[Quake], bulletin_path: str) -> None:
    if not Path(bulletin_path).exists():
        raise FileExistsError(f'{bulletin_path} does not exist!')
    with Path(bulletin_path).open('w', encoding='utf8') as file:
        for quake in quakes:
            file.write('\n'.join(get_bulletin(quake)))
        file.write(f'\nTotal: {len(quakes)}')

