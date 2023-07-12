import psycopg2
from config import db, user, password

#Удаляем все таблицы из Базы Данных
def drop_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE Phone_numbers;
                    DROP TABLE Clients;
                    """)
        conn.commit()
        print("База данных была успешно удалена!!!")
        print()

#Создаем необходимые таблицы для Базы Данных
def create_db(conn):

    with conn.cursor() as cur:
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Clients(
                    id serial PRIMARY KEY,
                    first_name varchar(50) NOT NULL,
                    last_name varchar(50) NOT NULL,
                    email varchar(50) UNIQUE
                    );
                    
                    CREATE TABLE IF NOT EXISTS Phone_numbers(
                    id serial PRIMARY KEY,
                    client_id INTEGER REFERENCES Clients(id),
                    phone_number varchar(20) 
                    );
                    """)
        
        conn.commit()
    print("База данных была успешно создана!!!")
    print()

#Создаем нового клиента
def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute(f"""
                    INSERT INTO Clients (first_name, last_name, email)
                    VALUES
                        ('{first_name}', '{last_name}', '{email}') 
                        RETURNING id;
                    """)
        print(f"Клиент {first_name} {last_name} был добавлен c идентификатором = {cur.fetchone()[0]}")
        print()

#Добавляем номер телефона для клиента
# def add_phone(conn, client_id, phone_number):
#     with conn.cursor() as cur:
#         cur.execute(f"""
#                     INSERT INTO Phone_numbers (client_id, phone_number)
#                     VALUES
#                         ({client_id}, '{phone_number}') 
#                         RETURNING id;
#                     """)
#         print(f"Phone number was added with id = {cur.fetchone()[0]}")

# def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
#     with conn.cursor() as cur:
#         print("Введите новые данные о клиенте: ")
#         cur.execute("""
#                     UPDATE Clients
#                     SET first_name = '{first_name}'
#                     WHERE id = {id};

#                     UPDATE Clients
#                     SET last_name = '{last_name}'
#                     WHERE id = {id};

#                     UPDATE Clients
#                     SET email = '{email}'
#                     WHERE id = {id};

#                     UPDATE Phone_numbers
#                     SET phone_number = '{phone_number}'
#                     WHERE client_id = '{client_id}';
#                     """)

# def delete_phone(conn, client_id, phone):
#     pass

# def delete_client(conn, client_id):
#     pass

# def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
#     pass


#Функция для вызова необходимых функций
def choose_function(conn):
    print("""Введите номер функции для выполнения: 
            1) Функция, создающая структуру БД (таблицы).
            2) Функция, удаляющая структуру БД (таблицы).
            3) Функция, позволяющая добавить нового клиента.
            4) Функция, позволяющая добавить телефон для существующего клиента.
            5) Функция, позволяющая изменить данные о клиенте.
            6) Функция, позволяющая удалить телефон для существующего клиента.
            7) Функция, позволяющая удалить существующего клиента.
            8) Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
            0) Выход из меню выбора.""")
    num = input()
    print()
    if num in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        if num == "0":
            exit()

        elif num == "1":
            create_db(conn)
            choose_function(conn)

        elif num == "2":
            drop_db(conn)
            choose_function(conn)

        elif num == "3":

            first_name = input("Введите email клиента: ")
            last_name = input("Введите фамилию клиента: ")
            email = input("Введите имя клиента: ")

            add_client(conn, first_name, last_name, email)  
            choose_function(conn)  
    else:
        print("Такой функции не существует, попробуй еще раз)")      
        print()          
        choose_function(conn)


with psycopg2.connect(database=db, user=user, password=password) as conn:
   choose_function(conn)
   
conn.close()




    
        












