"""
Repository layer: load/save records and queries.
This abstracts CSV I/O behind functions and returns model objects.
"""
from typing import List, Optional
from utils import read_table, append_row, write_table, ensure_tables, path_for
from constructor import Theater, Hall, Film, Session, User, Booking

ensure_tables()

# -- Generic loaders --

def _load_objects(table: str, cls, skip_header=True):
    rows = read_table(table)
    if not rows: return []
    if skip_header: rows = rows[1:]
    return [cls(*r) for r in rows]

def load_theaters() -> List[Theater]:
    return _load_objects('theater', Theater)

def load_halls() -> List[Hall]:
    return _load_objects('hall', Hall)

def load_films() -> List[Film]:
    return _load_objects('film', Film)

def load_sessions() -> List[Session]:
    return _load_objects('session', Session)

def load_users() -> List[User]:
    return _load_objects('user', User)

def load_bookings() -> List[Booking]:
    return _load_objects('booking', Booking)

# -- Find helpers --

def find_session(session_id: str) -> Optional[Session]:
    for s in load_sessions():
        if s.idSession == session_id:
            return s
    return None

def find_hall(hall_id: str) -> Optional[Hall]:
    for h in load_halls():
        if h.idHall == hall_id:
            return h
    return None

def find_user(user_id: str) -> Optional[User]:
    for u in load_users():
        if u.idUser == user_id:
            return u
    return None

# -- Persisters --

def add_theater(t: Theater):
    append_row('theater', t.to_row())

def add_hall(h: Hall):
    append_row('hall', h.to_row())

def add_film(f: Film):
    append_row('film', f.to_row())

def add_session(s: Session):
    append_row('session', s.to_row())

def add_user(u: User):
    append_row('user', u.to_row())

def add_booking(b: Booking):
    append_row('booking', b.to_row())
