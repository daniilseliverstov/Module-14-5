import sqlite3


def initiate_db():
    connection = sqlite3.connect('Product.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    title = ['Product 1', 'Product 2', 'Product 3', 'Product 4']
    description = ['Описание 1', 'Описание 2', 'Описание 3', 'Описание 4']
    price = ['100', '200', '300', '400']

    for prod in range(len(title)):
        cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                       (f'{title[prod]}', f'{description[prod]}', f'{price[prod]}'))

    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        ''')
    connection.commit()
    connection.close()


initiate_db()


def get_all_products():
    connection = sqlite3.connect('Product.db')
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products")
    db = cursor.fetchall()
    return list(db)


def add_user(username, email, age):
    balance = 1000
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    new_user = cursor.execute("SELECT COUNT(*) FROM Users").fetchone()[0] + 1
    cursor.execute(f'''INSERT INTO Users VALUES('{new_user}', '{username}', '{email}', '{age}', '{balance}')''')
    connection.commit()


def is_included(username):
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    if check_user is None:
        return False
    connection.commit()
    return True
