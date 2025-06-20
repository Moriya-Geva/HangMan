from http.client import responses

import requests
import time

from flask import json

from server import load_users_from_file
from user import user

# שמירת הכתובת עליה רץ השרת. הכתובת יכולה להיות גם חיצונית
basic_url = "http://127.0.0.1:5000/"
session = requests.session()

def print_word(under):
    print(" ".join(under))

def directions():
    return (r""":הוראות המשחק
           תחילה תתבקש להכניס תעודת זהות, כך תוכל להיות מזוהה על ידי המערכת, 
           ויהיה אפשר לעדכן את נתוני המשחק.
           אם אתה לא רשום המערכת תשלח אותך להתחברות.
           לאחר מכן תתבקש להכניס מספר. באמצעות המספר המערכת תגריל מילה ולחר מכן תתבקש להכניס אות 
           אם האות שניחשת מופיעה במילה שהוגרלה,
            אז תחשף האות בכל הפעמים שבהן היא מופיעה. אם האות שניחשו שגויה, 
           השמערכת תצייר חלק אחד מתוך עמוד תלייה שעליו תלוי אדם
            עליך לנחש את המילה בטרם יושלם עמוד התלייה.
           מספר הניסיונות השגויים שתוכל לטעות הם שבעה אם הניחוש אינו נכון, הדבר נחשב כניסיון שגוי""")

hangMan = [
    r"""x-------x""",
    r"""x-------x
|
|
|
|
|""",
    r"""x-------x
|       |
|       0
|
|
|""",
    r"""x-------x
|       |
|       0
|       |
|
|""",
    r"""x-------x
|       |
|       0
|      \|/ 
|
|""",
    r"""x-------x
|       |
|       0
|      \|/ 
|      \
|
""",
    r"""x-------x
|       |
|       0
|      \|/ 
|      \ / 
|"""
]
logo = r"""	
                _    _
               | |  | |
               | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
               |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
               | |  | | (_| | | | | (_| | | | | | | (_| | | | |
               |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                                    __/ |
                                   |___/
"""
print(logo)

print('ברוך הבא למשחק איש תלוי')
print()
# --------כניסה למשחק-------
tz = ''
while True:
    try:
        enter = int(input(r"""להוראות המשחק לחץ 1
לכניסה למשחק לחץ 2
"""))
        if enter == 2:
            break  # יציאה מהלולאה אם הקלט תקין
        elif enter == 1:
            print(directions())
        else:
            print("בחירה לא חוקית, נסה שוב.")
    except ValueError:
        print("אנא הכנס מספר תקין.")
# ----חיפוש המשתמש ומעבר למשחק---
if enter == 2:
    tz = input(r'''לכניסה למשחק עליך להכנס תעודת זהות
''')
    id_number = str(tz).strip()
    while len(id_number) != 9 or not id_number.isdigit():
        tz = input(r'''תעודת זהות לא תקינה, נסה שוב
''')
        print(" ")
        id_number = str(tz).strip()
    name = ''
    password = ''
    new_user = False
    use = user(name, tz, password, 0, [], 0)
    with open('./users.json', 'r') as f:
        data = json.load(f)
    users = [user.from_dict(us) for us in data]
    for i, usr in enumerate(users):
        if usr.tz == tz:
            use = usr
            new_user = True
            break

    if not new_user:  # אם לא נמצא משתמש עם אותה ת.ז
        print("אינך רשום במערכת עליך להרשם")
        name = input(r'''הכנס שם
''')
        password = input(r'''הכנס סיסמא
''')
        response = requests.post(f'{basic_url}register', json={"name": name, "password": password, "tz": tz})
        use = user(name, tz, password, 0, [], 0)
        if response.status_code == 201:  # 201 = נוצר בהצלחה
            cookies = response.cookies
            print(response.status_code)  # הדפסת תגובת השרת
        else:
            print(f"Error. Status code: {response.status_code}")
    #         -----יצירת עוגיה----
    cookie_content = {'user_name': use.name}
    response = session.post(f'{basic_url}set_cookie', json=cookie_content)
    #         ---הדפסת שם המשתמש---
    response = requests.post(f"{basic_url}say_hello", json={"name": use.name})
    print(f" {response.text}")
# הכנסת מספר לבחירת אפשרויות

while True:
    try:
        # הצגת התפריט כל הזמן עד שהמשתמש יבחר יציאה
        number = int(input(r"""להוראות המשחק לחץ 1
להתחלת המשחק לחץ 2
לצפייה בהסטוריית המשחקים לחץ 3
ביטול וחזרה לחץ 4
"""))

        if number == 1:
            print(directions())  # הדפסת ההוראות

        elif number == 2:
            # התחלת המשחק
            # # # בקשה לקבלת העוגיות
            cookies = response.cookies.get_dict()  # חילוץ העוגיות מהבקשה הקודמת
            response = session.get(f'{basic_url}get_cookie')  # , cookies=cookies
            num = int(input(r'''הכנס מספר להגרלת מילה
'''))
            response = requests.post(f"{basic_url}get_word", json={"number": num})
            word = response.json()['word']
            num1 = 0
            letter = ''
            win = 0
            word = word.lower()
            strWord = list(word)
            length = len(word)
            under = ['_'] * length
            print('לרשותך 7 פסילות, משך המשחק הינו 10 דק')
            print_word(under)
            while num1 < 7 and length > 0:
                letter = input('הכנס אות')
                if letter in strWord:
                    for i in range(len(strWord)):
                        if strWord[i] == letter and under[i] == '_':
                            under[i] = letter
                            length -= 1
                    print_word(under)
                else:
                    print(hangMan[num1])  # הדפסת שלב בתלייה
                    num1 += 1
                    print_word(under)
            if length == 0:
                win = 1
            response = requests.post(f"{basic_url}update",
                                     json={"name": use.name, 'tz': use.tz, "password": use.password,
                                           "word": word, "win": win})
            if win == 1:
                print("כל הכבוד!! ניצחת!👏🎉🎊🥳")
            else:
                print("נפסלת 🥺😓😭")

            # response = requests.delete(f"{basic_url}logout")
            # print(response.status_code)

        elif number == 3:  # הצגת היסטוריית המשחקים
            print(f'{use.numPlay} מספר המשחקים הוא ')
            print('המילים שהופיעו הן:')
            for i in use.strAppear:
                print(i + ' ,')
            print(f'{use.numWin} מספר הנצחונות הוא ')

        elif number == 4:  # יציאה מהלולאה
            print("תודה שהשתמשת במשחק שלנו! להתראות.")
            break  # יציאה מהלולאה הראשית

        else:
            print("בחירה לא חוקית, נסה שוב.")  # אם הקלט לא חוקי

    except ValueError:
        print("אנא הכנס מספר תקין.")  # אם הקלט לא מספר
# response = session.get(f"{basic_url}say_hello/Yasmin")
# if response.status_code == 200:  # האם הבקשה הצליחה?
#     print(response.text)  # הצגת המידע שנשלח מהשרת
# else:
#     print(f"Error. Status code: {response.status_code}")
# print(response.status_code, response.reason, ":", response.text[response.text.index('<p>') + 3:-5])
# #
# response = session.post(f"{basic_url}say_hello/", json={"obj": 'name'})
# print(f"Error {response.status_code}: {response.text}")

# print(response.status_code)
# print(response.status_code, response.reason, ":", response.text[response.text.index('<p>') + 3:-5])
#
# # עוגיות
# cookie_content = {'user_name': 'Yasmin Reuven'}
# response = session.post(f'{basic_url}set_cookie', json=cookie_content)
# print(response.text)  # העוגייה תקפה ל-10 שניות
#
# # # בקשה לקבלת העוגיות
# cookies = response.cookies.get_dict()  # חילוץ העוגיות מהבקשה הקודמת
# print(f"Cookie: {cookies}")
# response = session.get(f'{basic_url}get_cookie')  # , cookies=cookies
# print(response.text)
#
# # המתנה של 10 שניות כדי לראות שהעוגיה נמחקה
# # time.sleep(10)
# # אפשר גם למחוק את העוגייה
# response = session.delete(f"{basic_url}logout_cookie")
# print(response.text)
#
# # ניסיון לגשת לעוגייה
# response = session.get(f'{basic_url}get_cookie')
# print(response.text)

# גישה ל-API חיצוני
# url = "https://meowfacts.herokuapp.com/"

# שליחת בקשה
# response = requests.get(url)
#
# # בדיקה אם הבקשה הצליחה
# if response.status_code == 200:
#     data = response.json()  # המרת התשובה ל-JSON
#     print(f"Fun fact about cats: {data['data'][0]}")
# else:
#     print(f"Failed to fetch data. Status code: {response.status_code}")
