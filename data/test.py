import csv, sqlite3


conn = sqlite3.connect("db.sqlite3")
curs = conn.cursor()
# curs.execute("CREATE TABLE PCFC (name INTEGER, measurement_unit TEXT);")
reader = csv.reader(open('ingredients.csv', 'r'), delimiter=',')
count = 1
for row in reader:
#     print(row)

    to_db = [count, row[0], row[1]]
    curs.execute("INSERT INTO recipes_ingredient VALUES (?, ?, ?);", to_db)
    count += 1

conn.commit()

