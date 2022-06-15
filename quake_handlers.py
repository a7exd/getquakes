# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment

import config
from quake_structures import Quake, Catalog, Bulletin


def get_catalog(quake: Quake) -> Catalog:
    origin_d, origin_t = datetime.strftime(
        quake.origin_dt, '%d.%m.%Y %H:%M:%S.%f').split()
    lat = f'{quake.lat:.2f}' if quake.lat else '-'
    lon = f'{quake.lon:.2f}' if quake.lon else '-'
    mag = quake.get_magnitude()
    avg_ML = mag.ML if mag.ML else '-'
    avg_MPSP = mag.MPSP if mag.MPSP else '-'
    depth = f'{quake.depth:.2f}' if quake.depth else '-'
    reg = quake.reg
    stations_name = ', '.join(quake.get_stations_name())
    return Catalog(origin_d, origin_t, lat, lon, depth, reg,
                   avg_ML, avg_MPSP, stations_name)


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
    quake_hdr = get_quake_hdr(quake)
    station_hdr_describe = format_for_bulletin(config.STATION_HEADER_DESCRIBE,
                                               'sta_hdr')
    station_strings = get_station_strings(quake)
    return Bulletin(quake.id, quake_hdr_describe, quake_hdr,
                    station_hdr_describe, station_strings)


def get_quake_hdr_describe(quake: Quake) -> str:
    mag = quake.get_magnitude()
    mag_type = 'ML' if mag.ML else 'MPSP' if mag.MPSP else 'Mag'
    hdr_describe = config.QUAKE_HEADER_DESCRIBE.insert(5, mag_type)
    return format_for_bulletin(hdr_describe, 'quake_hdr')


def get_quake_hdr(quake: Quake) -> str:
    pass


def get_station_strings(quake: Quake) -> str:
    pass


def format_for_bulletin(string, type_format: str) -> str:
    pass
