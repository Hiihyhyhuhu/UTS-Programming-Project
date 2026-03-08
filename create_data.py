"""
Small script to create example CSV files with data to test the system.
Run once to create data/ files.
"""
from utils import genID, ensure_tables, write_table, path_for
from constructor import Theater, Hall, Film, Session, User

ensure_tables()

# Create data for theaters
th_rows = [['idTheater','name','address','brand'],
           ['T000001','CGV Aeon Binh Tan','Long Bien','CGV'],
           ['T000002','Galaxy Nguyen Du','D1','Galaxy'],
           ['T000003','Lotte Cinema Q7','Q7','Lotte']]
write_table('theater', th_rows)

# Create data for halls (price removed from Hall, now in Session)
h_rows = [['idHall','idTheater','name','rows','cols'],
          ['H000001','T000001','Hall A','5','6'],
          ['H000002','T000001','Hall B','4','5'],
          ['H000003','T000002','Hall 1','8','10'],
          ['H000004','T000002','Hall 2','6','7'],
          ['H000005','T000003','Premier Hall','3','4'],
          ['H000006','T000001','Hall C','7','8']]
write_table('hall', h_rows)

# Films
f_rows = [['idFilm','name','genre','duration','age','director','actor'],
          ['F000001','The Great Escape','Action','120','13','J Director','Alice'],
          ['F000002','Love & Coffee','Romance','95','0','A Director','Cathy'],
          ['F000003','Sci-Fi Odyssey','Sci-Fi','150','16','B Director','Bob'],
          ['F000004','Kids Adventure','Animation','80','0','C Director','Charlie'],
          ['F000005','The Mystery','Thriller','110','18','D Director','David'],
          ['F000006','Fantasy World','Fantasy','130','7','E Director','Eve'],
          ['F000007','Action Reloaded','Action','135','16','J Director','Alice'],
          ['F000008','Sweet Romance','Romance','100','0','A Director','Cathy'],
          ['F000009','Space Journey','Sci-Fi','160','13','B Director','Bob'],
          ['F000010','Jungle Quest','Animation','90','0','C Director','Charlie']]
write_table('film', f_rows)

# Sessions - Price added
s_rows = [['idSession','idHall','idFilm','date','time','price'],
          ['S000001','H000001','F000001','2025-12-08','19:00','50.0'],
          ['S000002','H000001','F000001','2025-12-09','19:00','50.0'],
          ['S000011','H000002','F000001','2025-12-09','18:00','35.0'],
          ['S000012','H000003','F000001','2025-12-09','18:00','45.0'],
          ['S000013','H000004','F000001','2025-12-09','11:00','55.0'],
          ['S000014','H000006','F000001','2025-12-09','18:00','65.0'],
          ['S000003','H000002','F000002','2025-12-08','21:00','45.0'],
          ['S000004','H000003','F000003','2025-12-10','18:30','70.0'],
          ['S000005','H000004','F000004','2025-12-11','14:00','40.0'],
          ['S000006','H000001','F000002','2025-12-08','10:00','40.0'],
          ['S000007','H000006','F000005','2025-12-12','20:00','60.0'],
          ['S000008','H000002','F000007','2025-12-09','17:00','55.0'],
          ['S000009','H000003','F000008','2025-12-10','20:00','65.0'],
          ['S000010','H000004','F000009','2025-12-11','21:00','75.0']]
write_table('session', s_rows)

# Users
u_rows = [['idUser','idTheater','name','password','role'],
          ['U000001','T000001','manager1','m123','manager'],
          ['U000002','T000001','reception1','r123','receptionist'],
          ['U000003','','guest1','g123','guest'],
          ['U000004','T000002','manager2','m456','manager'],
          ['U000005','','guest2','g456','guest'],
          ['U000006','T000003','reception2','r456','receptionist']]
write_table('user', u_rows)

# Bookings (keeping existing prices, as booking price is independent once set)
b_rows = [['idBooking','idSession','idUser','row','col','price','timestamp'],
          ['B000001','S000001','U000001','3','2','50','2025-12-08T19:00:00'],
          ['B000002','S000001','U000001','4','5','50','2025-12-08T19:00:00'],
          ['B000003','S000004','U000005','2','3','70','2025-12-10T18:00:00'],
          ['B000004','S000004','U000003','2','4','70','2025-12-10T18:05:00'],
          ['B000005','S000005','U000005','1','1','40','2025-12-11T13:30:00'],
          ['B000006','S000007','U000003','5','6','60','2025-12-12T19:00:00'],
          ['B000007','S000008','U000001','1','1','55','2025-12-09T16:00:00'],
          ['B000008','S000009','U000005','3','3','65','2025-12-10T19:00:00']]
write_table('booking', b_rows)

print('Bootstrap data created in data/ folder')
