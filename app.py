from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Backend is working!"


@app.route('/api/games', methods=['GET'])
def get_games():
    try:
        genre = request.args.get('genre')
        search = request.args.get('search')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = 'SELECT * FROM games'
        params = []

        if genre:
            query += ' WHERE genre = ?'
            params.append(genre)

        if search:
            if 'WHERE' in query:
                query += ' AND title LIKE ?'
            else:
                query += ' WHERE title LIKE ?'
            params.append(f'%{search}%')

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        games_list = [dict(row) for row in rows]

        return jsonify({
            "success": True,
            "data": games_list,
            "count": len(games_list),
            "filters": {
                "genre": genre,
                "search": search
            }
        })

    except sqlite3.Error as e:
        return jsonify({
            "success": False,
            "error": "Ошибка базы данных",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Внутренняя ошибка сервера",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



