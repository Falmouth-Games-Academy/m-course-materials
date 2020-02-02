import sqlite3


database = None
cursor = None


quitApp = False

while quitApp is False:

    print('\n')
    print('DB testbed')
    print('1..Create new DB')
    print('2..Open existing DB')
    print('3..Add')
    print('4..Display all')
    print('5..Find')            ##to do
    print('6..Delete contact')  ##to do
    print('7..drop tables')  ##to do
    print('X..Quit')
    print('\n')

    key = input('>')

    if key is '1': ##create db
        try:
            database = sqlite3.connect('data.sqlite')
            cursor = database.cursor()
            cursor.execute('create table table_phonenumbers (name varchar(20), number varchar(20) )')
        except:
            print('failed to create DB')

    if key is '2': ##open db
        try:
            database = sqlite3.connect('data.sqlite')
            cursor = database.cursor()
        except:
            print('Failed to open db')

    if key is '3':
        name = input('name')
        number = input('number')

        try:
            cursor.execute("select * from  table_phonenumbers where name =?", (name,) )
            rows = cursor.fetchall()

            if len(rows) == 0:
                cursor.execute('insert into table_phonenumbers(name, number) values(?,?)',(name,number))
                database.commit()
            else:
                print(name +' is already in the DB')
        except:
            print('Failed to add to DB')

    if key is '4':
        try:
            rows = cursor.execute("select * from " + "table_phonenumbers" + " order by name asc")

            for row in rows:
                print(row[0] + ' ' + row[1])
        except:
            print('Failed to display all')

    if key is '7':
        try:
            result = cursor.execute("insert into table_phonenumbers (name,number) values (\"bbb\", \"666\");drop table if exists table_phonenumbers;")
            print(str(result))
        except Exception as e:
            print('Failed to drop tables - ' + str(e))

    if key is 'x':
        quitApp = True
