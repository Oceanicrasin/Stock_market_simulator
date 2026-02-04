import sqlite3

DB_NAME = "Stock_market_db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    # Creates all the tables required for the program
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
    ticker INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    share_price REAL NOT NULL,
    market_cap REAL NOT NULL,
    revenue REAL NOT NULL,
    costs REAL NOT NULL,
    profit REAL NOT NULL,
    eps REAL NOT NULL,
    debt REAL NOT NULL
    )
    """)
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS traders (
      trader_id INTEGER PRIMARY KEY AUTOINCREMENT,
       capital REAL NOT NULL
       )
     """)
    connection.commit()
    cursor.close()

def repopulate_db():
    # Fills all the tables with initial data
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM companies """)
    companies = cursor.fetchall()
    print(companies)
    if not companies:
        cursor.execute(""" 
        INSERT INTO companies
        VALUES (0,"small_tech",1,10,3,1.5,1.5,0.15,0)
        """)
        cursor.execute(""" 
            INSERT INTO companies
            VALUES (1,"small_car",1,10,10,9,1,0.1,0.5)
            """)
        cursor.execute(""" 
            INSERT INTO companies
            VALUES (2,"small_airline",1,10,15,11,1,0.1,2)
            """)
        cursor.execute(""" 
            INSERT INTO companies
            VALUES (3,"small_supermarket",1,10,20,19,1,0.1,0.7)
            """)
        cursor.execute(""" 
            INSERT INTO companies
            VALUES (4,"medium_tech",10,100,30,15,15,1.5,0)
            """)
        cursor.execute(""" 
                INSERT INTO companies
                VALUES (5,"medium_car",10,100,100,90,10,1,5)
                """)
        cursor.execute(""" 
                INSERT INTO companies
                VALUES (6,"medium_airline",10,100,150,110,10,1,20)
                """)
        cursor.execute(""" 
                INSERT INTO companies
                VALUES (7,"medium_supermarket",10,100,200,190,10,1,7)
                """)
        cursor.execute(""" 
            INSERT INTO companies
            VALUES (8,"large_tech",100,1000,300,150,150,15,0)
            """)
        cursor.execute(""" 
                INSERT INTO companies
                VALUES (9,"large_car",100,1000,1000,900,100,10,50)
                """)
        cursor.execute(""" 
                INSERT INTO companies
                VALUES (10,"large_airline",100,1000,1500,1100,100,10,200)
                """)
        cursor.execute(""" 
                INSERT INTO companies
                VALUES (11,"large_supermarket",100,1000,2000,1900,100,10,70)
                """)
    cursor.execute("""SELECT * FROM traders """)
    traders = cursor.fetchall()
    print(traders)
    if not traders:
        cursor.execute(""" 
        INSERT INTO traders
        VALUES (0,100000)
        """)
    connection.commit()
    cursor.close()


def remove_table(table):
    # drops a table
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE IF EXISTS {}""".format(table))
    connection.commit()
    cursor.close()


def print_db():
    #outputs all the contents of a table to the terminal
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM companies """)
    companies = cursor.fetchall()
    for company in companies:
        print(company)

def extract_table(table):
    # returns a 2d list containing all the contents of a table
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM {} """.format(table))
    data = cursor.fetchall()
    return data

def change_capital(trader_id, capital):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(""" UPDATE traders SET capital = {} WHERE trader_id = {} """.format(capital, trader_id))
    connection.commit()
    cursor.close()


