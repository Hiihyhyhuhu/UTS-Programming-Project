import operator
from repository import load_films, load_sessions, load_users, load_theaters, load_halls, add_user, load_bookings, add_film, add_hall
from services import print_seat_map, book_seat, occupancy_rate, seat_map
from constructor import User, Film, Hall
import datetime

def menu():
    print("Welcome to Chanh Hy's Theater Ticketing System")
    while True:
        print('\n--- Main Menu ---')
        print('1) Login')
        print('2) Signup')
        print('3) Exit')
        choice = input('Choose: ').strip()
        if choice == '1':
            login()
        elif choice == '2':
            signup()
        elif choice == '3':
            print('Exiting the system. Goodbye!')
            break
        else:
            print('Invalid choice, please try again.')

def login():
    users = load_users()
    username = input('Enter username: ').strip()
    password = input('Enter password: ').strip()
    me = None
    for u in users:
        if u.name == username and u.password == password:
            me = u
            break
    if not me:
        print('Invalid credentials')
        return
    print(f'Logged in as {me.role}')
    if me.role == 'guest':
        guest_flow(me)
    elif me.role == 'manager':
        manager_flow(me)
    elif me.role == 'receptionist':
        receptionist_flow(me)
    else:
        print('Unknown role')

def signup():
    name = input('Choose username: ').strip()
    password = input('Choose password: ').strip()
    role = input('Role (guest/manager/receptionist) [default guest]: ').strip() or 'guest'
    idTheater = ''
    if role in ('manager','receptionist'):
        idTheater = input('Assign to theater id (e.g. T1): ').strip()

    existing = load_users()
    for u in existing:
        if u.name == name:
            print('Username already exists. Try another.')
            return

    new_user = User(None, idTheater, name, password, role)
    add_user(new_user)
    print(f'User successfully created. You can now login.')

def receptionist_flow(user):
    while True:
        print(f'\n--- Receptionist Menu for {user.name} ---')
        print('1) Show session list')
        print('2) Show seat map for session')
        print('3) List booking info')
        print('4) Back to Main Menu')
        choice = input('Choose: ').strip()
        if choice == '1':
            print('\n--- All Sessions ---')
            all_halls = load_halls()
            all_theaters = load_theaters()
            all_sessions = load_sessions()

            # Filter sessions by user's assigned theater
            filtered_sessions = []
            for s in all_sessions:
                hall = next((h for h in all_halls if h.idHall == s.idHall), None)
                if hall and hall.idTheater == user.idTheater:
                    filtered_sessions.append(s)

            # Sort filtered sessions by date and time
            filtered_sessions.sort(key=lambda s: (s.date, s.time))

            if filtered_sessions:
                for s in filtered_sessions:
                    hall = next((h for h in all_halls if h.idHall == s.idHall), None)
                    hall_name = hall.name if hall else 'N/A'
                    theater_name = 'N/A'
                    if hall:
                        theater = next((t for t in all_theaters if t.idTheater == hall.idTheater), None)
                        theater_name = theater.name if theater else 'N/A'
                    print(f'ID: {s.idSession}, Film ID: {s.idFilm}, Date: {s.date}, Time: {s.time}, Hall: {hall_name} (ID: {s.idHall}), Theater: {theater_name}')
            else:
                print(f'No sessions found for your assigned theater ({user.idTheater}).')

        elif choice == '2':
            sid = input('Enter session id: ').strip()
            try:
                print_seat_map(sid)
            except ValueError as e:
                print(f'Error: {e}')
        elif choice == '3':
            print('\n--- All Bookings ---')
            bookings = load_bookings()
            if bookings:
                filter_date_str = input('Enter date to filter bookings (YYYY-MM-DD, leave empty for all): ').strip()
                filtered_bookings = []
                if filter_date_str:
                    try:
                        filter_date = datetime.datetime.strptime(filter_date_str, "%Y-%m-%d").date()
                        for b in bookings:
                            booking_date = datetime.datetime.strptime(b.timestamp.split('T')[0], "%Y-%m-%d").date()
                            if booking_date == filter_date:
                                filtered_bookings.append(b)
                    except ValueError:
                        print("Invalid date format. Showing all bookings.")
                        filtered_bookings = bookings
                else:
                    filtered_bookings = bookings

                if filtered_bookings:
                    for b in filtered_bookings:
                        print(f'ID: {b.idBooking}, Session ID: {b.idSession}, User ID: {b.idUser}, Seat: ({b.row}, {b.col}), Price: {b.price}, Timestamp: {b.timestamp}')
                else:
                    print(f'No bookings found for date {filter_date_str}.')
            else:
                print('No bookings found.')
        elif choice == '4':
            break
        else:
            print('Invalid choice, please try again.')

def manager_flow(user):
    while True:
        print(f'\n--- Manager Menu for {user.name} ---')
        print('1) List sessions and occupancy')
        print('2) Show seat map for session')
        print('3) List booking info (sorted)')
        print('4) Add new film')
        print('5) Add new hall')
        print('6) List films')
        print('7) Back to Main Menu')
        choice = input('Choose: ').strip()
        if choice == '1':
            print('\n--- Session Occupancy ---')
            all_halls = load_halls()
            all_sessions = load_sessions()

            # Filter sessions by user's assigned theater
            filtered_sessions = []
            for s in all_sessions:
                hall = next((h for h in all_halls if h.idHall == s.idHall), None)
                if hall and hall.idTheater == user.idTheater:
                    filtered_sessions.append(s)

            # Sort filtered sessions by date and time
            filtered_sessions.sort(key=lambda s: (s.date, s.time))

            if filtered_sessions:
                for s in filtered_sessions:
                    occupancy = occupancy_rate(s.idSession)
                    print(f'Session ID: {s.idSession}, Film ID: {s.idFilm}, Date: {s.date}, Time: {s.time}, Occupancy: {occupancy*100:.1f}%')
            else:
                print(f'No sessions found for your assigned theater ({user.idTheater}).')

        elif choice == '2':
            sid = input('Enter session id: ').strip()
            try:
                print_seat_map(sid)
            except ValueError as e:
                print(f'Error: {e}')
        elif choice == '3':
            print('\n--- All Bookings (Sorted by Timestamp) ---')
            bookings = load_bookings()
            if bookings:
                filter_date_str = input('Enter date to filter bookings (YYYY-MM-DD, leave empty for all): ').strip()
                filtered_bookings = []
                if filter_date_str:
                    try:
                        filter_date = datetime.datetime.strptime(filter_date_str, "%Y-%m-%d").date()
                        for b in bookings:
                            booking_date = datetime.datetime.strptime(b.timestamp.split('T')[0], "%Y-%m-%d").date()
                            if booking_date == filter_date:
                                filtered_bookings.append(b)
                    except ValueError:
                        print("Invalid date format. Showing all bookings.")
                        filtered_bookings = bookings
                else:
                    filtered_bookings = bookings

                if filtered_bookings:
                    filtered_bookings.sort(key=operator.attrgetter('timestamp'))
                    for b in filtered_bookings:
                        print(f'ID: {b.idBooking}, Session ID: {b.idSession}, User ID: {b.idUser}, Seat: ({b.row}, {b.col}), Price: {b.price}, Timestamp: {b.timestamp}')
                else:
                    print(f'No bookings found for date {filter_date_str}.')
            else:
                print('No bookings found.')
        elif choice == '4':
            print('\n--- Add New Film ---')
            name = input('Film Name: ').strip()
            genre = input('Genre: ').strip()
            duration = int(input('Duration (minutes): ').strip())
            age = int(input('Age restriction (0 for all ages): ').strip())
            director = input('Director: ').strip()
            actor = input('Main Actor: ').strip()
            new_film = Film(name=name, genre=genre, duration=duration, age=age, director=director, actor=actor)
            add_film(new_film)
            print(f"Film '{new_film.name}' (ID: {new_film.idFilm}) added successfully.")
        elif choice == '5':
            if not user.idTheater:
                print('Error: Manager is not assigned to a theater. Cannot add hall.')
            else:
                print('\n--- Add New Hall ---')
                hall_name = input('Hall Name: ').strip()
                rows = int(input('Number of rows: ').strip())
                cols = int(input('Number of columns: ').strip())
                new_hall = Hall(idTheater=user.idTheater, name=hall_name, rows=rows, cols=cols)
                add_hall(new_hall)
                print(f"Hall '{new_hall.name}' (ID: {new_hall.idHall}) added to Theater {user.idTheater} successfully.")
        elif choice == '6':
            while True:
                print('\n--- List Films Options ---')
                print('1) Sort films by attribute')
                print('2) Filter films by attribute')
                print('3) Back to Manager Menu')
                sub_choice = input('Choose: ').strip()

                if sub_choice == '1':
                    print('\n--- All Films (Sorted) ---')
                    sort_field = input('Sort by (name, genre, duration, age, director, actor) [default name]: ').strip().lower()
                    valid_sort_fields = ['name', 'genre', 'duration', 'age', 'director', 'actor']
                    if sort_field not in valid_sort_fields:
                        print(f'Invalid sort field: {sort_field}. Defaulting to sorting by name.')
                        sort_field = 'name'

                    films = load_films()
                    films.sort(key=operator.attrgetter(sort_field))
                    for f in films:
                        print(f'ID: {f.idFilm}, Name: {f.name}, Genre: {f.genre}, Duration: {f.duration} min, Age: {f.age}+, Director: {f.director}, Actor: {f.actor}')
                elif sub_choice == '2':
                    print('\n--- Filter Films ---')
                    filter_field = input('Filter by (name, genre, duration, age, director, actor): ').strip().lower()
                    valid_filter_fields = ['name', 'genre', 'duration', 'age', 'director', 'actor']
                    if filter_field not in valid_filter_fields:
                        print(f'Invalid filter field: {filter_field}. Please choose from {', '.join(valid_filter_fields)}.')
                        continue

                    filter_value = input(f'Enter the value for {filter_field}: ').strip()
                    films = load_films()

                    filtered_films = []
                    for f in films:
                        attr_value = str(getattr(f, filter_field)).lower()
                        if filter_field == 'age':
                            try:
                                if int(f.age) < int(filter_value):
                                    filtered_films.append(f)
                            except ValueError:
                                continue
                        elif filter_field == 'duration':
                            try:
                                if int(attr_value) == int(filter_value):
                                    filtered_films.append(f)
                            except ValueError:
                                continue
                        else:
                            if attr_value == filter_value.lower():
                                filtered_films.append(f)

                    if filtered_films:
                        print(f'\n--- Films filtered by {filter_field} {'>' if filter_field == 'age' else '='} {filter_value} ---')
                        for f in filtered_films:
                            print(f'ID: {f.idFilm}, Name: {f.name}, Genre: {f.genre}, Duration: {f.duration} min, Age: {f.age}+, Director: {f.director}, Actor: {f.actor}')
                    else:
                        print(f'No films found for {filter_field} {'>' if filter_field == 'age' else '='} {filter_value}.')
                elif sub_choice == '3':
                    break
                else:
                    print('Invalid choice, please try again.')
        elif choice == '7':
            break
        else:
            print('Invalid choice, please try again.')

def guest_flow(user):
    while True:
        print(f'\n--- Guest Menu for {user.name} ---')
        print('1) List films')
        print('2) List sessions for a film')
        print('3) Book seat')
        print('4) Back to Main Menu')
        c = input('Choose: ').strip()
        if c == '1':
            while True:
                print('\n--- List Films Options ---')
                print('1) Sort films by attribute')
                print('2) Filter films by attribute')
                print('3) Back to Guest Menu')
                sub_choice = input('Choose: ').strip()

                if sub_choice == '1':
                    print('\n--- All Films (Sorted) ---')
                    sort_field = input('Sort by (name, genre, duration, age, director, actor) [default name]: ').strip().lower()
                    valid_sort_fields = ['name', 'genre', 'duration', 'age', 'director', 'actor']
                    if sort_field not in valid_sort_fields:
                        print(f'Invalid sort field: {sort_field}. Defaulting to sorting by name.')
                        sort_field = 'name'

                    films = load_films()
                    films.sort(key=operator.attrgetter(sort_field))
                    for f in films:
                        print(f'ID: {f.idFilm}, Name: {f.name}, Genre: {f.genre}, Duration: {f.duration} min, Age: {f.age}+, Director: {f.director}, Actor: {f.actor}')
                elif sub_choice == '2':
                    print('\n--- Filter Films ---')
                    filter_field = input('Filter by (name, genre, duration, age, director, actor): ').strip().lower()
                    valid_filter_fields = ['name', 'genre', 'duration', 'age', 'director', 'actor']
                    if filter_field not in valid_filter_fields:
                        print(f'Invalid filter field: {filter_field}. Please choose from {', '.join(valid_filter_fields)}.')
                        continue

                    filter_value = input(f'Enter the value for {filter_field}: ').strip()
                    films = load_films()

                    filtered_films = []
                    for f in films:
                        attr_value = str(getattr(f, filter_field)).lower()
                        if filter_field == 'age':
                            try:
                                # Filter by age < provided age
                                if int(f.age) < int(filter_value):
                                    filtered_films.append(f)
                            except ValueError:
                                continue
                        elif filter_field == 'duration':
                            try:
                                if int(attr_value) == int(filter_value):
                                    filtered_films.append(f)
                            except ValueError:
                                continue
                        else:
                            if attr_value == filter_value.lower():
                                filtered_films.append(f)

                    if filtered_films:
                        print(f'\n--- Films filtered by {filter_field} {'>' if filter_field == 'age' else '='} {filter_value} ---')
                        for f in filtered_films:
                            print(f'ID: {f.idFilm}, Name: {f.name}, Genre: {f.genre}, Duration: {f.duration} min, Age: {f.age}+, Director: {f.director}, Actor: {f.actor}')
                    else:
                        print(f'No films found for {filter_field} {'>' if filter_field == 'age' else '='} {filter_value}.')
                elif sub_choice == '3':
                    break
                else:
                    print('Invalid choice, please try again.')
        elif c == '2':
            fid = input('Enter film id: ').strip()
            print(f'\n--- Sessions for Film ID {fid} ---')
            all_halls = load_halls()
            all_theaters = load_theaters()
            # Load sessions for the film, then sort by date and time
            film_sessions = [s for s in load_sessions() if s.idFilm == fid]
            film_sessions.sort(key=lambda s: (s.date, s.time))

            if film_sessions:
                for s in film_sessions:
                    hall = next((h for h in all_halls if h.idHall == s.idHall), None)
                    hall_name = hall.name if hall else 'N/A'
                    theater_name = 'N/A'
                    if hall:
                        theater = next((t for t in all_theaters if t.idTheater == hall.idTheater), None)
                        theater_name = theater.name if theater else 'N/A'
                    print(f'Session ID: {s.idSession}, Date: {s.date}, Time: {s.time}, Hall: {hall_name} (ID: {s.idHall}), Theater: {theater_name}')
            else:
                print(f'No sessions found for film ID {fid}.')
        elif c == '3':
            sid = input('Session id: ').strip()
            try:
                print('\n--- Current Seat Map ---')
                print_seat_map(sid)
                hall_rows, hall_cols, _ = seat_map(sid) # Get hall dimensions for seat input validation
                row_input = input(f'Enter row (1-{hall_rows}): ').strip()
                col_input = input(f'Enter column (1-{hall_cols}): ').strip()
                row = int(row_input)
                col = int(col_input)

                booked_session = next((s for s in load_sessions() if s.idSession == sid), None)
                if not booked_session:
                    raise ValueError('Session not found.')

                booking = book_seat(sid, user.idUser, row, col)
                print(f'Booking successful! Booking ID: {booking.idBooking}, Price: {booking.price}')
                confirm = input('Confirm booking? (yes/no): ').strip().lower()
                if confirm == 'yes':
                    print('\n--- Updated Seat Map ---')
                    print_seat_map(sid)
                else:
                    print('Booking cancelled.')

            except ValueError as e:
                print(f'Booking failed: {e}')
            except Exception as e:
                print(f'An unexpected error occurred during booking: {e}')
        elif c == '4':
            break
        else:
            print('Invalid choice, please try again.')

if __name__ == '__main__':
    menu()
