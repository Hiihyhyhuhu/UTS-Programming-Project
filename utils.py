"""
Small utility functions: id generation, safe CSV parsing,
datetime helpers, manual comma parsing and append.
"""
import os
import datetime
from typing import List

def genID(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    last_line = lines[-1]
    last_id = last_line.split(",")[0]
    digit = last_id[0]
    new_id = int(last_id[1:]) + 1
    return f"{digit}{new_id:06d}"

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def parse_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_time(time_str: str) -> datetime.time:
    # Accept HH:MM or HH:MM:SS
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 2:
        h, m = parts
        s = 0
    else:
        h, m, s = parts
    return datetime.time(h, m, s)

DATA_DIR = "data"
ensure_dir(DATA_DIR)

def path_for(table: str) -> str:
    return os.path.join(DATA_DIR, f"{table}.csv")

def read_table(table: str) -> List[List[str]]:
    """Return list of rows (including header) - each row is list of strings."""
    p = path_for(table)
    if not os.path.exists(p):
        return []
    rows = []
    with open(p, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if line == '':
                continue
            # naive split by comma (no quote handling) as requested
            rows.append(line.split(','))
    return rows

def write_table(table: str, rows: List[List[str]]):
    p = path_for(table)
    with open(p, 'w') as f:
        for r in rows:
            f.write(','.join(map(str, r)) + '\n')

def append_row(table: str, row: List[str]):
    p = path_for(table)
    with open(p, 'a') as f:
        f.write(','.join(map(str, row)) + '\n')

# Convenience: ensure tables exist with header
DEFAULT_SCHEMAS = {
    'theater': ['idTheater', 'name', 'address', 'brand'],
    'hall': ['idHall', 'idTheater', 'name', 'rows', 'cols'],
    'film': ['idFilm', 'name', 'genre', 'duration', 'age', 'director', 'actor'],
    'session': ['idSession', 'idHall', 'idFilm', 'date', 'time', 'price'],
    'user': ['idUser', 'idTheater', 'name', 'password', 'role'],
    'booking': ['idBooking', 'idSession', 'idUser', 'row', 'col', 'price', 'timestamp'],
}

def ensure_tables():
    for t, header in DEFAULT_SCHEMAS.items():
        p = path_for(t)
        if not os.path.exists(p):
            with open(p, 'w') as f:
                f.write(','.join(header) + '\n')
