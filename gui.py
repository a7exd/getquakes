# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Generator

from PySide6.QtWidgets import (QDialog, QMainWindow, QMessageBox,
                               QFileDialog, QTableWidgetItem)

from exceptions import NoSelectedQuakesError, ConnectDatabaseError
from quake_storages import save_quakes,  storages
from quake_structures import Quake
from ui.main_window_ui import Ui_MainWindow
from ui.db_conn_ui import Ui_Dialog
import config
from quakes_from_db import get_data, get_quakes


class Window(QMainWindow, Ui_MainWindow):
    """Main window of application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()
        self.file_filter = ';;'.join(config.FILES_FILTERS.values())
        self.raw_quakes_data = None

    def _connect_signals_slots(self) -> None:
        self.save_as_button.clicked.connect(self.save_file)
        self.actionBulletin.triggered.connect(self.save_file)
        self.actionCatalog.triggered.connect(self.save_file)
        self.action_NAS_bulletin.triggered.connect(self.save_file)
        self.action_ArcGIS.triggered.connect(self.save_file)
        self.actionConnection.triggered.connect(self._show_connection_dialog)
        self.actionAbout.triggered.connect(self.about)
        self.search_events_button.clicked.connect(self.search_quakes)

    def _show_connection_dialog(self) -> None:
        conn_dialog = ConnectionDialog(self)
        conn_dialog.exec()

    def get_selected_quakes(self) -> tuple[Quake]:
        """Obtain tuple of Quake() according to selected quakes
        from the table of GUI"""
        try:
            selected_data = self._get_selected_data()
            return get_quakes(selected_data)
        except NoSelectedQuakesError:
            print('Nothing was selected!')
            # TODO print into log, show DialogWindow

    def search_quakes(self) -> None:
        try:
            self.raw_quakes_data = get_data(self._get_query_params())
            self._set_data_into_table()
        except ConnectDatabaseError as exc:
            print(exc.args[0])  # TODO print into log, show DialogWindow

    def _set_data_into_table(self) -> None:
        self.tableWidget.setRowCount(0)
        for quake_data in self.raw_quakes_data:
            params_dict = {config.ALL_PARAMS[i]: quake_data[i]
                           for i in range(len(quake_data))}
            column_num = 0
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for param in config.GUI_TABLE_PARAMS:
                self.tableWidget.setItem(
                    row, column_num, QTableWidgetItem(f'{params_dict[param]}'))
                column_num += 1

    def _get_selected_data(self) -> Generator:
        selected_id = self._get_selected_quakes_id()
        return (data for data in self.raw_quakes_data
                for _id in selected_id if data[0] == _id)

    def _get_selected_quakes_id(self) -> list[str]:
        selected_items_amnt = len(self.tableWidget.selectedItems())
        if selected_items_amnt == 0:
            raise NoSelectedQuakesError
        return [self.tableWidget.selectedItems()[i].text()
                for i in range(selected_items_amnt)
                if i % self.tableWidget.columnCount() == 0]

    def _get_query_params(self) -> tuple[str, ...]:
        from_dt = self.from_dateTime.text()
        to_dt = self.to_dateTime.text()
        comment = self.comment_line.text()
        sta = self.sta_line.text()
        from_mag = f'{self.from_Mag.value()}'
        to_mag = f'{self.to_Mag.value()}'
        return from_dt, to_dt, comment, sta, from_mag, to_mag

    def save_file(self) -> None:
        """Save function depending on ext of file."""
        dialog = QFileDialog(self)
        file = dialog.getSaveFileName(dir='untitled.txt',
                                      filter=self.file_filter)[0]
        file = Path(file)
        ext = file.suffix
        quakes = self.get_selected_quakes()
        save_quakes(quakes, storages[ext](file))

    def about(self) -> None:
        QMessageBox.about(
            self,
            'About getquakes ',
            '<p>Desktop application for obtaining a list of earthquakes from '
            'a database and then saving it as a bulletin or a file of another '
            'structure.</p>'
            '<p>The app built with:</p>'
            '<p>- Qt Designer</p>'
            '<p>- PySide6</p>'
            '<p>- Python</p>'
            '<p>Author: Alexey Danilov, a7exdanilov@gmail.com</p>',
        )


class ConnectionDialog(QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()
        self.host_line.setText(config.DB['host'])
        self.port_line.setText(config.DB['port'])
        self.db_name_line.setText(config.DB['database'])
        self.user_line.setText(config.DB['user'])
        self.password_line.setText(config.DB['password'])

    def _connect_signals_slots(self) -> None:
        self.buttonBox.accepted.connect(self.set_db_conn_config)

    def set_db_conn_config(self) -> None:
        content_lst = Path('config.py').open('r', encoding='utf8').readlines() 
        db_conf = (('host', self.host_line.text()),
                   ('port', self.port_line.text()),
                   ('database', self.db_name_line.text()),
                   ('user', self.user_line.text()),
                   ('password', self.password_line.text()))

        with Path('config.py').open('w', encoding='utf8') as config_file:
            config_file.writelines(content_lst[:3])
            config_file.write(f'DB = {dict(db_conf)}\n')
            config_file.writelines(content_lst[4:])
        self.close()
