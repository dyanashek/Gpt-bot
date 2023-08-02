from telebot import types

import config


def enter_name_keyboard():
    """Makes a reply to a message that asks about the name."""

    return types.ForceReply(input_field_placeholder=f'Введите Ваше имя')


def enter_phone_keyboard():
    """Makes a reply to a message that asks about the phone number."""

    return types.ForceReply(input_field_placeholder=f'Ваш номер телефона')


def confirm_first_name_keyboard(first_name):
    """Generates keyboard with 'confirm name' and self input options."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('✅ Подтвердить', callback_data = f'confirm_{first_name}'))
    keyboard.add(types.InlineKeyboardButton('🖋 Ввести вручную', callback_data = f'enter'))
    keyboard.add(types.InlineKeyboardButton('❌ Отменить', callback_data = f'cancel'))
    return keyboard


def call_keyboard():
    """Keyboard that allows ask for a call."""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(config.ASK_CALL))

    return keyboard

def call_inline_keyboard():
    """Keyboard that allows ask for a call."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(config.ASK_CALL, callback_data='application'))

    return keyboard


def manager_keyboard():
    """Generates keyboard with manager button."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('👨‍💻 Менеджер', url = f'https://t.me/{config.MANAGER_USERNAME}'))

    return keyboard