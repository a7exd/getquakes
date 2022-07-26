# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Generator, List

from PySide6.QtWidgets import (QDialog, QMainWindow, QMessageBox,
                               QFileDialog, QTableWidgetItem)

from exceptions import NoSelectedQuakesError, ConnectDatabaseError, \
    FormatToStrError
from quake_storages import save_quakes, storages
from ui.main_window_ui import Ui_MainWindow
from ui.db_conn_ui import Ui_Dialog
import config
from quakes_from_db import get_quakes, QueryParams
import logging.config


logging.config.dictConfig(config.LOG_CONFIG)
log = logging.getLogger('gui_logger')


class Window(QMainWindow, Ui_MainWindow):
    """Main window of application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()
        self.file_filter = ';;'.join(config.FILES_FILTERS.values())
        self.quakes = None
        self.statusBar().showMessage('Ready')

    def search_quakes(self) -> None:
        self.progressBar.setValue(5)
        try:
            log.info(f'Start search for records. '
                     f'DB connection config: {config.DB}.')
            query_params = self._get_query_params()
            log.info(f'{query_params}')
            self.quakes = get_quakes(query_params)
            self._set_data_into_table()
            self.statusBar().showMessage(f'Searched quakes: '
                                         f'{self.tableWidget.rowCount()}')
            self.progressBar.setValue(100)
        except ConnectDatabaseError as exc:
            self.statusBar().showMessage('Error: cannot connect to Database!')
            log.exception(exc)
            self._show_error_dialog(message=f'{exc.args[0]}\n\n'
                                            f'Check connection settings '
                                            f'(File->Settings->Connection) '
                                            f'and try again!')

    def get_selected_quakes(self) -> Generator:
        """Obtain tuple of Quake() according to selected quakes
        from the table of GUI"""
        selected_id = self._get_selected_quakes_id()
        return (quake for quake in self.quakes
                if quake.id in selected_id)

    def save_file(self) -> None:
        """Save function depending on ext of file."""
        self.progressBar.setValue(10)
        dialog = QFileDialog(self)
        file = dialog.getSaveFileName(self, dir='untitled.txt',
                                      filter=self.file_filter)[0]
        if not file:
            return self._show_error_dialog('File is not selected! '
                                           'Select a file and try again, '
                                           'please.')
        file = Path(file)
        log.info(f'file to save the quakes: {file}')
        ext = file.suffix
        try:
            quakes = self.get_selected_quakes()
            save_quakes(quakes, storages[ext](file))
            self.statusBar().showMessage('Writing into the file '
                                         'completed successfully.')
            log.info(f'Writing into the file completed successfully.')
            self.progressBar.setValue(100)
        except (NoSelectedQuakesError, FormatToStrError,
                PermissionError) as exc:
            self.statusBar().showMessage('Error: cannot save the data!')
            log.exception(exc)
            self._show_error_dialog(message=f'Cannot save the data '
                                            f'into the file "{file}"!\n'
                                            f'\n{exc.args}')

    def _show_error_dialog(self, message) -> None:
        title = 'Something went wrong'
        QMessageBox.critical(self, title, message,
                             buttons=QMessageBox.Ok,
                             defaultButton=QMessageBox.Ok)

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

    def _set_data_into_table(self) -> None:
        self.tableWidget.setRowCount(0)
        for quake in self.quakes:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            quake_vals = (quake.id, quake.origin_dt, quake.lat, quake.lon,
                          quake.depth, quake.magnitude.ML,
                          quake.magnitude.MPSP, quake.reg)
            for column, val in enumerate(quake_vals):
                self.tableWidget.setItem(
                    row, column, QTableWidgetItem(f'{val}'))
            sta_ph_time = []
            for sta in quake.stations:
                sta_ph_time.append(
                    ' '.join(
                        (sta.name, sta.phase, f'{sta.phase_dt}')) + '\n')
            self.tableWidget.setItem(
                row, 8, QTableWidgetItem('\n'.join(sta_ph_time)))

    def _get_selected_quakes_id(self) -> List[str]:
        selected_items_amnt = len(self.tableWidget.selectedItems())
        log.info(f'selected items amount: {selected_items_amnt}')
        col_count = self.tableWidget.columnCount()
        if selected_items_amnt == 0 or selected_items_amnt % col_count != 0:
            raise NoSelectedQuakesError('Nothing is selected! At least one row'
                                        ' from the table must be selected!')
        log.info(f'selected quakes amount: {selected_items_amnt / col_count}')
        return [self.tableWidget.selectedItems()[i].text()
                for i in range(selected_items_amnt) if i % col_count == 0]

    def _get_query_params(self) -> QueryParams:
        return QueryParams(from_dt=self.from_dateTime.text(),
                           to_dt=self.to_dateTime.text(),
                           comment=self.comment_line.text(),
                           sta=self.sta_line.text(),
                           from_mag=f'{self.from_Mag.value()}',
                           to_mag=f'{self.to_Mag.value()}')

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
        self._init_db_config_gui()

    def _connect_signals_slots(self) -> None:
        self.buttonBox.accepted.connect(self.set_db_conn_config)

    def _init_db_config_gui(self) -> None:
        self.host_line.setText(config.DB['host'])
        self.port_line.setText(config.DB['port'])
        self.db_name_line.setText(config.DB['database'])
        self.user_line.setText(config.DB['user'])
        self.password_line.setText(config.DB['password'])

    def set_db_conn_config(self) -> None:
        content_lst = Path('config.py').open('r', encoding='utf8').readlines()
        db_conf = {'host': self.host_line.text(),
                   'port': self.port_line.text(),
                   'database': self.db_name_line.text(),
                   'user': self.user_line.text(),
                   'password': self.password_line.text()}

        with Path('config.py').open('w', encoding='utf8') as config_file:
            config_file.writelines(content_lst[:3])
            config_file.write(f'DB = {db_conf}\n')
            config_file.writelines(content_lst[4:])
        self.close()
        config.DB = db_conf
        log.info(f'db connection config is changed to {db_conf}')
