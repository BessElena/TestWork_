import sqlite3

def create_database():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT,
            platform TEXT,
            description TEXT
        )
    ''')


    cursor.execute('SELECT COUNT(*) FROM games')
    if cursor.fetchone()[0] == 0:
        test_game = (
            "Космический рейнджер",
            "Экшен",
            "PC",
            "Космический шутер с прокачкой корабля."
        )
        cursor.execute('''
            INSERT INTO games (title, genre, platform, description)
            VALUES (?, ?, ?, ?)
        ''', test_game)

    conn.commit()
    conn.close()
    print("База данных и таблица созданы. Тестовые данные добавлены (если их не было).")


if __name__ == '__main__':
    create_database()


