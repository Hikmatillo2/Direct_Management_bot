# coding: utf-8


import datetime
import sys
import time
from PIL import Image
from data import db_session
from data.users import User
from data.banned_users import BannedUser
from data.requests import Request
from scripts.calculator import Calculator
import telebot
import io
from scripts.drawer import Drawer


class Data:
    def __init__(self):
        self.TOKEN = ''
        self.bot = telebot.TeleBot(self.TOKEN)


class SetUp:
    @staticmethod
    def add_user(name: str, id_: int, acces_level: int = 0):
        user = User()
        user.name = name
        user.id = id_
        user.start_session = datetime.datetime.now().strftime('%m/%d/%Y')
        user.acces_level = acces_level
        user.message_counter = 0
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()

    @staticmethod
    def unban_user(id_: int):
        db_sess = db_session.create_session()
        user = db_sess.query(BannedUser).filter(BannedUser.id == id_).first()
        db_sess.delete(user)
        db_sess.commit()

    @staticmethod
    def ban_user(id_: int, name: str):
        user = BannedUser()
        user.id = id_
        user.name = name
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()


class Keyboard(telebot.types.ReplyKeyboardMarkup):
    def __init__(self, resize: bool = True, text: list = None):
        super().__init__()
        self.resize_keyboard = resize
        self.text = text
        self.make_keyboard()

    def make_keyboard(self):
        for text in self.text:
            self.add(telebot.types.KeyboardButton(text))


class DbScripts:
    @staticmethod
    def check(id_: int):
        db_sess = db_session.create_session()
        if str(id_) == str(db_sess.query(User).filter(User.id == id_).first()).split()[0]:
            db_sess.close()
            return True
        return False

    @staticmethod
    def check_banned(id_: int):
        db_sess = db_session.create_session()
        if str(id_) == str(db_sess.query(BannedUser).filter(BannedUser.id == id_).first()).split()[0]:
            return True
        return False

    @staticmethod
    def get_all_id():
        db_sess = db_session.create_session()
        data = (str(_) for _ in db_sess.query(User).all())
        return [''.join(_.split()[0]) for _ in data]

    @staticmethod
    def get_all_users():
        db_sess = db_session.create_session()
        data = (str(_) for _ in db_sess.query(User).all())
        return [' '.join(_.split()[:3]) + ' ' + str(_.split()[-1]) for _ in data]

    @staticmethod
    def get_all_banned_users():
        db_sess = db_session.create_session()
        data = str(db_sess.query(BannedUser).all())
        return [_[1:-1] for _ in data.split(',')]

    @staticmethod
    def get_acces_level_by_id(id_: int):
        db_sess = db_session.create_session()
        acces_level = str(db_sess.query(User).filter(User.id == id_).first()).split()[-1]
        return acces_level

    @staticmethod
    def get_start_session_by_id(id_: int):
        db_sess = db_session.create_session()
        start_session = str(db_sess.query(User).filter(User.id == id_).first()).split()[3]
        return start_session

    @staticmethod
    def get_message_counter_by_id(id_: int):
        db_sess = db_session.create_session()
        message_counter = str(db_sess.query(User).filter(User.id == id_).first()).split()[4]
        return message_counter

    @staticmethod
    def update_message_counter_by_id(id_: int):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id_).first()
        user.message_counter += 1
        db_sess.commit()

    @staticmethod
    def change_acces_level_by_id(id_: int, acces_level: int = 0):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id_).first()
        user.acces_level = acces_level
        db_sess.commit()

    @staticmethod
    def get_code_by_id(id_: int):
        db_sess = db_session.create_session()
        code = str(db_sess.query(User).filter(User.id == id_).first()).split()[-2]
        return code


class RequestsScripts:
    @staticmethod
    def change_clicks(id_: int, clicks: int):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.clicks = clicks
        db_sess.commit()

    @staticmethod
    def change_money(id_: int, money: int):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.money = money
        db_sess.commit()

    @staticmethod
    def change_site(id_: int, site: float):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.site = site
        db_sess.commit()

    @staticmethod
    def change_manager(id_: int, manager: float):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.manager = manager
        db_sess.commit()

    @staticmethod
    def change_traffic(id_: int, traffic: float):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.traffic = traffic
        db_sess.commit()

    @staticmethod
    def change_stgs(id_: int, stgs: bool):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.stgs = stgs
        db_sess.commit()

    @staticmethod
    def restore_defaults(id_: int):
        db_sess = db_session.create_session()
        req = db_sess.query(Request).filter(Request.id == id_).first()
        req.clicks = 0
        req.money = 0
        req.site = 0.03
        req.manager = 0.1
        req.traffic = 0.62
        req.stgs = False
        db_sess.commit()

    @staticmethod
    def get_all(id_: int):
        db_sess = db_session.create_session()
        return str(db_sess.query(Request).filter(Request.id == id_).first()).split()

    @staticmethod
    def add_request(id_: int):
        req = Request()
        req.id = id_
        db_sess = db_session.create_session()
        db_sess.add(req)
        db_sess.commit()


ADMIN_ID = 476893348, 829825582
bot = Data().bot
co = 0
flag = True
SETUP_MODE = False
UNBAN_MODE = False
ANNOUNCE_MODE = False
BAN_MODE = False
CHANGE_ACCES_LEVEL_MODE = False
CALCULATOR_MODE = False

CLICKS = False
MONEY = False
SITE = False
MANAGER = False
TRAFFIC = False


def delete_messages(chat_id: int, message_id: int, iterations: int = 1):
    for _ in range(1, iterations + 1):
        try:
            bot.delete_message(chat_id, message_id - _)
        except Exception:
            pass


@bot.message_handler(commands=['ban'])
def ban(message):
    global ADMIN_ID, BAN_MODE
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Привет, кого забанить? Напиши ID.', reply_markup=Keyboard(True, ['Назад']))
        BAN_MODE = True
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['shutdown'])
def get_all(message):
    global ADMIN_ID
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Завершение работы...')
        raise Exception('1')
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['getall'])
def get_all(message):
    global ADMIN_ID
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Юзер лист:' + '\n' + '\n'.join(DbScripts.get_all_users()))
        bot.send_message(id_, 'Бан лист:' + '\n' + '\n'.join(DbScripts.get_all_banned_users()))
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['setup'])
def setup(message):
    global ADMIN_ID, SETUP_MODE
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Привет, кого будем добавлять? Напиши имя, ID и уровень доступа. в формате:\n'
                              '{имя}, {ID}, {acces_level}', reply_markup=Keyboard(True, ['Назад']))
        SETUP_MODE = True
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['change_access_level'])
def change_acces_level(message):
    global ADMIN_ID, CHANGE_ACCES_LEVEL_MODE
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Кому меняем access_level? Напиши ID и уровень доступа. в формате:\n'
                              '{ID}, {acces_level}', reply_markup=Keyboard(True, ['Назад']))
        CHANGE_ACCES_LEVEL_MODE = True
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['unban'])
def unban(message):
    global ADMIN_ID, UNBAN_MODE
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Привет, кого разбанить? Напиши ID.', reply_markup=Keyboard(True, ['Назад']))
        UNBAN_MODE = True
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['announce'])
def announce(message):
    global ADMIN_ID, ANNOUNCE_MODE
    id_ = message.chat.id
    if message.chat.id in ADMIN_ID:
        bot.send_message(id_, 'Привет, что напишем?', reply_markup=Keyboard(True, ['Назад']))
        ANNOUNCE_MODE = True
    else:
        bot.send_message(id_, 'К сожалению у вас нет прав Администратора для доступа к данному разделу')


@bot.message_handler(commands=['start'])
def start_message(message):
    id_ = message.chat.id
    global flag

    bot.send_sticker(id_, 'CAACAgIAAxkBAAEEI_diLd85gwqQDLPkqUa9Hc5gei1v6wACaQsAApe62UniP9hNazdftiME')
    bot.send_message(id_, 'Добрый день, <i>{}</i>, проверяю <b>вашу</b> учетную запись в базе данных'
                          '.'.format(message.from_user.first_name), parse_mode='html')

    if DbScripts.check_banned(id_):
        bot.send_message(id_, '{}, к сожалению, вы в бане, я выключась'.format(message.from_user.first_name))
        flag = False

    if flag:
        if DbScripts.check(id_):
            bot.send_message(id_, 'Вы в базе! Добро пожаловать!')
            bot.send_message(id_, 'Выберите команду', reply_markup=InlineKeyboard(2, [['Калькулятор', 'calc'],
                                                                                      ['Coming soon', 'smth']]))
        else:
            bot.send_message(id_, 'К сожалению, Вас нет в базе данных, инициализация нового пользователя...')
            try:
                name = message.from_user.first_name
                if len(name.split()) == 2:
                    SetUp.add_user(name, message.chat.id)
                elif len(name.split()) == 1:
                    SetUp.add_user(name + ' ' + name, message.chat.id)
                RequestsScripts.add_request(id_)
                bot.send_message(id_, 'Инициализация успешна.')
                bot.send_message(message.chat.id, 'Для того, чтобы приобрести доступ к '
                                                  'полному функционалу, оплатите подписку. Для этого в'
                                                  ' комментарии к переводуна карту <b>5469460017185181</b>'
                                                  ' укажите Ваш уникальный код:'
                                                  ' <i>{}</i>'
                                                  ''.format(DbScripts.get_code_by_id(message.chat.id)),
                                 parse_mode='html')
            except Exception as ex:
                bot.send_message(message.chat.id, 'An error occured: {}'.format(str(ex)))


class InlineKeyboard(telebot.types.InlineKeyboardMarkup):
    def __init__(self, width: int = 2, text: list = None):
        super().__init__()
        self.text = text
        if width == 2:
            self.row_width = len(text)
        else:
            self.row_width = width
        self.make_keyboard()

    def make_keyboard(self):
        for text in self.text:
            self.add(telebot.types.InlineKeyboardButton(text[0], callback_data=text[1]))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global SITE, CLICKS, MANAGER, TRAFFIC, MONEY
    if call.data == "calc":
        bot.answer_callback_query(call.id, "Открываю калькулятор")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы находитесь в'
                                                                                                     ' режиме'
                                                                                                     ' калькулятора.'
                                                                                                     ' Введите '
                                                                                                     'количество '
                                                                                                     'кликов',
                              reply_markup=InlineKeyboard(1, [['Тонкая настройка', 'stgs'], ['<- Назад', 'back']]))
        CLICKS = True
    elif call.data == 'stgs':
        print(101)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Вы находитесь в режиме тонкой настройки калькулятора.\n\nВ '
                                   'этом режиме можно настроить'
                                   ' конверсию сайта, эффективность менеджера, трафик.',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back2']]))
        bot.send_message(call.message.chat.id, 'Введите конверсию сайта в процентах, или нажмите на кнопку,'
                                               ' чтобы восстановислось значение по умолчанию. \nПример: 36',
                         reply_markup=Keyboard(True, ['default']))
        CLICKS = False
        SITE = True
    elif call.data == 'back2':
        bot.send_message(call.message.chat.id, 'Попробуем еще раз?', reply_markup=telebot.types.ReplyKeyboardRemove())
        CLICKS = True
        MONEY = False
        SITE = False
        MANAGER = False
        TRAFFIC = False
        RequestsScripts.restore_defaults(call.message.chat.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы находитесь в'
                                                                                                     ' режиме'
                                                                                                     ' калькулятора.'
                                                                                                     ' Введите '
                                                                                                     'количество '
                                                                                                     'кликов',
                              reply_markup=InlineKeyboard(1, [['Тонкая настройка', 'stgs'], ['<- Назад', 'back']]))
    elif call.data == "smth":
        bot.answer_callback_query(call.id, "Данный раздел находится в разработке")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Данный раздел'
                                                                                                     ' находится в'
                                                                                                     ' разработке',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back']]))
    elif call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите команду',
                              reply_markup=InlineKeyboard(2, [['Калькулятор', 'calc'],
                                                              ['Вова, придумай', 'smth']]))


@bot.message_handler(content_types=['text'])
def send_text(message):
    global SETUP_MODE, UNBAN_MODE, BAN_MODE, ANNOUNCE_MODE, CHANGE_ACCES_LEVEL_MODE, \
        flag, ADMIN_ID, CLICKS, SITE, MANAGER, MONEY, TRAFFIC
    if not DbScripts.check(message.chat.id):
        start_message(message)
    if flag:
        DbScripts.update_message_counter_by_id(message.chat.id)
        print('User: {} WROTE: {}'.format(message.from_user.first_name, message.text), message.chat.id)
        if int(DbScripts.get_acces_level_by_id(message.chat.id)) > 0 or message.chat.id in ADMIN_ID:
            if message.text == 'Назад':
                SETUP_MODE = False
                UNBAN_MODE = False
                CHANGE_ACCES_LEVEL_MODE = False
                ANNOUNCE_MODE = False
                BAN_MODE = False

            if SETUP_MODE:
                try:
                    name, id_, acces_level = message.text.split(',')[0], int(message.text.split(',')[1]), int(
                        message.text.split(',')[2])
                    SetUp.add_user(name=name, id_=id_, acces_level=acces_level)
                    bot.send_message(message.chat.id, 'Добавление успешно.')
                except Exception as e_:
                    bot.send_message(message.chat.id, '<i>An error occured</i>: {}'.format(e_), parse_mode='html')
                SETUP_MODE = False

            if UNBAN_MODE:
                try:
                    id_ = int(message.text)
                    SetUp.unban_user(id_=id_)
                    bot.send_message(message.chat.id, 'Удаление из бан листа успешно.')
                except Exception as e_:
                    print(e_)
                    bot.send_message(message.chat.id, '<i>An error occured</i>: {}'.format(e_), parse_mode='html')
                UNBAN_MODE = False

            if BAN_MODE:
                try:
                    data = message.text.split()
                    SetUp.ban_user(id_=data[0], name=data[1])
                    bot.send_message(message.chat.id, 'Добавление в бан лист успешно.')
                except Exception as e_:
                    print(e_)
                    bot.send_message(message.chat.id, '<i>An error occured</i>: {}'.format(e_), parse_mode='html')
                BAN_MODE = False

            if ANNOUNCE_MODE:
                text = message.text
                co_ = 0

                for id__ in DbScripts.get_all_id():
                    print(id__)
                    try:
                        bot.send_message(id__, text)
                    except Exception as e_:
                        print(e_)
                        co_ += 1
                bot.send_message(message.chat.id, 'Сообщение отправлено.')
                bot.send_message(message.chat.id, 'Юзеров, не получивших сообщение: <i>{}</i>.'.format(co),
                                 parse_mode='html')
                ANNOUNCE_MODE = False

            if CHANGE_ACCES_LEVEL_MODE:
                try:
                    id_, acces_level = message.text.split(',')[0], int(message.text.split(',')[1])
                    DbScripts.change_acces_level_by_id(id_, acces_level)
                    bot.send_message(message.chat.id, 'Изменение успешно.')
                except Exception as e_:
                    bot.send_message(message.chat.id, '<i>An error occured</i>: {}'.format(e_), parse_mode='html')
                CHANGE_ACCES_LEVEL_MODE = False

            if CLICKS:
                RequestsScripts.change_clicks(int(message.chat.id), int(message.text))
                bot.send_message(message.chat.id, 'Введите Ваш рекламный бюджет')
                MONEY = True
                CLICKS = False

            elif MONEY:
                try:
                    RequestsScripts.change_money(message.chat.id, int(message.text))
                    bot.send_message(message.chat.id, 'Считаю...', reply_markup=telebot.types.ReplyKeyboardRemove())
                    data = [float(_) for _ in RequestsScripts.get_all(message.chat.id)]
                    calculator = Calculator(int(data[0]), int(data[1]),
                                            site=data[2],
                                            manager=data[3],
                                            traffic=data[4]).compile()
                    bot.send_photo(message.chat.id, photo=Drawer.make_table(calculator))
                except Exception as ex_:
                    print(str(ex_))
                    bot.send_message(message.chat.id, 'Произошла ошибка: <i>{}</i>'.format(str(ex_)), parse_mode='html')
                bot.send_message(message.chat.id, 'Выберите команду',
                                 reply_markup=InlineKeyboard(2, [['Калькулятор', 'calc'],
                                                                 ['Coming soon', 'smth']]))
                CLICKS = False
                MONEY = False
                SITE = False
                MANAGER = False
                TRAFFIC = False
                RequestsScripts.restore_defaults(message.chat.id)

            elif SITE:
                delete_messages(message.chat.id, message.message_id, iterations=1)
                if message.text == 'default':
                    bot.send_message(message.chat.id, 'Конверсия сайта приняла значение по умолчанию')
                else:
                    RequestsScripts.change_site(message.chat.id, int(message.text) / 100)
                    bot.send_message(message.chat.id, f'Конверсия сайта приняла значение: {message.text}%')
                bot.send_message(message.chat.id, 'Введите эффективность менеджера в процентах, или нажмите на кнопку,'
                                                  ' чтобы восстановислось значение по умолчанию. \nПример: 43',
                                 reply_markup=Keyboard(True, ['default']))
                SITE = False
                MANAGER = True

            elif MANAGER:
                delete_messages(message.chat.id, message.message_id, iterations=2)
                if message.text == 'default':
                    bot.send_message(message.chat.id, 'Эффективность менеджера приняла значение по умолчанию')
                else:
                    RequestsScripts.change_manager(message.chat.id, int(message.text) / 100)
                    bot.send_message(message.chat.id, f'Эффективность менеджера  приняла значение: {message.text}%')
                bot.send_message(message.chat.id, 'Введите трафик в процентах, или нажмите на кнопку,'
                                                  ' чтобы восстановислось значение по умолчанию. \nПример: 43',
                                 reply_markup=Keyboard(True, ['default']))
                MANAGER = False
                TRAFFIC = True

            elif TRAFFIC:
                delete_messages(message.chat.id, message.message_id, iterations=2)
                if message.text == 'default':
                    bot.send_message(message.chat.id, 'Трафик принял значение по умолчанию')
                else:
                    RequestsScripts.change_traffic(message.chat.id, int(message.text) / 100)
                    bot.send_message(message.chat.id, f'Трафик принял значение: {message.text}%')
                bot.send_message(message.chat.id, ' Введите '
                                                  'количество '
                                                  'кликов')
                TRAFFIC = False
                CLICKS = True

            else:
                bot.send_message(message.chat.id, 'Используйте кнопки')

        else:
            bot.send_message(message.chat.id, 'Для того, чтобы приобрести доступ к '
                                              'полному функционалу, отправьте Ваш уникальный код:'
                                              ' <i>{}</i> на карту <b>5469460017185181</b>'
                                              ''.format(DbScripts.get_code_by_id(message.chat.id)),
                             parse_mode='html')


if __name__ == '__main__':
    db_session.global_init("db/users.db")
    flag_ = True
    while flag_:
        try:
            bot.polling(none_stop=True, timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(e)
            bot.stop_polling()
            time.sleep(15)
            if str(e) == '1':
                flag_ = False

for i in ADMIN_ID:
    bot.send_message(i, 'Программа завершила свою работу.')
print('Программа завершила свою работу.')
sys.exit()
