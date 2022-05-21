
import sqlite3 as lite
import re
import sys

DB_FILENAME = 'members.db'

con = lite.connect(DB_FILENAME)
cur = con.cursor()

'''
Option to create a new table for a new database file
'''
if len(sys.argv) > 1:
    if sys.argv[1] == '-c':
        # Creating a new table
        cur.execute('create table club_members(name text primary key, phone_number int, email text, pkg int);')
        con.commit()
        print('Successfully created table club_members')
        sys.exit(0)

menu = \
'''
BR.STONE Fitness Club

1. New member
2. Delete member
3. Update member details
4. List all members
5. Search members by name
6. Exit

Choice: '''

# Print all the values that match the input in the specified column
def search_by(colname):
    inp = input(f'Enter search {colname}? ').strip()
    cur.execute(f'select {colname} from club_members where {colname} like \'%{inp}%\'')
    for item in cur.fetchall():
        print(item[0], end=', ')
    print('\n')

# check if colvalue exists in colname 
def check_if_in_db(colname, colvalue):
    cur.execute(f'select {colname} from club_members where {colname} = \'{colvalue}\'')
    return cur.fetchall() != []

# Check whether any colvalue entered for the column is valid
def is_valid_col_value(colname, value):
    if colname == 'name':
        return value != ''
    elif colname == 'phone_number':
        if len(value) != 10 or value.isdigit() == False:
            return False
        else:
            return True
        # return len(value) == 10 or value.isdigit() == True
    elif colname == 'email':
        return re.match(r'^[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+$', value) != None
    elif colname == 'pkg':
        return value in list('1234')

# Returns None when invalid package is selected
# else return the pkg number selected 
def show_pkg_menu():
    pkg_menu = \
            '''
Select your package:
1. Regular (Rs 300/m)
2. Pro (Rs 600/m)
3. Gold (Rs 1200/m)
4. Premium (Rs 3600/m)

Choose package: '''

    pkg = input(pkg_menu).strip()

    if not is_valid_col_value('pkg', pkg):
        print('Unknown package type')
        return None

    return int(pkg)

while True:
    op = input(menu).strip()

    if op not in list('123456'):
        print('Please select a valid option')
    elif op == '6':
        print('Thank you for coming! Visit again!')
        break

    # New member is joined
    else:
        if op == '1':
            name = input('Your name? ').strip()

            if not is_valid_col_value('name', name):
                print('The provided name is empty')
                continue

            number = input('Your phone number? ').strip()

            if not is_valid_col_value('phone_number', number):
                print("Your phone number is invalid")
                continue

            email = input('Your email? ').strip()

            if not is_valid_col_value('email', email):
                print("Your email is invalid")
                continue

            pkg = show_pkg_menu()
            if pkg == None:
                continue

            cur.execute(f'insert into club_members values(\'{name}\', {number}, \'{email}\', {pkg});')
            con.commit()

        elif op == '2':
            search_by('name')

            member=input("Enter the full name? ")
            if check_if_in_db('name', member) == False:
                print('No such name exists in the database')
                continue

            cur.execute(f'delete from club_members where name = \'{member}\';')
            con.commit()

        elif op == '3':
            search_by('name')
            name = input('Enter your name? ').strip()
            if not check_if_in_db('name', name):
                print(f'Name {name} not in database')
                continue

            col_menu = \
'''
Select the column to modify:
1. Name
2. Phone number
3. Email
4. Package
Column choice: '''
            col = input(col_menu).strip()

            if not is_valid_col_value('pkg', col):
                print('Please select a valid column')
                continue

            col_dict = {'1': 'name', '2': 'phone_number', '3': 'email', '4': 'pkg'}
            col_name = col_dict[col]

            if col in list('123'):
                new_value=input(f'Enter new {col_name}? ').strip()

                if not is_valid_col_value(col_name, new_value):
                    print(f'Invalid {col_name} value {new_value}')
                    continue
            else:
                new_value = show_pkg_menu()
                if new_value == None:
                    continue

            cur.execute(f'update club_members set {col_name} = \'{new_value}\' where name = \'{name}\';')
            con.commit()

        elif op == '4':
            cur.execute(f'select name,phone_number,email,pkg from club_members')
            for item in cur.fetchall():
                print(item[0],item[1],item[2],item[3],sep='\t ')

        elif op == '5':
            name = input('Enter search name? ').strip()
            cur.execute(f'select name from club_members where name like \'%{name}%\'')
            for name in cur.fetchall():
                print(name[0])
