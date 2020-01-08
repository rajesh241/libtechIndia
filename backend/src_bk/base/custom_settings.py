"""This module has custom settings for Libtech Django backend"""
from pathlib import Path
HOMEDIR = str(Path.home())
SQL_CONFIG = f"{HOMEDIR}/.libtech/libtech_backend_mysql.cnf"
