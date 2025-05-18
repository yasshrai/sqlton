import mysql.connector
import os

def clear():
    os.system("cls")


def values():

    global h_val, u_val, p_val
    print('enter some detail for connecting to mysql server\n')

    h_val = input('\nenter host(by default localhost) ::')
    u_val = input('enter user (by default root)::')
    if h_val == "":
        h_val = 'localhost'
    if u_val == "":
        u_val = 'root'
    p_val = input('enter password ::')


def connecting():
    global cur
    try:
        mycon = mysql.connector.connect(host=h_val, user=u_val, password=p_val)
        if mycon.is_connected():
            print("\nSuccesfully connected to mysql server\n")
            print("---------------------------------------------------\n\n")
            input("Enter to continue")
            clear()
            cur = mycon.cursor()
            menu()
    except Exception as e:
        print("\nnot able to connect to server\n")
        print(e)
        print('please check yours details')
        print("or check whether the mysql is installed on your system or not")
        try_connect()


def show_database():
    global name_database
    cur.execute('show databases;')
    count = 0
    for rec in cur:
        count = count+1
        print(rec)
    print(f"there are {count} databases")
    choice = input("do you want to access any database y/n ::")
    print()
    try:
        if choice == 'y' or choice == 'Y':
            name_database = input("enter the name of databases ::")
            try:
                cur.execute(f'use {name_database}')
                print(f'connected to {name_database} database\n')
                print("------------------------------------------------\n\n")
                database_menu()
            except Exception as e:
                print('not able to access data ')
                print(e)
                menu()
        elif choice == 'n' or choice == 'N':
            menu()
    except Exception as e:
        print()
        print(e)
        database_menu()


def display_tables():
    global table_access_name
    cur.execute(f'show tables')
    count_table = 0
    for rec in cur:
        count_table = count_table+1
        print(f'Table name {rec}')
    print(f'there is total {count_table} no tables in {name_database}')
    t_choice = input('do you want to access table y/n ::  ')
    try:
        if t_choice == 'y' or t_choice == 'Y':
            table_access_name = input("enter table you want to access ::")
            print("---------------------------------------------\n\n")
            table_menu(table_access_name)
    except Exception as e:
        print(f"Not Able to access {table_access_name} table")
        print(e)


def drop_database():
    print("you can't access deleted database permanently")
    choice_del = input("do you really wanna delete database y/n::")
    if choice_del == 'y' or choice_del == 'Y' or choice_del == ' y':
        del_database = input('enter name of database for deleting ::')
        try:
            cur.execute(f"drop database {del_database}")
            print(f"successfully delete the database {del_database}")
        except Exception as e:
            print(e)
            database_menu()
    elif choice_del == 'n' or choice_del == 'N':
        database_menu()


def create_database():
    global new_database
    new_database = input("enter database name ::")
    cur.execute(f'create database {new_database}')
    print(f'database {new_database} created')


def create_table():
    column_name = []
    column_data = []
    print('\nplease enter details carefully')
    table_name = input("enter table name ::")
    val1 = int(input('enter the numbers of column in tables ::'))
    for i in range(1, val1+1):
        print(f'enter the details of {i}  column')
        column_val = input("enter the name of column ::")
        column_name.append(column_val)
        c_data_val = input("enter the valid datatype::")
        column_data.append(c_data_val)

    command = f'create table {table_name}('
    for j in range(0, val1):
        if j == val1-1:
            command = command+f'{column_name[j]} {column_data[j]}'
        else:
            command = command+f'{column_name[j]} {column_data[j]},'
    command = command+')'
    print(command)
    try:
        cur.execute(command)
    except Exception as e:
        print("NOT ABLE TO CREATE TABLE")
        print(e)


def drop_table():
    print("you can't access deleted table permanently")
    ch = input('do you really want to delete table y/n :: ')
    try:
        if ch == 'y' or ch == ' y':
            t_name = input("enter table name for removing :: ")

            cur.execute(f'drop table {t_name}')
        else:
            database_menu()
    except Exception as e:
        print(e)
        print('enter valid choice !!')
        database_menu()


def database_menu():
    clear()
    while True:
        print("--------------------------------------")
        print('-------------databases menu-----------')
        print("--------------------------------------\n")
        print('1.Display all tables of database')
        print('2.delete  database')
        print('3.create tables')
        print('4.drop table')
        print('5.exit from database menu\n')
        print("---------------------------------------\n\n")
        ch2 = int(input("enter the choice from above ::"))
        try:
            if ch2 == 1:
                display_tables()
            elif ch2 == 2:
                drop_database()
            elif ch2 == 3:
                create_table()
            elif ch2 == 4:
                drop_table()
            elif ch2 == 5:
                menu()
            else:
                print('please enter correct choice !!')
        except Exception as e:
            print(e)


def display_elements():
    clear()
    print("-------------------------------")
    print("---------display menu----------")
    print("-------------------------------\n")
    print("1.display all rows")
    print("2.display n number of row")
    print("-------------------------------\n")
    ch_2 = int(input("enter choice from above::"))
    try:
        if ch_2 == 1:
            cur.execute(f'select * from {table_access_name } ')
            for row in cur:
                print(row)
        elif ch_2 == 2:
            fetch_no = int(input("enter number of rows for display::"))
            cur.execute(f'select * from {table_access_name}')
            count = 1
            for row in cur:
                print(row)
                count = count+1
                if count > fetch_no:
                    break
        else:
            print("enter correct value ")
            print("try next time !!")
    except Exception as e:
        print(e)
        print("try next time !!")


def describe_table():
    global count_column
    print(" structure table ")
    cur.execute(f"desc {table_access_name}")
    count_column = 0
    for row in cur:
        print(row)
        count_column = count_column+1


def insert_values():
    print(f"there are {count_column} column  in {table_access_name}")
    val_row = []
    c1 = ''
    for i in range(1,count_column+1):
        print(f"enter value for column {i}")
        value = input("enter value ::")
        val_row.append(value)
    for j in range(1,count_column):
        if j == count_column:
            c1 = c1+f"{val_row[j]}"
        else:
            c1 = c1+f"{val_row[j]},"
            insert_command=f"insert into {table_access_name} values({c1})"
            print(insert_command)
            input()
            cur.execute(insert_command)
            

def update_values():
    column_change_name = input("Enter name of column for change :: ")
    reference_column = input(
        "Enter the name of column by which you have to change the value ::")
    value = input("Enter the value of reference column  ::")
    updated_value = input("Enter the updated value ::")
    try:
        command = f'''UPDATE {table_access_name}
                      SET {column_change_name} = "{updated_value}"
                      WHERE {reference_column} = "{value}"'''
        print(command)
        cur.execute(command)
        print("successfully updated the value")
    except Exception as e:
        print(e)
        print("can't able to update the value")


def alter_query():
    column_change_name = input("Enter the name of column to be changed: ")
    new_column_name = input(
        "Enter the new column name (if no change needed, leave it blank): ")
    new_data_type = input(
        "Enter the new data type for the column (if no change needed, leave it blank): ")
    try:
        command = f"ALTER TABLE {table_access_name} "
        if new_column_name:
            command += f"RENAME COLUMN {column_change_name} TO {new_column_name}"
        if new_data_type:
            if new_column_name:
                command += ", "
            command += f"ALTER COLUMN {new_column_name if new_column_name else column_change_name} TYPE {new_data_type}"
        cur.execute(command)
        print("Table altered successfully.")
    except Exception as e:
        print(e)
        print("Can't able to alter the table.")


def custom_query():
    command = input("enter the command ::")
    cur.execute(command)
    try:
        for i in cur:
            print(i)
    except Exception as e:
        print(e)
        print("not able to execute command")


def table_menu(x):
    clear()
    while True:
        print("------------------------------------------------")
        print("------------=------table menu ---=--------------")
        print("------------------------------------------------\n")
        print("1.display all elements of one table")
        print('2.describe table')
        print("3.insert value in table ")
        print("4.update values in table")
        print("5.alter table command(add column,redefine column)")
        print('6.custom query')
        print("7.exit")
        print("--------------=---------------------------------\n")
        ch1 = int(input("enter choice from table menu ::"))
        print("\n\n")
        try:
            if ch1 == 1:
                display_elements()
            elif ch1 == 2:
                describe_table()
            elif ch1 == 3:
                insert_values()
            elif ch1 == 4:
                update_values()
            elif ch1 == 5:
                alter_query()
            elif ch1 == 6:
                custom_query()
            elif ch1 == 7:
                database_menu()
            else:
                pass
        except Exception as e:
            print('please enter valid choice')
            print(e)


def menu():
    clear()
    while (True):
        print("---------------------------------")
        print('------------Main menu------------')
        print("---------------------------------")
        print('1.show database')
        print('2.create database')
        print('3.exit')
        print('---------------------------------\n\n')
        ch1 = int(input('enter the choice::'))
        print("\n")
        try:
            if ch1 == 1:
                show_database()
            elif ch1 == 2:
                create_database()
            elif ch1 == 3:
                exit()
        except Exception as e:
            print("enter correct choice !!\n")


def try_connect():
    while True:
        ch = input('do you want enter values again y/n ::')
        try:
            if ch == 'y' or ch == 'Y' or ch == ' y':
                values()
                connecting()
            elif ch == 'n' or ch == 'N':
                print('enter to terminate the program\n')
                input()
                exit()
            else:
                print('enter correct choice !!\n')
        except Exception as e:
            print('enter correct choice !!\n')
            
if __name__ == '__main__':
    values()
    connecting()
