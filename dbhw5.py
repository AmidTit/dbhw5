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
        cur.execute("""
                    INSERT INTO Clients (first_name, last_name, email)
                    VALUES
                        (%s, %s, %s) 
                        RETURNING id;
                    """, (first_name, last_name, email))
        conn.commit()
        print()
        print(f"Клиент {first_name} {last_name} был добавлен c идентификатором = {cur.fetchone()[0]}")
        print()

#Добавляем номер телефона для клиента
def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT id FROM Clients
                    WHERE id = %s
                    """, (client_id, ))
        
        if cur.fetchone() == None:
            print("Id не найден, повторите попытку еще раз")                           
        else:
            cur.execute("""
                        INSERT INTO Phone_numbers (client_id, phone_number)
                        VALUES
                            (%s, %s) 
                            RETURNING id;
                        """, (client_id, phone_number))
            conn.commit()
            print(f"Номер телефона был добавлен с id = {cur.fetchone()[0]}")
               
#Изменяем данные о клиенте
def change_client(conn, client_id, first_name, last_name, email, phone_number):
    with conn.cursor() as cur:
        
        cur.execute("""
                    UPDATE Clients
                    SET first_name = %s
                    WHERE id = %s;
                    """, (first_name, client_id))
        
        cur.execute("""
                    UPDATE Clients
                    SET last_name = %s
                    WHERE id = %s;
                    """, (last_name, client_id))
        
        cur.execute("""
                    UPDATE Clients
                    SET email = %s
                    WHERE id = %s;
                    """, (email, client_id))

        cur.execute("""
                    UPDATE Phone_numbers
                    SET phone_number = %s
                    WHERE client_id = %s;
                    """, (phone_number, client_id))
        conn.commit()
        print("Данные были успешно обновлены!!!")

#Удаляем телефонные номера по client_id
def delete_phone(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
                        SELECT phone_number FROM Phone_numbers
                        WHERE id = %s
                    """, (id, ))
        
        cur.execute("""
                    DELETE FROM Phone_numbers
                    WHERE id = %s
                    """, (id, ))
        print("Номер был успешно удален!!!")
        conn.commit()

#Удаляем существующего клиента         
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM Phone_numbers
                    WHERE client_id = %s 
                    """, (client_id, ))
        cur.execute("""
                    DELETE FROM Clients
                    WHERE id = %s
                    """, (client_id, ))
        print("Клиент был успешно удален!!!")
        conn.commit()

#Поиск клиента        
def find_client(conn, info, first_name=None, last_name=None, email=None, phone_number=None):
    if info == 1:
        with conn.cursor() as cur:
            cur.execute("""SELECT id FROM Clients WHERE first_name = %s AND last_name = %s AND email=%s;
                        """, (first_name, last_name, email))
            
            if cur.rowcount > 0:
                print(f"клиент с id = {cur.fetchone()[0]} был успешно найден")
                conn.commit()
                
            else:    
                print("Клиент не найден")
    else:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT client_id FROM Phone_numbers WHERE phone_number = %s;
            """, (phone_number, ))

            if cur.rowcount > 0:
                print(f"клиент с id = {cur.fetchone()[0]} был успешно найден")
                conn.commit()
                
            else:    
                print("Клиент не найден")
            


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

            first_name = input("Введите имя клиента: ")
            last_name = input("Введите фамилию клиента: ")
            email = input("Введите email клиента: ")

            add_client(conn, first_name, last_name, email) 
            choose_function(conn)  

        elif num == "4":

            client_id, phone_number = int(input("Введите id клиента: ")), input("Введите номер телефона клиента: ")
            
            add_phone(conn, client_id, phone_number)
            print()
            choose_function(conn)

        elif num == "5":
            print("Введите новые данные о клиенте: ")
            print()
            client_id = int(input("Введите id клиента, данные о которм вы хотите изменить: ")) 
            first_name, last_name = input("Введите новое имя клиента: "), input("Введите новую фамилию клиента: ")
            email, phone_number = input("Введите новый  email клиента: "), input("Введите новый номер телефона клиента: ")
            change_client(conn, client_id, first_name, last_name, email, phone_number)
            print()          
            choose_function(conn)

        elif num == "6":
            id = input("Введите id номера телефона для удаления: ")
            delete_phone(conn, id)
            print()          
            choose_function(conn)

        elif num == "7":
            client_id = input("Введите id Клиента для удаления: ")
            delete_client(conn, client_id)
            print()          
            choose_function(conn) 

        elif num == "8":
            print()
            info = int(input('''
                        По каким данным вы хотите осуществить поиск клиента?
                        1) По ФИО и email
                        2) По номеру телефона
                        '''))
            
            if info == 1:

                first_name = input('Введите имя для поиска: ')
                last_name = input('Введите фамилию для поиска: ')
                email = input('Введите email для поиска: ')
                find_client(conn, info, first_name, last_name, email)
                print()          
                choose_function(conn) 

            elif info == 2:
                phone_number = input('Введите телефон для поиска: ')
                find_client(conn, info, phone_number) 
                print()          
                choose_function(conn)   


    else:
        print("Такой функции не существует, попробуй еще раз)")      
        print()          
        choose_function(conn)

if __name__ == "__main__":

    with psycopg2.connect(database=db, user=user, password=password) as conn:
        choose_function(conn)
   
conn.close()




    
        












