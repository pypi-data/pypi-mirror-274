"""
Provides DB functions
"""

import errno
import os
import logging
import sqlite3
from sqlite3 import Cursor
from ._utils import file_exists


class DB():
    """
    Provides SQLite database functions for MusicFinderMicro
    """

    cursor: Cursor

    def _debug(self, message):
        logging.debug(message)

    def __init__(self, file_name: str) -> None:
        if not file_exists(file_name):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), file_name)
        self.connect(file_name)

    def connect(self, file_name: str):
        """Sets up the required SQLite db
        :param file_name: path and file name of db file
        :returns: The SQLite cursor relating to the DB
        """
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        self.cursor = cur

    def get_all_album_groups(self) -> list:
        self.cursor.execute(
            "SELECT mb_release_group_id, title FROM album_group")
        ret_val = self.cursor.fetchall()
        # logging.debug(ret_val)
        return [] if ret_val is None else ret_val

    def db_commit(self) -> None:
        """Commits all outstanding statements"""
        self.cursor.connection.commit()

    def db_close(self) -> None:
        """Closes the connection"""
        self.cursor.connection.commit()
