import sqlite3
import datetime
import requests
import time
import telebot

import keyboards
import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


def name_response(first_name):
    """Generates a response, depends on first name."""

    if first_name is None:
        keyboard = keyboards.enter_name_keyboard()
        reply_text = config.FIRST_NAME_MESSAGE
    else:
        first_name = first_name.split(' ')[0]
        keyboard = keyboards.confirm_first_name_keyboard(first_name)
        reply_text = f'Ваше имя - *{first_name}*?'

    return reply_text, keyboard


def is_in_database(user_id):
    """Checks if user already in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    users = cursor.execute(f'''SELECT COUNT(id) 
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0][0]
    
    cursor.close()
    database.close()

    return users


def add_user(user_id, user_username):
    """Adds a new user to database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''
        INSERT INTO users (user_id, user_username, history)
        VALUES (?, ?, ?)
        ''', (user_id, user_username, "[]",))
        
    database.commit()
    cursor.close()
    database.close()


def get_message_id(user_id):
    """Gets user's information."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    message_id = cursor.execute(f'''SELECT message_id
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()
    
    cursor.close()
    database.close()

    if message_id:
        message_id = message_id[0][0]

    return message_id


def update_message_id(user_id, message_id):
    '''Updates message's id.'''

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET message_id=?
                    WHERE user_id=?
                    ''', (message_id, user_id,))

    database.commit()
    cursor.close()
    database.close()


def drop_counter():
    """Drops counter to 0."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute('UPDATE users SET counter=0')
        
    database.commit()
    cursor.close()
    database.close()


def get_info(user_id):
    """Gets user's information."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    info = cursor.execute(f'''SELECT history, busy, counter
                            FROM users 
                            WHERE user_id=?
                            ''', (user_id,)).fetchall()[0]
    
    cursor.close()
    database.close()

    return info


def update_counter(user_id, new_counter):
    """Updates counter in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    new_counter += 1

    cursor.execute(f'''UPDATE users
                    SET counter=?
                    WHERE user_id=?
                    ''', (new_counter, user_id,))

    database.commit()
    cursor.close()
    database.close()


def update_history(user_id, new_history):
    """Updates counter in database."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET history=?
                    WHERE user_id=?
                    ''', (new_history, user_id,))

    database.commit()
    cursor.close()
    database.close()


def set_busy(user_id, status):
    """Updates busy status to True."""

    database = sqlite3.connect("db.db")
    cursor = database.cursor()

    cursor.execute(f'''UPDATE users
                    SET busy=?
                    WHERE user_id=?
                    ''', (status, user_id,))

    database.commit()
    cursor.close()
    database.close()


def set_header():
    """Set header for bot list"""

    config.work_sheet.update('A1:E1', [config.LIST_HEADER])


def color_row_yellow():
    """Colors headers on bot list."""

    config.work_sheet.format(f'A1:E1', {"backgroundColor": {"red": 0.84, "green": 0.68, "blue": 0.0}})


def get_empty_row():
    """Finds first empty row on a list."""

    return len(config.work_sheet.col_values(1)) + 1


def application_to_spread(user_id, username, name, phone, row_num):
    """Adds new application to google spread."""

    current_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")
    config.work_sheet.update(f'A{row_num}:E{row_num}',
                             [[user_id, f'@{username}', name, phone, current_time]],
                             )
    

def connect_ai(change_id, sleep_time, question, history, user_id):
    """Connects to AI, handles query."""

    print(str(sleep_time))
    try:
        time.sleep(sleep_time)
    except:
        pass

    headers = {
        'Connection': 'keep-alive',

        'User-Agent': 'python-requests/2.31.0',
        'accept': 'application/json',
        'token': config.AI_TOKEN,
    }

    json_data = {
        'question': question,
        'chat_history': history,
    }

    response = requests.post(config.AI_ENDPOINT, headers=headers, json=json_data)

    try:
        answer = response.json()[0].get('data').get('answer')
        new_history = response.json()[0].get('data').get('chat_history')
    except:
        answer = False
        new_history = False

    if response.status_code == 200 and answer and new_history:
        update_history(user_id, str(new_history))

        for i in range(2, 20):
            answer = answer.replace(f'{i}.', f'\n\n{i}.')

        try:
            bot.delete_message(chat_id=user_id,
                               message_id=change_id,
                               )
            
            bot.send_message(chat_id=user_id,
                            text=answer,
                            reply_markup=keyboards.call_keyboard(),
                            )
        except:
            pass
    
    else:
        try:
            bot.delete_message(chat_id=user_id,
                               message_id=change_id,
                               )
            
            bot.send_message(chat_id=user_id,
                            text=config.ERROR_TEXT,
                            reply_markup=keyboards.manager_keyboard(),
                            parse_mode='Markdown',
                            )
        except:
            pass
        
    
    set_busy(user_id, False)


def drop_counter_loop():
    while True:
        drop_counter()
        time.sleep(config.RENEW_TIME * 60)