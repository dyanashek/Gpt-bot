import telebot
import threading

import config
import functions
import keyboards
import utils

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

functions.set_header()
functions.color_row_yellow()
threading.Thread(daemon=True, target=functions.drop_counter_loop).start()


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id

    if not functions.is_in_database(user_id):
        user_username = message.from_user.username
        functions.add_user(user_id, user_username)

    bot.send_message(chat_id=message.chat.id,
                     text=config.START_MESSAGE,
                     reply_markup=keyboards.call_inline_keyboard(),
                     parse_mode='Markdown',
                     )
    

@bot.message_handler(commands=['restart'])
def start_message(message):
    functions.update_history(message.from_user.id, '[]')
    functions.set_busy(message.from_user.id, False)
    
    message_id = functions.get_message_id(message.from_user.id)

    try:
        bot.delete_message(chat_id=message.chat.id,
                           message_id=message_id,
                           )
    except:
        pass

    bot.send_message(chat_id=message.chat.id,
                     text='История сообщений успешно очищена, все запросы к серверу отменены.',
                     reply_markup=keyboards.call_keyboard(),
                     )


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text=config.HELP_MESSAGE,
                     reply_markup=keyboards.call_keyboard(),
                     parse_mode='Markdown',
                     )
    

@bot.callback_query_handler(func = lambda call: True)
def callback_query(call):
    """Handles queries from inline keyboards."""

    # getting message's and user's ids
    message_id = call.message.id
    chat_id = call.message.chat.id

    call_data = call.data.split('_')
    query = call_data[0]


    if query == 'enter':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
        bot.send_message(chat_id=chat_id,
                     text=config.FIRST_NAME_MESSAGE,
                     parse_mode='Markdown',
                     reply_markup=keyboards.enter_name_keyboard(),
                     )

    elif query == 'confirm':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
        user_name = call_data[1]
        reply_text = f'Имя: {user_name}\n\n{config.PHONE_MESSAGE}'

        bot.send_message(chat_id=chat_id,
                    text=reply_text,
                    parse_mode='Markdown',
                    reply_markup=keyboards.enter_phone_keyboard(),
                    )
    
    elif query == 'cancel':
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
        bot.send_message(chat_id=chat_id,
                    text='Заявка на звонок отменена.',
                    parse_mode='Markdown',
                    reply_markup=keyboards.call_keyboard(),
                    )
    
    elif query == 'application':
        first_name = call.from_user.first_name
        reply_text, keyboard = functions.name_response(first_name)

        bot.send_message(chat_id=chat_id,
                        text=reply_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown',
                        )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handles message with text type."""

    user_id = message.from_user.id
    chat_id = message.chat.id

    if config.ASK_CALL == message.text:
        first_name = message.from_user.first_name
        reply_text, keyboard = functions.name_response(first_name)

        bot.send_message(chat_id=message.chat.id,
                        text=reply_text,
                        reply_markup=keyboard,
                        parse_mode='Markdown',
                        )
        
    elif (message.reply_to_message is not None) and\
    (str(message.reply_to_message.from_user.id) == config.BOT_ID) and\
    (config.FIRST_NAME_MESSAGE.replace('*', '') == message.reply_to_message.text or\
     config.PHONE_MESSAGE.replace('*', '') in message.reply_to_message.text):
        
        message_id = message.reply_to_message.id

        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass

        if config.FIRST_NAME_MESSAGE.replace('*', '') == message.reply_to_message.text:
            
            reply_text = f'Имя: {message.text}\n\n{config.PHONE_MESSAGE}'

            bot.send_message(chat_id=chat_id,
                     text=reply_text,
                     parse_mode='Markdown',
                     reply_markup=keyboards.enter_phone_keyboard(),
                     )

        elif config.PHONE_MESSAGE.replace('*', '') in message.reply_to_message.text:
            user_name = utils.extract_name(message.reply_to_message.text)
            phone = message.text
            user_username = message.from_user.username

            row_num = functions.get_empty_row()
            functions.application_to_spread(user_id, user_username, user_name, phone, row_num)

            bot.send_message(chat_id=chat_id,
                             text=config.SUCCESS_REQUEST_MESSAGE,
                             reply_markup=keyboards.manager_keyboard(),
                             )
            
    else:
        user_info = functions.get_info(user_id)
        
        is_busy = user_info[1]
        counter = user_info[2]
        
        if is_busy:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message.id)
            except:
                pass

        else:
            functions.set_busy(user_id, True)
            functions.update_counter(user_id, counter)

            history = eval(user_info[0])
            sleep_time = 2 ** (counter + 1 - config.EXPONENT)

            reply_message = bot.send_message(chat_id=chat_id,
                                             text='Подождите, Ваш запрос обрабатывается...',
                                             )
            
            functions.update_message_id(user_id, reply_message.id)

            threading.Thread(daemon=True, 
                            target=functions.connect_ai, 
                            args=(reply_message.id,
                                  sleep_time,
                                  message.text,
                                  history,
                                  user_id,
                                  ),
                            ).start()
            

@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def handle_text(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Отправьте, пожалуйста, текстовое сообщение, чтобы я мог предоставить ответ.',
                     reply_markup=keyboards.call_keyboard(),
                     )


if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass
