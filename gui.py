# -*- coding: utf-8 -*-
from pathlib import Path
from PySide6.QtWidgets import (QDialog, QMainWindow, QMessageBox,
                               QFileDialog, QTableWidgetItem)
from ui.main_window_ui import Ui_MainWindow
from ui.db_conn_ui import Ui_Dialog
import config
from quakes_data_from_db import get_data


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._connect_signals_slots()
        self.file_for_save = None
        self.file_for_open = None
        self.file_filter = ';;'.join(config.FILES_FILTERS.values())

    def _connect_signals_slots(self) -> None:
        self.action_Save_as.triggered.connect(self.save_file)
        self.actionOpen_Bulletin.triggered.connect(self.open_bulletin)
        self.actionConnection.triggered.connect(self._show_connection_dialog)
        self.actionAbout.triggered.connect(self.about)
        self.search_events_button.clicked.connect(self.get_events)

    def _show_connection_dialog(self) -> None:
        conn_dialog = ConnectionDialog(self)
        conn_dialog.exec()

    def get_events(self):
        # TODO obtain list of Events()
        data_lst = get_data()
        self._set_data_into_table(data_lst)

    def _set_data_into_table(self, data_lst: list[tuple]) -> None:
        for data_tuple in data_lst:
            column_num = 0
            for data in data_tuple:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(
                    row, column_num, QTableWidgetItem(f'{data}'))
                column_num += 1

    def save_file(self) -> None:
        # TODO save function depending on ext of file 
        self.file_for_save = \
            QFileDialog(self).getSaveFileName(filter=self.file_filter)[0]

    def open_bulletin(self) -> None:
        # TODO
        """All events are loaded from the bulletin file into the list of Event()
        and displayed in the table of the main window."""

        filedialog = QFileDialog(self)
        self.file_for_open, slctd_filter = filedialog.getOpenFileName(
            caption='Open Bulletin', filter=config.FILES_FILTERS['Text'])

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

