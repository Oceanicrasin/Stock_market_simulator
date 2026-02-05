import sqlite3

DB_NAME = "Stock_market_db"

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS current_positions (
     trader_id INTEGER NOT NULL,
     ticker INTEGER NOT NULL,
     avg_price REAL NOT NULL,
     num_of_shares INTEGER NOT NULL,
     total_value REAL NOT NULL,
     profit REAL NOT NULL,
     
     PRIMARY KEY (trader_id,ticker),
     
     FOREIGN KEY (trader_id)
     REFERENCES traders (trader_id)
     ON DELETE CASCADE
     ON UPDATE CASCADE,
     
     FOREIGN KEY (ticker)
     REFERENCES companies (ticker)
     ON DELETE CASCADE
     ON UPDATE CASCADE
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaction_history (
     transaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     trader_id INTEGER NOT NULL,
     transaction_type VARCHAR NOT NULL,
     ticker INTEGER NOT NULL,
     share_price REAL NOT NULL,
     num_of_shares INTEGER NOT NULL,
     total_value REAL NOT NULL,
     
     FOREIGN KEY (trader_id) 
     REFERENCES traders (trader_id)
     ON DELETE CASCADE
     ON UPDATE CASCADE,

     FOREIGN KEY (ticker) 
     REFERENCES companies (ticker)
     ON DELETE CASCADE
     ON UPDATE CASCADE
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buy_order_book (
     buy_order_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     trader_id INTEGER NOT NULL,
     ticker INTEGER NOT NULL,
     share_price REAL NOT NULL,
     num_of_shares INTEGER NOT NULL,
     total_value REAL NOT NULL,
     
     FOREIGN KEY (trader_id) 
     REFERENCES traders (trader_id)
     ON DELETE CASCADE
     ON UPDATE CASCADE,

     FOREIGN KEY (ticker) 
     REFERENCES companies (ticker)
     ON DELETE CASCADE
     ON UPDATE CASCADE
     )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sell_order_book (
     sell_order_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
     trader_id INTEGER NOT NULL,
     ticker INTEGER NOT NULL,
     share_price REAL NOT NULL,
     num_of_shares INTEGER NOT NULL,
     total_value REAL NOT NULL,

     FOREIGN KEY (trader_id) 
     REFERENCES traders (trader_id)
     ON DELETE CASCADE
     ON UPDATE CASCADE,

     FOREIGN KEY (ticker) 
     REFERENCES companies (ticker)
     ON DELETE CASCADE
     ON UPDATE CASCADE
     )
    """)



    cursor.close()

def repopulate_db():
    # Fills all the tables with initial data
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM companies """)
    companies = cursor.fetchall()

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
    if not traders:
        cursor.execute(""" 
        INSERT INTO traders
        VALUES (0,100000)
        """)
    cursor.execute(""" SELECT * FROM current_positions """)
    current_positions = cursor.fetchall()
    cursor.execute(""" SELECT * FROM transaction_history """)
    transaction_history = cursor.fetchall()
    if not transaction_history and not current_positions:
        cursor.execute(""" 
        INSERT INTO current_positions VALUES (0,0,1,1000,1000,0)
         """)
        cursor.execute(""" 
        INSERT INTO current_positions VALUES (0,1,1,1000,1000,0)
         """)
        cursor.execute(""" 
        INSERT INTO current_positions VALUES (0,2,1,1000,1000,0)
         """)
        cursor.execute(""" 
        INSERT INTO transaction_history VALUES (0,0,'BUY',0,1,1000,1000)
         """)
        cursor.execute(""" 
        INSERT INTO transaction_history VALUES (1,0,'BUY',1,1,1000,1000)
         """)
        cursor.execute(""" 
        INSERT INTO transaction_history VALUES (2,0,'BUY',2,1,1000,1000)
         """)

    connection.commit()
    cursor.close()


def clear_db():
    # drops a table
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""DROP TABLE IF EXISTS buy_order_book""")
    cursor.execute("""DROP TABLE IF EXISTS sell_order_book""")
    cursor.execute("""DROP TABLE IF EXISTS current_positions""")
    cursor.execute("""DROP TABLE IF EXISTS transaction_history""")
    cursor.execute("""DROP TABLE IF EXISTS companies""")
    cursor.execute("""DROP TABLE IF EXISTS traders""")
    connection.commit()
    cursor.close()

def clear_buy_order_book():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE IF EXISTS buy_order_book""")
    connection.commit()
    cursor.close()


def print_db(table):
    #outputs all the contents of a table to the terminal
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM {} """.format(table))
    data = cursor.fetchall()
    for record in data:
        print(record)

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

def add_order(type, ticker, share_price, num_of_shares, total_value):
    connection = get_connection()
    cursor = connection.cursor()
    if type == "buy":
        cursor.execute(""" 
        INSERT INTO buy_order_book (trader_id, ticker, share_price, num_of_shares, total_value) 
        VALUES (?, ?, ?, ?, ?)
        """, (0, ticker, share_price, num_of_shares, total_value))
        connection.commit()
    else:
        cursor.execute(""" 
        INSERT INTO sell_order_book (trader_id, ticker, share_price, num_of_shares, total_value) 
        VALUES (?, ?, ?, ?, ?)
        """, (0, ticker, share_price, num_of_shares, total_value))
        connection.commit()


def insert_into_order_book(ticker, share_price, num_of_shares, total_value):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM buy_order_book""")
    item = [ticker, share_price, num_of_shares, total_value]
    order_book = cursor.fetchall()
    print("Order book Initial:", order_book)
    # delete the order_ids:
    for record in order_book:
        record.pop(0)
    print("Order book without id:", order_book)
    i = 0
    added = False
    for record in order_book:
        # causes order book to be ordered by ascending ticker
        if ticker < record[1]:
            insert(item,order_book,i)
            added = True
            break
        elif ticker == record[1]:
            if share_price <= record[2]:
                #causes order book to be ordered by ascending share price
                insert(item,order_book,i)
                added = True
                break
    if not added:
        order_book.append(item)

    #add records into database
    print("Order book with info: ",order_book)
    clear_buy_order_book()
    init_db()
    for record in order_book:
        add_order("buy",record[0],record[1],record[2],record[3])


def insert(item,lst,index):
    n_lst=[]
    for i in range(0,len(lst)-1):
        if i == index:
            n_lst.append(item)
        n_lst.append(lst[i])
    return n_lst

# a = insert(10,[1,2,3,4],1)
# print (a)

print_db("buy_order_book")



