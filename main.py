import telebot, sqlite3, random, monobank, json, time,threading, re
from telebot import types
from datetime import datetime
from config import tg, admin, api_mono, link_mono

game=0
sum=0
card=0
tconv1 = lambda x: time.strftime("%Y", time.localtime(x))
tconv2 = lambda x: time.strftime("%m", time.localtime(x))
tconv3 = lambda x: time.strftime("%d", time.localtime(x))

bot=telebot.TeleBot(tg)

connect=sqlite3.connect('users.db')
cursor=connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER,
    balance INTEGER,
    code TEXT
)""")
connect.commit()

@bot.message_handler()
def mes(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute(f'SELECT id FROM users WHERE tg_id={message.chat.id}') 
    if cursor.fetchone() is None:
            code=random_code()
            info=[message.chat.id, 0, code]
            cursor.execute('INSERT INTO users(tg_id, balance, code) VALUES (?, ?, ?);', info)
            connect.commit()
    connect.commit()
    global game 
    if message.text=='/start':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='🎰Игры'
        button2='💰Баланс'
        klava.add(button1,button2)
        bot.send_message(message.chat.id, f'Рады видеть тебя в нашем боте!',reply_markup=klava)
    elif message.text=='🎰Игры':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
        button1='🎯Дартс'
        button2='🏀Баскетбол'
        button3='🎰Слоты'
        button4='🎲Кости'
        button7='🎳Боулинг'
        button5='🏚В меню'
        klava.add(button1,button2,button3,button4,button5,button7)
        bot.send_message(message.chat.id,'Выбери желаемую игру, либо вернись в меню',reply_markup=klava)
    elif message.text=='🎯Дартс' or message.text=='🎲Кости' or message.text=='🎳Боулинг':
        
        if message.text=='🎯Дартс':
            game='🎯'
        elif message.text=='🎲Кости':
            game='🎲'
        elif message.text=='🎳Боулинг':
            game='🎳'
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='🙅‍♂️Не хочу играть'
        klava.add(button1)
        val6=bot.send_message(message.chat.id,f'На твоем балансе *{balance}* грн. При победе - ты получишь х5 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(val6,val6_f)
        
    elif message.text=='🏀Баскетбол':
        game='🏀'
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='🙅‍♂️Не хочу играть'
        klava.add(button1)
        val5=bot.send_message(message.chat.id,f'На твоем балансе *{balance}* грн. При победе - ты получишь х2 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(val5,val5_f)

    elif message.text=='🎰Слоты':
        game='🎰'
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='🙅‍♂️Не хочу играть'
        klava.add(button1)
        val64=bot.send_message(message.chat.id,f'На твоем балансе *{balance}* грн. При победе - ты получишь х10 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
        bot.register_next_step_handler(val64,val64_f)

    elif message.text=='💰Баланс' or message.text=='◀️Назад':
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()


        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='Пополнить'
        button3='Вывести'
        button2='🏚В меню'        
        klava.add(button1,button2,button3)
        bot.send_message(message.chat.id,f'Ваш баланс *{balance} грн.*',reply_markup=klava,parse_mode='Markdown')
    elif message.text=='Вывести':
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='◀️Назад'
        klava.add(button1)
        pay=bot.send_message(message.chat.id, f'Ваш баланс - *{balance}*. Укажи сумму, которую хочешь вывести',parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(pay,pay_f)
    elif message.text=='Пополнить':
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT code FROM users WHERE tg_id={message.chat.id}')
        code=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='◀️Назад'
        klava.add(button1)
        bot.send_message(message.chat.id, f'Для поповнення балансу: \n1. Перейди за посиланням {link_mono}\n2. У коментарі вкажи `{code}`\n3. У сумі вкажи ту, на яку хочеш поповнити баланс. Чекай надходження коштів протягом 2 хвилин',parse_mode='Markdown',reply_markup=klava)
    elif message.text=='🏚В меню':
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='🎰Игры'
        button2='💰Баланс'
        klava.add(button1,button2)
        bot.send_message(message.chat.id, f'Рады видеть тебя в нашем боте!',reply_markup=klava)
    else:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='🎰Игры'
        button2='💰Баланс'
        klava.add(button1,button2)
        bot.send_message(message.chat.id, f'Рады видеть тебя в нашем боте!',reply_markup=klava)


def pay_f(message):
    connect=sqlite3.connect('users.db')
    cursor=connect.cursor()
    cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
    balance=cursor.fetchall()[0][0]
    connect.commit()
    if message.text is None:
        bot.send_message(message.chat.id,'/start')
    else:
        if (message.text).isnumeric():
            if int(message.text)<(balance+1):
                global sum
                sum=message.text
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='◀️Назад'
                klava.add(button1)
                paycard=bot.send_message(message.chat.id, f'Укажите номер карты, на который хотите сделать вывод средств (Формат - 1111222233334444)',parse_mode='Markdown',reply_markup=klava)
                bot.register_next_step_handler(paycard,paycard_f)
            else:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='◀️Назад'
                klava.add(button1)
                pay=bot.send_message(message.chat.id, f'Ваш баланс - *{balance}*. Укажи сумму, которую хочешь вывести',parse_mode='Markdown',reply_markup=klava)
                bot.register_next_step_handler(pay,pay_f)

        elif message.text=='◀️Назад':
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='Пополнить'
            button3='Вывести'
            button2='🏚В меню'        
            klava.add(button1,button2,button3)
            bot.send_message(message.chat.id,f'Ваш баланс *{balance} грн.*',reply_markup=klava,parse_mode='Markdown')
        else:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='◀️Назад'
            klava.add(button1)
            pay=bot.send_message(message.chat.id, f'Ваш баланс - *{balance}*. Укажи сумму, которую хочешь вывести',parse_mode='Markdown',reply_markup=klava)
            bot.register_next_step_handler(pay,pay_f)

def paycard_f(message):
    
    if message.text is None:
        bot.send_message(message.chat.id,'/start')
    else:
        if (message.text).isnumeric():
            r=re.search(r'\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d',message.text)
            print(r)
            if r is None:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='◀️Назад'
                klava.add(button1)
                paycard=bot.send_message(message.chat.id, f'Укажите номер карты, на который хотите сделать вывод средств (Формат - 1111222233334444)',parse_mode='Markdown',reply_markup=klava)
                bot.register_next_step_handler(paycard,paycard_f)
            else:
                r=re.search(r'\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d',message.text)
                print(r)
                if r is None:
                    global sum
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button1='✅Все верно'
                    button2='❌Отменить вывод'
                    klava.add(button1,button2)
                    global card
                    card=message.text
                    text=f'Сумма: `{sum} грн.`\nКарта: `{message.text}`\n\nВсе верно?'
                    payans=bot.send_message(message.chat.id,text,parse_mode='Markdown',reply_markup=klava)
                    bot.register_next_step_handler(payans,payans_f)
                else:
                    klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button1='◀️Назад'
                    klava.add(button1)
                    paycard=bot.send_message(message.chat.id, f'Укажите номер карты, на который хотите сделать вывод средств (Формат - 1111222233334444)',parse_mode='Markdown',reply_markup=klava)
                    bot.register_next_step_handler(paycard,paycard_f)
            

        elif message.text=='◀️Назад':
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='Пополнить'
            button3='Вывести'
            button2='🏚В меню'        
            klava.add(button1,button2,button3)
            bot.send_message(message.chat.id,f'Ваш баланс *{balance} грн.*',reply_markup=klava,parse_mode='Markdown')
        else:
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='◀️Назад'
            klava.add(button1)
            paycard=bot.send_message(message.chat.id, f'Укажите номер карты, на который хотите сделать вывод средств (Формат - 1111222233334444)',parse_mode='Markdown',reply_markup=klava)
            bot.register_next_step_handler(paycard,paycard_f)

def payans_f(message):
    global card, sum
    if message.text=='✅Все верно':
        bot.send_message(admin,f'Запрос на вывод средств\n\nСумма: `{sum} грн.`\nКарта: `{card}`\nId: `{message.chat.id}`',parse_mode='Markdown')
        bot.send_message(message.chat.id,'Запрос был отправлен администрации!')
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (int(balance)-int(sum), message.chat.id))
        connect.commit()
        
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='Пополнить'
        button3='Вывести'
        button2='🏚В меню'        
        klava.add(button1,button2,button3)
        bot.send_message(message.chat.id,f'Ваш баланс *{balance} грн.*',reply_markup=klava,parse_mode='Markdown')
    elif message.text=='❌Отменить вывод':
        connect=sqlite3.connect('users.db')
        cursor=connect.cursor()
        cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
        balance=cursor.fetchall()[0][0]
        connect.commit()
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='Пополнить'
        button3='Вывести'
        button2='🏚В меню'        
        klava.add(button1,button2,button3)
        bot.send_message(message.chat.id,f'Ваш баланс *{balance} грн.*',reply_markup=klava,parse_mode='Markdown')
    else:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1='✅Все верно'
        button2='❌Отменить вывод'
        klava.add(button1,button2)
        text=f'Сумма: `{sum} грн.`\nКарта: `{card}`\n\nВсе верно?'
        payans=bot.send_message(message.chat.id,text,parse_mode='Markdown',reply_markup=klava)
        bot.register_next_step_handler(payans,payans_f)


def val64_f(message):
    global game
    
    if message.text is None:
        bot.send_message(message.chat.id,'/start')
    else:
        if message.text=='🙅‍♂️Не хочу играть':
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🎰Игры'
            button2='💰Баланс'
            klava.add(button1,button2)
            bot.send_message(message.chat.id, f'Рады видеть тебя в нашем боте!',reply_markup=klava)
        elif (message.text).isnumeric():
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            if int(message.text)<(balance+1) and int(message.text)>0:
                klava=types.ReplyKeyboardRemove()
                sent=bot.send_dice(message.chat.id,game,reply_markup=klava)
                if game=='🎰':
                    time.sleep(3)
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='✅Сыграю еще'
                button2='🎮Сменить игру'
                klava.add(button1,button2)
                print(sent.dice.value)
                if sent.dice.value==1 or sent.dice.value == 22 or sent.dice.value == 43 or sent.dice.value == 64:
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
                    balance=cursor.fetchall()[0][0]
                    newbalance=balance+int(message.text) * 4
                    cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (newbalance, message.chat.id))
                    connect.commit()
                    ewe=bot.send_message(message.chat.id,f'Поздравляю, вы выиграли *{int(message.text) * 10} грн.* Баланс - *{newbalance} грн.*\nХотите сыграть еще раз, или выберите другую игру?',reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ewe,ewe_f)
                else:
                    
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT balance FROM users WHERE  tg_id = {message.chat.id}')
                    balance=cursor.fetchall()[0][0]
                    newbalance=balance-int(message.text)
                    cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (newbalance, message.chat.id))
                    connect.commit()
                    ewe=bot.send_message(message.chat.id,f'К сожалению, вы проиграли *{int(message.text)} грн.* Оставшийся баланс - *{newbalance} грн.*\nХотите сыграть еще раз, или выберите другую игру?',parse_mode='Markdown',reply_markup=klava)
                    bot.register_next_step_handler(ewe,ewe_f)

            else:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='🙅‍♂️Не хочу играть'
                klava.add(button1)
                val6=bot.send_message(message.chat.id,f'Твоя ставка *{message.text} грн.* превышает твой баланс *{balance} грн.*. Введи подходящую сумму',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(val6,val6_f)
        else:
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🙅‍♂️Не хочу играть'
            klava.add(button1)
            val64=bot.send_message(message.chat.id,f'На твоем балансе *{balance} грн.* грн. При победе - ты получишь х10 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(val64,val64_f)
 
        
def val5_f(message):
    global game
    
    if message.text is None:
        bot.send_message(message.chat.id,'/start')
    else:
        if message.text=='🙅‍♂️Не хочу играть':
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🎰Игры'
            button2='💰Баланс'
            klava.add(button1,button2)
            bot.send_message(message.chat.id, f'Рады видеть тебя в нашем боте!',reply_markup=klava)
        elif (message.text).isnumeric():
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            if int(message.text)<(balance+1) and int(message.text)>0:
                klava=types.ReplyKeyboardRemove()
                sent=bot.send_dice(message.chat.id,game,reply_markup=klava)
                if game=='🏀':
                    time.sleep(6)
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='✅Сыграю еще'
                button2='🎮Сменить игру'
                klava.add(button1,button2)
                print(sent.dice.value)
                if sent.dice.value>3:
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
                    balance=cursor.fetchall()[0][0]
                    newbalance=balance+int(message.text) * 4
                    cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (newbalance, message.chat.id))
                    connect.commit()
                    ewe=bot.send_message(message.chat.id,f'Поздравляю, вы выиграли *{int(message.text) * 2} грн.* Баланс - *{newbalance} грн.*\nХотите сыграть еще раз, или выберите другую игру?',reply_markup=klava,parse_mode='Markdown')
                    bot.register_next_step_handler(ewe,ewe_f)
                else:
                    
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT balance FROM users WHERE  tg_id = {message.chat.id}')
                    balance=cursor.fetchall()[0][0]
                    newbalance=balance-int(message.text)
                    cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (newbalance, message.chat.id))
                    connect.commit()
                    ewe=bot.send_message(message.chat.id,f'К сожалению, вы проиграли *{int(message.text)} грн.* Оставшийся баланс - *{newbalance} грн.*\nХотите сыграть еще раз, или выберите другую игру?',parse_mode='Markdown',reply_markup=klava)
                    bot.register_next_step_handler(ewe,ewe_f)

            else:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='🙅‍♂️Не хочу играть'
                klava.add(button1)
                val6=bot.send_message(message.chat.id,f'Твоя ставка *{message.text} грн.* превышает твой баланс *{balance} грн.*. Введи подходящую сумму',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(val6,val6_f)
        else:
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🙅‍♂️Не хочу играть'
            klava.add(button1)
            val6=bot.send_message(message.chat.id,f'На твоем балансе *{balance} грн.* грн. При победе - ты получишь х5 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(val6,val6_f)
    
        
def val6_f(message):
    global game
    if message.text is None:
        bot.send_message(message.chat.id,'/start')
    else:
        if message.text=='🙅‍♂️Не хочу играть':
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🎰Игры'
            button2='💰Баланс'
            klava.add(button1,button2)
            bot.send_message(message.chat.id, f'Рады видеть тебя в нашем боте!',reply_markup=klava)
            
        elif (message.text).isnumeric():
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            if int(message.text)<(balance+1) and int(message.text)>0:
                klava=types.ReplyKeyboardRemove()
                sent=bot.send_dice(message.chat.id,game,reply_markup=klava)
                if game=='🎳':
                    time.sleep(4)
                elif game=='🎲':
                    time.sleep(4)
                elif game=='🎯':
                    time.sleep(3)
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='✅Сыграю еще'
                button2='🎮Сменить игру'
                klava.add(button1,button2)
                if sent.dice.value==6:
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
                    balance=cursor.fetchall()[0][0]
                    newbalance=balance+int(message.text) * 5
                    cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (newbalance, message.chat.id))
                    connect.commit()
                    ewe=bot.send_message(message.chat.id,f'Поздравляю, вы выиграли *{int(message.text) * 5}грн.* Баланс - *{newbalance} грн.*\nХотите сыграть еще раз, или выберите другую игру?',reply_markup=klava, parse_mode='Markdown')
                    bot.register_next_step_handler(ewe,ewe_f)
                else:
                    
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT balance FROM users WHERE  tg_id = {message.chat.id}')
                    balance=cursor.fetchall()[0][0]
                    newbalance=balance-int(message.text)
                    cursor.execute(f'UPDATE users SET balance = ? WHERE tg_id = ?', (newbalance, message.chat.id))
                    connect.commit()
                    ewe=bot.send_message(message.chat.id,f'К сожалению, вы проиграли *{int(message.text)} грн.* Оставшийся баланс - *{newbalance} грн.*\nХотите сыграть еще раз, или выберите другую игру?',parse_mode='Markdown',reply_markup=klava)
                    bot.register_next_step_handler(ewe,ewe_f)

            else:
                klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1='🙅‍♂️Не хочу играть'
                klava.add(button1)
                val6=bot.send_message(message.chat.id,f'Твоя ставка *{message.text} грн.* превышает твой баланс *{balance} грн.*. Введи подходящую сумму',reply_markup=klava,parse_mode='Markdown')
                bot.register_next_step_handler(val6,val6_f)
        else:
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🙅‍♂️Не хочу играть'
            klava.add(button1)
            val6=bot.send_message(message.chat.id,f'На твоем балансе *{balance} грн.* грн. При победе - ты получишь х5 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(val6,val6_f)


def ewe_f(message):
    global game
    if message.text=='✅Сыграю еще':
        if game=='🎲' or game=='🎯' or game=='🎳':
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🙅‍♂️Не хочу играть'
            klava.add(button1)
            val6=bot.send_message(message.chat.id,f'На твоем балансе *{balance}* грн. При победе - ты получишь х5 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(val6,val6_f)
        elif game=='🏀' :
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🙅‍♂️Не хочу играть'
            klava.add(button1)
            val5=bot.send_message(message.chat.id,f'На твоем балансе *{balance}* грн. При победе - ты получишь х4 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(val5,val5_f)
        elif game=='🎰' :
            connect=sqlite3.connect('users.db')
            cursor=connect.cursor()
            cursor.execute(f'SELECT balance FROM users WHERE tg_id={message.chat.id}')
            balance=cursor.fetchall()[0][0]
            connect.commit()
            klava=types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1='🙅‍♂️Не хочу играть'
            klava.add(button1)
            val64=bot.send_message(message.chat.id,f'На твоем балансе *{balance}* грн. При победе - ты получишь х10 от ставки. Какую сумму ставишь?',reply_markup=klava,parse_mode='Markdown')
            bot.register_next_step_handler(val64,val64_f)
    else:
        klava=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
        button1='🎯Дартс'
        button2='🏀Баскетбол'
        button3='🎰Слоты'
        button4='🎲Кости'
        button7='🎳Боулинг'
        button5='🏚В меню'
        klava.add(button1,button2,button3,button4,button5,button7)
        bot.send_message(message.chat.id,'Выбери желаемую игру, либо вернись в меню',reply_markup=klava)

def starter():
    while True:
        
        mono = monobank.Client(api_mono)
        now = datetime.now()
        dt1=(datetime(int(now.year), now.month, int(now.day-3)))
        dt2=(datetime(int(now.year), now.month, int(now.day)))
        
        try:
            banka_info=mono.get_statements('x5r0WC4Wm8toDdKemE_4ZtDHnYSKFIs', (dt1), (dt2))
            print((banka_info[0]['id']))
            for i in banka_info:
                connect  = sqlite3.connect('users.db')
                cursor = connect.cursor()
                cursor.execute(f'SELECT COUNT (id) FROM users')
                connect.commit()
                t = list(i.items())
                for i2 in range(cursor.fetchall()[0][0]):
                    connect=sqlite3.connect('users.db')
                    cursor=connect.cursor()
                    cursor.execute(f'SELECT code FROM users WHERE id={i2+1}')
                    code=cursor.fetchall()[0][0]
                    connect.commit()
                    if str(t[3][1]) == str(code):
                        connect=sqlite3.connect('users.db')
                        cursor=connect.cursor()
                        cursor.execute(f'SELECT balance FROM users WHERE id={i2+1}')
                        balance=cursor.fetchall()[0][0]
                        connect.commit()
                        connect  = sqlite3.connect('users.db')
                        cursor = connect.cursor()
                        newbalance = int(balance)+(float(t[6][1])/100)

                        
                        connect=sqlite3.connect('users.db')
                        cursor=connect.cursor()
                        cursor.execute(f'SELECT tg_id FROM users WHERE id={i2+1}')
                        id=cursor.fetchall()[0][0]
                        connect.commit()

                        
                        bot.send_message(id,f'Ваш баланс було поповнено на{float(t[6][1])/100} грн.!')
                        bot.send_message(admin, f'Юзер `{id}` пополнил баланс на {float(t[6][1])/100} грн.!')
                        cursor.execute(f'UPDATE users SET balance = ? WHERE id = ?', (newbalance, i2+1))
                        cursor.execute(f'UPDATE users SET code = ? WHERE id = ?', (random_code(), i2+1))
                        connect.commit()
        except:
            print('error')
        time.sleep(120)

def random_code():
    
    return (random.randint(1,999999999999))

if __name__ == '__main__':
    t2 = threading.Thread(target=starter)
    t2.start()
    bot.polling(none_stop=True)

