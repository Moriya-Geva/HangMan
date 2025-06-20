import json

from click import password_option
from flask import Flask, request, abort, make_response, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin

from user import user

app = Flask(__name__)
CORS(app, supports_credentials=True)


def load_users_from_file():
    # טוען את המשתמשים הקיימים מהקובץ (אם קיים)
    try:
        with open('./users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # אם אין קובץ או אם הקובץ לא חוקי, נחזיר רשימה ריקה
        return []


def save_users_to_file(users):
    # שומר את המשתמשים לקובץ JSON
    with open('./users.json', 'w') as f:
        json.dump(users, f, indent=4)


def add_user_to_file(user):
    # טוען את המשתמשים הקיימים
    users = load_users_from_file()

    # מוסיף את המשתמש החדש לרשימה
    users.append(user.to_dict())

    # שומר את כל המשתמשים בקובץ
    save_users_to_file(users)

# קריאת המילים מהקובץ
def load_words():
    with open('./word_bank', 'r') as f:
        words = f.read().splitlines()
    return words
# רשימת מילים מתוך הקובץ
word_list = load_words()


@cross_origin(app, supports_credentials=True)  # לא חובה
@app.route('/say_hello', methods=['GET', 'POST'])
def say_hello():
    if request.method == 'POST':
        obj = request.json
        name = obj.get('name')
        return jsonify(f"hello {name}")
    return jsonify("Hello!")


@cross_origin(app, supports_credentials=True)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    tz = data.get('tz')  # תעודת זהות
    password = data.get('password')
    # יצירת משתמש חדש
    new_user = user(name, tz, password, 0, [], 0)

# דוגמה לשימוש:
    add_user_to_file(new_user)

    # החזרת הודעת הצלחה
    return jsonify({"message": f"User {name} registered successfully"}), 201

@app.route('/get_word', methods=['POST'])
def get_word():
    obj = request.json
    number = obj.get('number', 0)
    if number < 0:
        return jsonify({"error": "Invalid number"}), 400

    # בחירת מילה באופן מעגלי
    selected_word = word_list[number % len(word_list)]
    return jsonify({"word": selected_word})



@cross_origin(app, supports_credentials=True)
@app.route('/update', methods=['POST'])
def update():
    data = request.json
    tz = data.get('tz')
    word = data.get('word')
    win = data.get('win')

    users = load_users_from_file()  # טוענים את רשימת הלקוחות מהקובץ
    # בודקים אם הלקוח כבר קיים
    for i, _user in enumerate(users):
        for i, _user in enumerate(users):
            if _user.get('tz') == tz:
                # עדכון המידע
                _user['numPlay'] += 1
                if word not in _user['strAppear']:
                    _user['strAppear'].append(word)
                _user['numWin'] += win

                with open('users.json', 'w') as f:
                    json.dump(users, f, indent=4)
                return jsonify({"message": "User data updated successfully!"}), 200
            # אם הלקוח לא נמצא
    return jsonify({"message": "User not found!"}), 404

# @cross_origin(app, supports_credentials=True)
# @app.route('/logout', methods=['DELETE'])
# def logout():
#     response = make_response(jsonify({"Game is over!"}))
#     # מחיקת העוגייה על ידי הצבת זמן פג תוקף
#     response.set_cookie('username', '', max_age=0)
#     return response



@cross_origin(app, supports_credentials=True)
@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    req = request.json
    response = make_response("Cookie is set!")
    # מקבלת: שם העוגיה, ערך העוגיה, משך התוקף של העוגיה בשניות, העוגיה נגישה רק דרך HTTP/S כלומר, JS לא יוכל לגשת לזה מטעמי אבטחה
    # העוגיה תישלח רק דרך פרוטוקול מאובטח- HTTPS ורק אם ההודעה מוצפנת כדי להגן מפני יירוטים
    # העוגיה תישלח רק אם מקורה באתר ממנו היא נשלחה. כלומר, לחיצה על קישור לא תשלח את העוגייה כדי למנוע התקפות
    response.set_cookie('user_name', req['user_name'], max_age=600, httponly=True, secure=False, samesite='None')
    print(response.headers['Set-Cookie'])
    return response


@cross_origin(app, supports_credentials=True)
@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    user_name = request.cookies.get('user_name')
    print(f"Get: {user_name}")
    if user_name:
        return f'Hello, {user_name}!'
    return 'No cookie found!'



if __name__ == '__main__':
    app.run(debug=True)
