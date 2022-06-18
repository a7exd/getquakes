# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
from typing import Sequence

import openpyxl
from openpyxl.styles import Alignment

import config
from quake_structures import Quake, Catalog, Bulletin


def get_catalog(quake: Quake) -> Catalog:
    origin_dt, lat, lon, avg_ml, avg_mpsp, depth = _format_common_attrs(quake)
    origin_d, origin_t = origin_dt.split()
    stations_name = ', '.join(quake.get_stations_name())
    return Catalog(origin_d, origin_t, lat, lon, depth, quake.reg,
                   avg_ml, avg_mpsp, stations_name)


def _format_common_attrs(quake: Quake) -> tuple[str, str, str, str, str, str]:
    origin_dt = datetime.strftime(quake.origin_dt, '%d.%m.%Y %H:%M:%S.%f')[:-3]
    lat = f'{quake.lat:.2f}' if quake.lat else '-'
    lon = f'{quake.lon:.2f}' if quake.lon else '-'
    mag = quake.get_magnitude()
    avg_ml = f'{mag.ML:.1f}' if mag.ML else '-'
    avg_mpsp = f'{mag.MPSP:.1f}' if mag.MPSP else '-'
    depth = f'{quake.depth:.2f}' if quake.depth else '-'
    return origin_dt, lat, lon, avg_ml, avg_mpsp, depth


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
    quake_hdr_describe = _get_quake_hdr_describe(quake)
    quake_hdr = _get_quake_hdr(quake) + '\n'
    station_hdr_describe = \
        _format_to_bul(config.STATION_HEADER_DESCRIBE,
                       config.AMNT_COLUMN_SYMBOLS['sta_hdr'])
    station_strings = _get_stations_string(quake)
    return Bulletin(quake.id, quake_hdr_describe, quake_hdr,
                    station_hdr_describe, station_strings)


def _get_quake_hdr_describe(quake: Quake) -> str:
    mag = quake.get_magnitude()
    mag_type = 'ML' if mag.ML else 'MPSP' if mag.MPSP else 'Mag'
    config.QUAKE_HEADER_DESCRIBE.insert(5, mag_type)
    return _format_to_bul(config.QUAKE_HEADER_DESCRIBE,
                          config.AMNT_COLUMN_SYMBOLS['quake_hdr'])


def _get_quake_hdr(quake: Quake) -> str:
    origin_dt, lat, lon, avg_ml, avg_mpsp, depth = _format_common_attrs(quake)
    mag = avg_ml if avg_ml != '-' else avg_mpsp
    amnt_sta = str(len(quake.get_stations_name()))
    return _format_to_bul(
        columns_data=(origin_dt, lat, lon, depth, amnt_sta, mag, quake.reg),
        hdr_type_config=config.AMNT_COLUMN_SYMBOLS['quake_hdr'])


def _get_stations_string(quake: Quake) -> str:
    res = ''
    for sta in quake.stations:
        mag = sta.mag_ML if sta.mag_ML else \
              sta.mag_MPSP if sta.mag_MPSP else '-'
        mag_type = 'ML' if sta.mag_ML else 'MPSP' if sta.mag_MPSP else '-'
        sta_data = (sta.name, sta.dist, sta.azimuth, sta.phase, sta.entry,
                    sta.phase_dt, sta.ampl, sta.period, mag, mag_type)
        res += _format_to_bul(sta_data,
                              config.AMNT_COLUMN_SYMBOLS['sta_hdr']) + '\n'
    return res + '\n'


def _format_to_bul(columns_data: Sequence[str], hdr_type_config: tuple) -> str:
    """Return formatted string accordingly layout of bulletin"""
    res = ''
    for i in range(len(hdr_type_config)):
        res += f'{columns_data[i]:<{hdr_type_config[i]}}'
    return res


def write_bulletin(quakes: tuple[Quake], f_name: str) -> None:
    f_name = f'{f_name}.txt'
    with Path(f_name).open('w', encoding='utf8') as file:
        for quake in quakes:
            file.write('\n'.join(get_bulletin(quake)))
        file.write(f'\nTotal: {len(quakes)}')


def _get_nas_bltn(quake: Quake) -> list[str]:
    dt = datetime.strftime(quake.origin_dt, '%Y %m %d %H %M %S.%f')[:-3]
    header = f'Fi={quake.lat:.2f}  LD={quake.lon:.2f} T0={dt}'
    bltn_strings = [header]
    for sta in quake.stations:
        phase_dt = datetime.strftime(sta.phase_dt,
                                     '%Y %m %d   %H %M %S.%f')[:-3]
        bltn_strings.append(f'{sta.name}    {sta.phase}={phase_dt}')
    return bltn_strings


def write_nas_bltn(quakes: tuple[Quake], path: str) -> None:
    for quake in quakes:
        nas_bltn = _get_nas_bltn(quake)
        f_name = datetime.strftime(quake.origin_dt, '%Y%m%d_%H%M%S')
        full_path = Path.joinpath(path, f_name, '.bltn')
        with Path(full_path).open('w', encoding='utf8') as file:
            file.write('\n'.join(nas_bltn))


def write_arcgis(quakes: tuple[Quake], f_name: str) -> None:
    f_name = Path.joinpath(f_name, '_ArcGis.txt')
    with Path(f_name).open('w', encoding='utf8') as file:
        file.write(' '.join(config.ArcGIS_HEADER) + '\n')
        for quake in quakes:
            columns = _get_columns_arcgis(quake)
            file.write(' '.join(columns))


def _get_columns_arcgis(quake: Quake) -> tuple[str, str, str, str, str, str]:
    origin_dt, lat, lon, avg_ml, avg_mpsp, _ = _format_common_attrs(quake)
    mag = avg_ml if avg_ml != '-' else avg_mpsp
    columns = origin_dt, lat, lon, '0.0', '1', '\n'
    if mag != '-':
        for _range in config.MAGNITUDE_RANGES:
            if _range[0] < float(mag) < _range[1]:
                columns = origin_dt, lat, lon, mag,\
                          config.MAGNITUDE_RANGES[_range], '\n'
    return columns
