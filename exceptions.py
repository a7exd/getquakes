# -*- coding: utf-8 -*-

class NoSelectedQuakesError(Exception):
    """Any quakes were not selected"""


class ConnectDatabaseError(Exception):
    """Program can't connect to the Database"""


class FormatToStrError(Exception):
    """Program can't format sequence to string"""
