"""
Plain data classes representing domain entities.
No external dataclasses lib used to keep compatibility.
"""
from typing import Optional
from utils import genID

class Theater:
    def __init__(self, idTheater: Optional[str] = None, name: str = '', address: str = '', brand: str = ''):
        self.idTheater = idTheater if idTheater else genID("data/theater.csv")
        self.name = name
        self.address = address
        self.brand = brand

    def to_row(self):
        return [self.idTheater, self.name, self.address, self.brand]

class Hall:
    def __init__(self, idHall: Optional[str] = None, idTheater: str = '', name: str = '', rows: int = 0, cols: int = 0):
        self.idHall = idHall if idHall else genID("data/hall.csv")
        self.idTheater = idTheater
        self.name = name
        self.rows = int(rows)
        self.cols = int(cols)

    def to_row(self):
        return [self.idHall, self.idTheater, self.name, str(self.rows), str(self.cols)]

class Film:
    def __init__(self, idFilm: Optional[str] = None, name: str = '', genre: str = '', duration: int = 0, age: int = 0, director: str = '', actor: str = ''):
        self.idFilm = idFilm if idFilm else genID("data/film.csv")
        self.name = name
        self.genre = genre
        self.duration = int(duration)
        self.age = int(age)
        self.director = director
        self.actor = actor

    def to_row(self):
        return [self.idFilm, self.name, self.genre, str(self.duration), str(self.age), self.director, self.actor]

class Session:
    def __init__(self, idSession: Optional[str] = None, idHall: str = '', idFilm: str = '', date: str = '', time: str = '', price: str = ''):
        self.idSession = idSession if idSession else genID("data/session.csv")
        self.idHall = idHall
        self.idFilm = idFilm
        self.date = date  # YYYY-MM-DD
        self.time = time  # HH:MM
        self.price = float(price)

    def to_row(self):
        return [self.idSession, self.idHall, self.idFilm, self.date, self.time, self.price]

class User:
    def __init__(self, idUser: Optional[str] = None, idTheater: str = '', name: str = '', password: str = '', role: str = ''):
        self.idUser = idUser if idUser else genID("data/user.csv")
        self.idTheater = idTheater
        self.name = name
        self.password = password
        self.role = role

    def to_row(self):
        return [self.idUser, self.idTheater, self.name, self.password, self.role]

class Booking:
    def __init__(self, idBooking: Optional[str] = None, idSession: str = '', idUser: str = '', row: int = 0, col: int = 0, price: float = 0.0, timestamp: str = ''):
        self.idBooking = idBooking if idBooking else genID("data/booking.csv")
        self.idSession = idSession
        self.idUser = idUser
        self.row = int(row)
        self.col = int(col)
        self.price = float(price)
        self.timestamp = timestamp

    def to_row(self):
        return [self.idBooking, self.idSession, self.idUser, str(self.row), str(self.col), str(self.price), self.timestamp]
