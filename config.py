import os
import gspread

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_ID = os.getenv('BOT_ID')
MANAGER_USERNAME = os.getenv('MANAGER_USERNAME')

AI_TOKEN = os.getenv('AI_TOKEN')
AI_ENDPOINT = os.getenv('AI_ENDPOINT')

SPREAD_NAME = os.getenv('SPREAD_NAME')
LIST_NAME = os.getenv('LIST_NAME')

EXPONENT = float(os.getenv('EXPONENT'))
RENEW_TIME = float(os.getenv('RENEW_TIME'))

service_acc = gspread.service_account(filename='service_account.json')
sheet = service_acc.open(SPREAD_NAME)
work_sheet = sheet.worksheet(LIST_NAME)

LIST_HEADER = ['ID', 'USERNAME', 'NAME', 'PHONE', 'DATE']

START_MESSAGE = 'Привет! Я чат-бот, готовый помочь вам сделать заказ на разработку бота.'
START_MESSAGE = 'Привет! Я чат-бот, готовый помочь вам сделать заказ на разработку бота.'

HELP_MESSAGE = '''
                \nКоманды:\
                \n/restart - обнуляет историю сообщений и отменяет текущие запросы к серверу;\
                \n/help - вызывает список доступных команд.\
                '''

FIRST_NAME_MESSAGE = 'В ответ на это сообщение введите Ваше *имя*.'
PHONE_MESSAGE = 'В ответ на это сообщение введите Ваш *номер телефона*.'

ASK_CALL = '📲 Заказать звонок'

SUCCESS_REQUEST_MESSAGE = 'Менеджер свяжется с вами в ближайшее время!\n\nВы можете самостоятельно перейти в диалог с менеджером, воспользовавшись кнопкой ниже.'

ERROR_TEXT = 'Что-то пошло не так, повторите попытку позже. Если проблема носит регулярный характер - воспользуйтесь командой */restart* для сброса истории общения с ботом и отмены запросов к серверу.\n\nВы также можете связаться с нашим менеджером.'
