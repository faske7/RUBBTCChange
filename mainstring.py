import telebot
from telebot import types
from telebot.types import Message
import sqlite3
from decimal import Decimal
import requests
import dbworker
import config
import datetime
from datetime import datetime
from config import qiwiop, token

bot = telebot.TeleBot(token)
user_dict = {}



class User:
    def __init__(self, sum1):
        self.sum1 = sum1
        self.comment = None
        self.trade_id = None
        self.digits = None
        self.qiwi = None
        self.exrub = None
        self.btc = None
        self.amount = None
        self.amo5 = None

@bot.message_handler(commands=['start'])
def welcome_bot(message: Message):
    s = requests.Session()
    s.headers['Authorization'] = qiwiop
    q = s.get('https://api.qiwiop.com/v2/' + '/balance')
    q.json()
    data = q.json()
    ratetele2 = data['data']['rate']['rub_tele2_btc']
    welcome_message = '🤖Бот по обмену RUB >> BTC' + '\n' + '♻️Курс: 1 BTC = ' + str(
        ratetele2) + ' руб.' + '\n' + ' Выберете: ⬇ ⬇ ⬇️️️'
    chat_id = message.chat.id
    bot.send_message(chat_id, welcome_message, reply_markup=keyboard())
    name = chat_id
    user = User(name)
    user_dict[chat_id] = user
    user = user_dict[chat_id]
    data1 = int(chat_id)
    con = sqlite3.connect('./Shop_DB.db')
    cur = con.cursor()
    cur.execute("SELECT Id_Users FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
    fool = str(cur.fetchone())
    cur.close()
    con.close()
    bot.delete_message(chat_id, message.message_id)
    dbworker.set_state(chat_id, config.States.S_START.value)
    if fool == 'None':
        con = sqlite3.connect('./Shop_DB.db')
        cur = con.cursor()
        cur.execute("INSERT INTO Shop_BD VALUES(1, " + str(data1) + " , 0, 0, 0.00000000)")
        con.commit()
        cur.close()
        con.close()
    else:
        pass

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START.value)
def shop(message: Message):
    s = requests.Session()
    s.headers['Authorization'] = qiwiop
    q = s.get('https://api.qiwiop.com/v2/' + '/balance')
    q.json()
    data = q.json()
    ratetele2 = data['data']['rate']['rub_tele2_btc']
    welcome_message = '🤖Бот по обмену RUB >> BTC' + '\n' + '♻️Курс: 1 BTC = ' + str(
        ratetele2) + ' руб.' + '\n' + ' Выберете: ⬇ ⬇ ⬇️️️'
    chat_id = message.chat.id
    markup1 = types.InlineKeyboardMarkup(row_width=1)
    btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
    markup1.add(btn2)
    x = int(message.message_id) - 1
    if message.text == '📈Обменять на Bitcoin📉':
        try:
            dbworker.set_state(chat_id, config.States.S_ENTER_SUM1.value)
            data1 = int(chat_id)
            con = sqlite3.connect('./Shop_DB.db')
            cur = con.cursor()
            cur.execute("SELECT Ballance FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
            ballance = str(cur.fetchone())
            ballance2 = ballance[1:-2]
            cur.close()
            con.close()
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            q = s.get('https://api.qiwiop.com/v2/' + '/balance')
            q.json()
            data = q.json()
            ratetele2 = data['data']['rate']['rub_tele2_btc']
            data8 = (1 / float(ratetele2)) * float(ballance2)
            data9 = Decimal(data8)
            data10 = str(data9)[0:9]
            bot.send_message(chat_id, 'Ваш баланс: ' + str(ballance2) + ' руб. (~' + str(data10) + ' BTC)' + '\n' + 'Введите кол-во рублей для обмена:', reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        except KeyError:
            return
    if message.text == '📲Пополнить баланс через TELE2📲':
        try:
            dbworker.set_state(message.chat.id, config.States.S_ENTER_SUM.value)
            bot.send_message(chat_id, 'Введите сумму пополнения в рублях (min-100р, max-15000р)', reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        except KeyError:
            return
    if message.text == '⬅️ Назад':
        try:
            bot.send_message(chat_id, welcome_message, reply_markup=keyboard())
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        except KeyError:
            return
    if message.text == '💸Вывести на BTC кошелек💸':
        try:
            bot.send_message(chat_id, "Введите адрес BitCoin Кошелька" + "\n" + "Пример: 13zHfcxzEp4dSByFQtGJygVmpWwsePfEyJ", reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            dbworker.set_state(chat_id, config.States.S_ENTER_CARD2.value)
            return
        except KeyError:
            return
    if message.text == '💰Личный кабинет💰':
        try:
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            q = s.get('https://api.qiwiop.com/v2/' + '/balance')
            q.json()
            data = q.json()
            ratetele2 = data['data']['rate']['rub_tele2_btc']
            if ratetele2 == 'None':
                bot.send_message(chat_id, 'Сервис вр️️️еменно недоступен',
                                 reply_markup=keyboard2())
                bot.delete_message(chat_id, message.message_id)
                bot.delete_message(chat_id, x)
            else:
                data1 = int(chat_id)
                con = sqlite3.connect('./Shop_DB.db')
                cur = con.cursor()
                cur.execute("SELECT Ballance FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
                fool = str(cur.fetchone())
                fool2 = fool[1:-2]
                cur.execute("SELECT Ballancebtc FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
                fool1 = str(cur.fetchone())
                fool11 = fool1[1:-2]
                cur.close()
                con.close()
                data8 = (1/float(ratetele2))*float(fool2)
                data9 = Decimal(data8)
                data10 = str(data9)[0:9]
                dbworker.set_state(message.chat.id, config.States.S_START.value)
                bot.send_message(chat_id, '♻️Курс: *1 BTC = '+ str(ratetele2)  + ' руб.*'+'\n'+'💰Ваш рублевый баланс: *' + str(fool2) + ' руб.* (~'+str(data10)+' BTC)'+'\n'+'💳Ваш BTC баланс: *' + str(fool11) + ' BTC*'+'\n'+ 'Выберите:⬇ ⬇ ⬇️️️', reply_markup=keyboard2(), parse_mode="Markdown")
                bot.delete_message(chat_id, message.message_id)
                bot.delete_message(chat_id, x)
                return
        except KeyError:
            return
    if message.text == '👨🏽‍💻Оператор👨🏽‍💻':
        try:
            bot.send_message(chat_id, "связь с оператором @fasbtcbank ", reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        except KeyError:
            return
    else:
        try:
            bot.send_message(chat_id, welcome_message, reply_markup=keyboard())
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        except KeyError:
            return

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_SUM.value)
def send_anyint(message):
    try:
        markup1 = types.InlineKeyboardMarkup(row_width=1)
        btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
        markup1.add(btn2)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Получить номер TELE2', callback_data="payment")
        btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="backpay")
        markup.add(btn1, btn2)
        chat_id = message.chat.id
        sum1 = message.text
        x = int(message.message_id) - 1
        if not sum1.isdigit():
            bot.send_message(chat_id, '‼️Введите корректную сумму‼️', reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        if int(sum1) < 100:
            bot.send_message(chat_id, "‼️min 100‼️", reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        if int(sum1) > 15000:
            bot.send_message(chat_id, "‼️max 15000‼️", reply_markup=markup1)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        else:
            ic = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M')
            q = " " + str(chat_id) + " " + ic + ""
            comment = q
            user = user_dict[chat_id]
            user.comment = comment
            user.amo5 = sum1
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            postjson = {"amount_rub": "", "comment": "", "fiat_type": "", "last4": ""}
            postjson["amount_rub"] = sum1
            postjson["fiat_type"] = "tele2"
            postjson["comment"] = q
            q = s.post('https://api.qiwiop.com/v2/' + '/create_trade', json=postjson)
            con = sqlite3.connect('./Shop_DB.db')
            cur = con.cursor()
            query = "INSERT INTO Shop_Payments VALUES ('"+sum1+"', '"+comment+"', 'Wait for pay', '"+str(chat_id)+"' )"
            cur.execute(query)
            con.commit()
            cur.close()
            con.close()
            bot.send_message(chat_id, 'Переведите '+str(sum1)+' руб. на номер TELE2. Оплачивать можно как угодно (Банки, Терминалы, Балансы сим, итп) . Время на оплату 5мин!!!', reply_markup=markup)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            dbworker.set_state(chat_id, config.States.S_START.value)
            return
    except KeyError:
        return

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CARD2.value)
def send_number_card_2(message):
    try:
        markup11 = types.InlineKeyboardMarkup(row_width=1)
        btn18 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
        markup11.add(btn18)
        chat_id = message.chat.id
        text3 = message.text
        user = user_dict[chat_id]
        user.card1 = text3
        x = int(message.message_id) - 1
        if len(text3) <= 34:
            if len(text3) >= 32:
                data1 = int(chat_id)
                con = sqlite3.connect('./Shop_DB.db')
                cur = con.cursor()
                cur.execute("SELECT Ballancebtc FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
                fool1 = str(cur.fetchone())
                fool11 = fool1[1:-2]
                cur.close()
                con.close()
                user = user_dict[chat_id]
                user.btc = text3
                bot.send_message(chat_id, "Введите кол-во BTC"+ "\n" +" Пример: 0.00145731 "+ "\n" +"Ваш Баланс BTC: "+ str(fool11) +" BTC", reply_markup=markup11)
                bot.delete_message(chat_id, message.message_id)
                bot.delete_message(chat_id, x)
                dbworker.set_state(chat_id, config.States.S_ENTER_CARD3.value)
                return
            else:
                bot.send_message(chat_id, '‼️Введите корректный кошелек‼️', reply_markup=markup11)
                bot.delete_message(chat_id, message.message_id)
                bot.delete_message(chat_id, x)
                return
        else:
            bot.send_message(chat_id, '‼️Введите корректный кошелек‼️', reply_markup=markup11)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
    except KeyError:
        return

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_CARD3.value)
def send_number_card_3(message):
    try:
        markup14 = types.InlineKeyboardMarkup(row_width=1)
        btn17 = types.InlineKeyboardButton(text='✅Согласен(а)', callback_data="withdraw2")
        btn19 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
        markup14.add(btn17, btn19)
        markup11 = types.InlineKeyboardMarkup(row_width=1)
        btn18 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
        markup11.add(btn18)
        markup12 = types.InlineKeyboardMarkup(row_width=1)
        btn17 = types.InlineKeyboardButton(text='✅Согласен(а)', callback_data="withdraw")
        btn19 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
        markup12.add(btn17, btn19)
        chat_id = message.chat.id
        text3 = message.text
        data1 = int(chat_id)
        user = user_dict[chat_id]
        user.amount = text3
        con = sqlite3.connect('./Shop_DB.db')
        cur = con.cursor()
        cur.execute("SELECT Ballancebtc FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
        fool1 = str(cur.fetchone())
        fool21 = fool1[1:-2]
        cur.close()
        con.close()
        x = int(message.message_id) - 1
        if text3.isalpha():
            bot.send_message(chat_id, '‼️Введите корректную сумму‼️', reply_markup=markup11)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        if len(text3) > 11:
            bot.send_message(chat_id, '‼️Введите корректную сумму‼️', reply_markup=markup11)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        if float(user.amount) > float(fool21) - 0.00012:
            bot.delete_message(chat_id, x)
            bot.delete_message(chat_id, message.message_id)
            bot.send_message(chat_id, '‼️Сумма превышает *остаток на счете* + комиссию сети Bitcoin *0,00012*‼️', reply_markup=markup11, parse_mode='Markdown')
            return
        if text3 == 0:
            bot.send_message(chat_id, '‼️Введите корректную сумму‼️', reply_markup=markup11)
            bot.delete_message(chat_id, message.message_id)
            bot.delete_message(chat_id, x)
            return
        else:
            bot.delete_message(chat_id, x)
            bot.delete_message(chat_id, message.message_id)
            bot.send_message(chat_id, 'Перевести: ' + str(text3) + ' btc на кошелек ' + str(user.btc) + ' ?', reply_markup=markup12)
            return
    except KeyError:
        return

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_SUM1.value)
def send_any_int(message):
    try:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='✅Обменять', callback_data="payment44")
        btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="backpay")
        markup.add(btn1, btn2)
        markup1 = types.InlineKeyboardMarkup(row_width=1)
        btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="back")
        markup1.add(btn2)
        chat_id = message.chat.id
        data1 = int(chat_id)
        sum1 = message.text
        con = sqlite3.connect('./Shop_DB.db')
        cur = con.cursor()
        cur.execute("SELECT Ballance FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
        fool = str(cur.fetchone())
        fool2 = fool[1:-2]
        cur.close()
        con.close()
        if not sum1.isdigit():
            x = int(message.message_id)-1
            bot.delete_message(chat_id, x)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id, '‼️Введите корректную сумму‼️', reply_markup=markup1)
            return
        if int(sum1) < 1000:
            x = int(message.message_id)-1
            bot.delete_message(chat_id, x)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id, "‼️min 1000‼️", reply_markup=markup1)
            return
        if int(sum1) > 15000:
            x = int(message.message_id)-1
            bot.delete_message(chat_id, x)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id, "‼️max 15000‼️", reply_markup=markup1)
            return
        if int(sum1) > int(fool2):
            x = int(message.message_id)-1
            bot.delete_message(chat_id, x)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id, "‼️Сумма превышает остаток на балансе‼️", reply_markup=markup1)
            return
        else:
            ic = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M')
            q = " " + str(chat_id) + " " + ic + ""
            comment = q
            user = user_dict[chat_id]
            user.comment = comment
            user.exrub = sum1
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            q = s.get('https://api.qiwiop.com/v2/' + '/balance')
            q.json()
            data = q.json()
            ratetele2 = data['data']['rate']['rub_tele2_btc']
            data8 = (1 / float(ratetele2)) * float(sum1)
            data9 = Decimal(data8)
            data10 = str(data9)[0:9]
            x = int(message.message_id)-1
            bot.delete_message(chat_id, x)
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id, 'При переводе '+str(sum1)+' руб. вы получите ~ ' + str(data10) + ' BTC', reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.S_START.value)
            return
    except KeyError:
        return

@bot.callback_query_handler(func=lambda message: True)
def inline_shop(message):
    try:
        s = requests.Session()
        s.headers['Authorization'] = qiwiop
        q = s.get('https://api.qiwiop.com/v2/' + '/balance')
        q.json()
        data = q.json()
        ratetele2 = data['data']['rate']['rub_tele2_btc']
        welcome_message = '🤖Бот по обмену RUB >> BTC' + '\n' + '♻️Курс: 1 BTC = ' + str(
            ratetele2) + ' руб.' + '\n' + ' Выберете: ⬇ ⬇ ⬇️️️'
        chat_id = message.message.chat.id
        user = user_dict[chat_id]
        data1 = chat_id
        if message.data == 'back':
            dbworker.set_state(chat_id, config.States.S_START.value)
            bot.send_message(chat_id, welcome_message, reply_markup=keyboard())
            bot.delete_message(chat_id, message.message.message_id)
        if message.data == 'payment44':
            con = sqlite3.connect('./Shop_DB.db')
            cur = con.cursor()
            cur.execute("SELECT Ballance FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
            ball = str(cur.fetchone())
            ball2 = ball[1:-2]
            amo3 = int(ball2)-int(user.exrub)
            cur.execute("UPDATE Shop_BD SET Ballance=" + str(amo3) + " WHERE Id_Users2=" + str(data1) + "")
            con.commit()
            cur.execute("SELECT Ballancebtc FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
            ballancebtc = str(cur.fetchone())
            ballancebtc2 = ballancebtc[1:-2]
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            postjson = {"to": "", "from": "", "fiat_type": "", "amount": ""}
            postjson["to"] = "btc"
            postjson["from"] = "rub"
            postjson["fiat_type"] = "tele2"
            postjson["amount"] = user.exrub
            q = s.post('https://api.qiwiop.com/v2/' + '/exchange', json=postjson)
            q.json()
            #print(q.json())
            result = q.json()
            rs = result['result_text']
            am = result['amount']['btc']
            amo6 = float(ballancebtc2)+float(am)
            cur.execute("UPDATE Shop_BD SET Ballancebtc=" + str(amo6) + " WHERE Id_Users2=" + str(data1) + "")
            con.commit()
            cur.close()
            con.close()
            bot.delete_message(chat_id, message.message.message_id)
            bot.send_message(chat_id, " ! " +str(rs)+ " ! ", reply_markup=keyboard())
            dbworker.set_state(chat_id, config.States.S_START.value)
        if message.data == 'withdraw':
            amo = float(user.amount) + 0.000113
            asd = str(user.amount)
            amo2 = Decimal(asd) + Decimal(0.00012)
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            postjson = {"amount": "", "btc_wallet": ""}
            postjson["amount"] = amo
            postjson["btc_wallet"] = user.btc
            q = s.post('https://api.qiwiop.com/v2/' + '/withdraw', json=postjson)
            q.json()
            con = sqlite3.connect('./Shop_DB.db')
            cur = con.cursor()
            cur.execute("SELECT Ballancebtc FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
            fool5 = str(cur.fetchone())
            fool6 = fool5[1:-2]
            amo4 = Decimal(float(fool6)-float(amo2))
            cur.execute("UPDATE Shop_BD SET Ballancebtc=" + str(amo4) + " WHERE Id_Users2=" + str(data1) + "")
            con.commit()
            cur.close()
            con.close()
            bot.send_message(chat_id, " ! 💸" +str(user.amount)+ " (+ коммисия сети Bitcoin 0.00012) btc отправлено на кошелек "+str(user.btc)+"!💸  ", reply_markup=keyboard())
            bot.delete_message(chat_id, message.message.message_id)
            dbworker.set_state(chat_id, config.States.S_START.value)
        if message.data == 'payment':
            q = qiwi_op()
            g = q.get('data')
            if g == None:
                bot.send_message(chat_id, '❌Сервис недоступен' + '\n' + '!' + '\n' + '!' + '\n' + '⬆️⬆️⬆️⬆️️⬆️️', reply_markup=keyboard())
                bot.delete_message(chat_id, message.message.message_id)
                dbworker.set_state(chat_id, config.States.S_START.value)
            else:
                t = len(list(q['data']['trades']))
                trade_ids = [g['trades'][i]['trade_id'] for i in range(t)]
                qiwi_wallets = [g['trades'][i]['qiwi_wallet'] for i in range(t)]
                comments2 = [g['trades'][i]['comment'] for i in range(t)]
                for idx, i in enumerate(comments2):
                    if i == str(user.comment):
                        c = int(trade_ids[idx])
                        b = int(qiwi_wallets[idx])
                        user.trade_id = c
                        bot.send_message(chat_id, 'Переводите ' + str(user.amo5) + ' РУБ на номер TELE2 ' + str(b) + ' Платите через любой удобный способ.', reply_markup=payment2())
                        bot.delete_message(chat_id, message.message.message_id)
        if message.data == 'payment2':
            markup1 = types.InlineKeyboardMarkup(row_width=1)
            btn2 = types.InlineKeyboardButton(text='❌ОТМЕНИТЬ ЗАЯВКУ❌', callback_data="backpay")
            markup1.add(btn2)
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            postjson = {"trade_id": "trade_id"}
            postjson["trade_id"] = user.trade_id
            q = s.post('https://api.qiwiop.com/v2/' + '/update_trade/mark_paid', json=postjson)
            con = sqlite3.connect('./Shop_DB.db')
            cur = con.cursor()
            cur.execute("UPDATE Shop_Payments SET Status='Pending' WHERE id_comment='" + user.comment + "'")
            con.commit()
            cur.close()
            con.close()
            bot.delete_message(chat_id, message.message.message_id)
            bot.send_message(chat_id, '⏱Ожидайте поступления⏱', reply_markup=payment3())
        if message.data == 'payment3':
            s = requests.Session()
            s.headers['Authorization'] = qiwiop
            q = s.get('https://api.qiwiop.com/v2/' + '/trade_info/?trade_id={'+str(user.trade_id)+'}')
            l = q.json()
            g = l['data']['status']
            if g == 'completed':
                sumq = l['data']['amount_rub']
                datachat = int(chat_id)
                con = sqlite3.connect('./Shop_DB.db')
                cur = con.cursor()
                cur.execute('SELECT Ballance FROM Shop_BD WHERE Id_Users2=' + str(datachat) + '')
                bal = str(cur.fetchone())
                newbal = int(bal[1:-2]) + float(sumq)
                cur.execute('UPDATE Shop_BD SET Ballance=' + str(newbal) + ' WHERE Id_Users2=' + str(datachat) + '')
                con.commit()
                cur.close()
                con.close()
                bot.delete_message(chat_id, message.message.message_id)
                bot.send_message(chat_id, '💵💵💵Баланс пополнен!💵💵💵', reply_markup=keyboard())
                dbworker.set_state(chat_id, config.States.S_START.value)
            if g == 'pending':
                bot.delete_message(chat_id, message.message.message_id)
                bot.send_message(chat_id, '⏱Ожидайте поступления⏱', reply_markup=payment3())
        if message.data == 'backpay':
            q = qiwi_op()
            g = q.get('data')
            if g is None:
                bot.delete_message(chat_id, message.message.message_id)
                bot.send_message(chat_id, welcome_message, reply_markup=keyboard())
                dbworker.set_state(chat_id, config.States.S_START.value)

            else:
                t = len(list(g['trades']))
                trade_ids = [g['trades'][i]['trade_id'] for i in range(t)]
                comments2 = [g['trades'][i]['comment'] for i in range(t)]
                for idx, i in enumerate(comments2):
                    if i == str(user.comment):
                        dbworker.set_state(chat_id, config.States.S_START.value)
                        bot.delete_message(chat_id, message.message.message_id)
                        c = int(trade_ids[idx])
                        user.trade_id = c
                        s = requests.Session()
                        s.headers['Authorization'] = qiwiop
                        postjson = {"trade_id": "trade_id"}
                        postjson["trade_id"] = user.trade_id
                        q = s.post('https://api.qiwiop.com/v2/' + '/update_trade/cancel', json=postjson)
                        bot.send_message(chat_id, welcome_message, reply_markup=keyboard())
        #if message.data == 'withdraw2':
            #con = sqlite3.connect('./Shop_DB.db')
            #cur = con.cursor()
            #cur.execute("SELECT Ballancebtc FROM Shop_BD WHERE Id_Users2=" + str(data1) + "")
            #fool5 = str(cur.fetchone())
            #fool6 = fool5[1:-2]
            #amo14 = float(fool6) - 0.00002
            #amo22 = float(fool6) - 0.0001
            #s = requests.Session()
            #s.headers['Authorization'] = qiwiop
            #postjson = {"amount": "", "btc_wallet": ""}
            #postjson["amount"] = amo14
            #postjson["btc_wallet"] = user.btc
            #q = s.post('https://api.qiwiop.com/v2/' + '/withdraw', json=postjson)
            #q.json()
            #amo4 = 0.00000000
            #cur.execute("UPDATE Shop_BD SET Ballancebtc=" + str(amo4) + " WHERE Id_Users2=" + str(data1) + "")
            #con.commit()
            #cur.close()
            #con.close()
            #bot.send_message(chat_id, " ! 💸" +str(amo22)+ " btc отправлено на кошелек "+str(user.btc)+"!💸  ", reply_markup=keyboard())
            #bot.delete_message(chat_id, message.message.message_id)
            #dbworker.set_state(chat_id, config.States.S_START.value)
    except KeyError:
        return

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text='👨🏽‍💻Оператор👨🏽‍💻')
    btn3 = types.KeyboardButton(text='💰Личный кабинет💰')
    markup.add(btn3, btn1)
    return markup

def keyboard2():
    markupCash = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('📲Пополнить баланс через TELE2📲')
    btn2 = types.KeyboardButton('📈Обменять на Bitcoin📉')
    btn3 = types.KeyboardButton('💸Вывести на BTC кошелек💸')
    btn4 = types.KeyboardButton('⬅️ Назад')
    markupCash.add(btn1, btn2, btn3, btn4)
    return markupCash

def keyboard3():
    markupCash2 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    btn3 = types.KeyboardButton('⬅️ Назад')
    markupCash2.add(btn3)
    return markupCash2

def payment():
    payment = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='✅Перевел(а)', callback_data="payment")
    btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="backpay")
    payment.add(btn1, btn2)
    return payment

def payment2():
    payment = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='✅Оплатил(а)', callback_data="payment2")
    btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="backpay")
    payment.add(btn1, btn2)
    return payment

def payment3():
    payment = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='🔄Обновить Баланс🔄', callback_data="payment3")
    btn2 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data="backpay")
    payment.add(btn1, btn2)
    return payment

def qiwi_op():
    s = requests.Session()
    s.headers['Authorization'] = qiwiop
    q = s.get('https://api.qiwiop.com/v2/' + '/list_trades')
    return q.json()

bot.polling(none_stop=True)
