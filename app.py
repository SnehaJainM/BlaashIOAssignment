from flask import Flask, request, jsonify
from database import get_db_connection
from sms_service import send_sms

app = Flask(__name__)
@app.route('/')
def homepage():
     return jsonify({"message": "Welcome to the homepage of GamePortal.. "}), 201

@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    players_id = data['PlayersID']
    game_id = data['GameID']
    score = data['Score']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO scores (PlayersID, GameID, Score) VALUES (%s, %s, %s)", 
                   (players_id, game_id, score))

    conn.commit()

    # Get player's phone number to send the SMS
    cursor.execute("SELECT PhoneNumber FROM players WHERE PlayersID = %s", (players_id,))
    phone_number = cursor.fetchone()[0]

    # Send SMS
    message = f"Your final score for game ID {game_id} is {score}."
    send_sms(phone_number, message)

    cursor.close()
    conn.close()

    return jsonify({"message": "Score added successfully"}), 201

@app.route('/leaderboard/<game_id>', methods=['GET'])
def leaderboard(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT P.PlayerName, SUM(S.Score) as total_score
        FROM players P
        JOIN scores S ON P.PlayersID = S.PlayersID
        WHERE S.GameID = %s
        GROUP BY P.PlayerName
        ORDER BY total_score DESC
        LIMIT 5
    """, (game_id,))

    leaderboard = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(leaderboard)

if __name__ == '__main__':
    app.run(debug=True)
