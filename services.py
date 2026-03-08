import datetime
from typing import List, Tuple
from repository import load_halls, load_sessions, load_films, load_bookings, add_booking, find_session, find_hall
from constructor import Booking
from utils import genID

def seat_map(session_id: str) -> Tuple[int, int, List[Tuple[int, int]]]:
    """Return (rows, cols, booked_seats_list)"""
    s = find_session(session_id)
    if not s:
        raise ValueError('Session not found')
    hall = find_hall(s.idHall)
    if not hall:
        raise ValueError('Hall not found')
    rows, cols = hall.rows, hall.cols
    booked = []
    for b in load_bookings():
        if b.idSession == session_id:
            booked.append((b.row, b.col))
    return rows, cols, booked

def print_seat_map(session_id: str):
    rows, cols, booked = seat_map(session_id)
    booked_set = set(booked)
    lines = []
    # Add a screen indicator
    lines.append(f"       |    SCREEN    |         ")

    # Add column numbers (centered above each column)
    col_numbers = []
    for c in range(1, cols + 1):
        col_numbers.append(f"{c:^3}") # Center column number in 3 spaces
    lines.append("   " + " ".join(col_numbers))

    # Add row letters and seats
    for r in range(1, rows + 1):
        row_elems = []
        for c in range(1, cols + 1):
            if (r, c) in booked_set:
                row_elems.append('[X]')
            else:
                row_elems.append('[ ]')
        lines.append(f"{r:^2} {' '.join(row_elems)}") # Prepend row number
    print('\n'.join(lines))

def is_seat_available(session_id: str, row: int, col: int) -> bool:
    for b in load_bookings():
        if b.idSession == session_id and b.row == row and b.col == col:
            return False
    return True

def book_seat(session_id: str, user_id: str, row: int, col: int, price: float = None) -> Booking:
    # Validate session and hall
    s = find_session(session_id)
    if not s:
        raise ValueError('Session not found')
    hall = find_hall(s.idHall)
    if not hall:
        raise ValueError('Hall not found')
    if row < 1 or row > hall.rows or col < 1 or col > hall.cols:
        raise ValueError('Seat out of range')
    if not is_seat_available(session_id, row, col):
        raise ValueError('Seat already booked')
    if price is None:
        price = s.price # Changed from hall.price to s.price
    timestamp = datetime.datetime.now().isoformat()
    booking_id = genID('data/booking.csv')
    booking = Booking(booking_id, session_id, user_id, row, col, price, timestamp)
    add_booking(booking)
    return booking

# Analytics: occupancy rate for a session
def occupancy_rate(session_id: str) -> float:
    s = find_session(session_id)
    if not s:
        return 0.0
    hall = find_hall(s.idHall)
    total = hall.rows * hall.cols
    booked = sum(1 for b in load_bookings() if b.idSession == session_id)
    return booked / total if total else 0.0
