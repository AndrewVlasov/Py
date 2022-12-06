import time

import pymysql
import telebot
import datetime


from telebot import types

global token;
# token = '1119149371:AAHaiPLOqbkYOzmGckeO8KhO5WNFiIT35Iw'; #nissmos15
token = '953976898:AAGnzRRg4H6BM3biHaPL1u0e5QVQ1gIFhnU'; #dontdoit
bot = telebot.TeleBot(token)

global connect;
global cur;

def statistics(message, connect, cur):
    with connect:
        sql = "select updated, restarts from bot_db.dontdoit where active = 1 and user_id = user_id"

    count = cur.execute(sql)

    myresult = cur.fetchall()
    print(2)

    for row in myresult:
        updated = row[0],
        restarts = row[1]
        bot.send_message(message.from_user.id, "Количество попыток " + str(row[1]) + ", время последнего старта " + str(row[0]));

def start_timer(message,connect, cur):
    user_id = str(message.from_user.id),
    username = message.from_user.username,
    first_name = message.from_user.first_name,
    last_name = message.from_user.last_name,
    chat_id = str(message.chat.id),
    reply_to_msg_id = str(message.message_id),
    what = message.text,
    active = 1,

    # print (user_id,  username, first_name, last_name, chat_id,reply_to_msg_id, what, active, str(token))

    bot.send_message(message.from_user.id, 'Поздравляю, это первый шаг к отказу от привычки');
    #
    while True:
        try:
            # print("Msg sending...")
            with connect:
                cur = connect.cursor()
                sql = "INSERT INTO bot_db.dontdoit (user_id, username, first_name, last_name, chat_id, reply_to_msg_id, what, active, TOKEN, restarts)" \
                      "VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s)"
                val = (
                    user_id,
                    username,
                    first_name,
                    last_name,
                    chat_id,
                    reply_to_msg_id,
                    what,
                    active,
                    str(token),
                    1
                 )
                cur.execute(sql, val)
                break
        except:
            # print("SQL err. insert. ")
            bot.send_message(user_id, 'Ошибка запуска. Повторите позже')
            break

def stop_timer(user_id, connect, cur):
    while True:
        try:
            print("stop")
            with connect:
                sql_update_query = """update bot_db.dontdoit set active = 0 where user_id = (%s)"""
                val = user_id
                cur.execute(sql_update_query, val)
            bot.send_message(user_id, 'Надеюсь, что ты больше этого не делаешь. Таймер успешно остановлен. Напиши мне, что бы ты хотел еще бросить?');
            bot.send_sticker(user_id, 'CAACAgIAAxkBAALZ4l7FBA59TDxpVJaL1Ny3HoMwLgpLAAIwBAACnNbnCjOy7LRrs9XQGQQ')
            break
        except:
            bot.send_message(user_id, 'Ошибка остановки. Повторите позже')
            break


def restart_timer(user_id, connect, cur):
    while True:
        try:
            print("Restarting")

            with connect:
                sql_update_query = """update bot_db.dontdoit set restarts = restarts+1 where user_id = (%s) and active = 1"""
                val = user_id
                cur.execute(sql_update_query, val)

            bot.send_sticker(user_id, 'CAACAgIAAxkBAALZ4F7FAxa5UFkwHzOsFRNBos4pa3_MAAIqBAACnNbnCgb0edQ-BzqkGQQ');
            bot.send_message(user_id,'Ну это ты зря. Таймер перезапущен', reply_markup=keyboard1)
            break
        except:
            # print("Stop Timer. SQL connection error " + str(datetime.datetime.now()))
            bot.send_message(user_id, 'Ошибка перезапуска. Повторите позже')
            break



def check_acive_set(id, connect, cur):
    while True:
        try:
            cur = connect.cursor()
            print("checking")
            with connect:
                sql = "select count(*) from bot_db.dontdoit where active = 1 and user_id = (%s)"
                val = (
                    id
                )
                count = cur.execute(sql, val)

                count = cur.fetchall()
                for row in count:
                    count = int(row[0])
                    # print(count)
                    return count
                break
        except ValueError:
            print("ValueError")
            break


        except:
            print("Chk active set. SQL connection error "+ str(datetime.datetime.now()))
            time.sleep(10)
            break


keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Сбросить счетчик', 'Остановить счетчик')



@bot.message_handler(content_types=['text'])

def main(message):
    while True:
        try:
            connect = pymysql.connect('localhost', 'andreyvls', 'RB26dett!', 'bot_db')
            # connect = pymysql.connect('localhost', 'root', 'root', 'bot_db')
            cur = connect.cursor()
            print("Connected " + str(connect.open))
            if message.text == '/help':
                bot.send_message(message.from_user.id,
                                 "Напиши мне от чего ты хочешь отказаться. Доступные команды\n /restart перезапустит счетчик времени\n /stop остановит счетчик времени");
            elif message.text == '/stop' or message.text == 'Остановить счетчик':
                stop_timer(message.from_user.id, connect, cur);
            elif message.text == '/stat' or message.text == 'Остановить счетчик':
                statistics(message, connect, cur);
            elif message.text == '/start':
                bot.send_message(message.from_user.id, "Напиши мне от чего ты хочешь отказаться");
            elif message.text == '/restart' or message.text == 'Сбросить счетчик':
                restart_timer(message.from_user.id, connect, cur);
            else:
                count_active = check_acive_set(message.from_user.id, connect, cur);

                # print("count active1 = "  + str(count_active))
                if count_active == None:
                    bot.send_message(message.chat.id, 'Ошибка. Повторите позже')
                elif count_active > 0:
                    bot.send_message(message.chat.id,
                                     'Луше тренировать привычки последовательно. Чтобы добавить новую, остановите таймер у текущей',
                                     reply_markup=keyboard1)
                    bot.send_sticker(message.from_user.id,
                                     'CAACAgIAAxkBAALZ5l7FBbrrgMIj6n7d4PabpfkoaOgXAAI1BAACnNbnCnDLrILjnvVSGQQ');

                else:
                    bot.send_message(message.chat.id, 'Хорошее начало', reply_markup=keyboard1)
                    start_timer(message, connect, cur);
                    bot.send_sticker(message.from_user.id,
                                     'CAACAgIAAxkBAALZ5F7FBGHzdOjW0zbjn3vX3OD8xoc6AAIyBAACnNbnCnkpXhcPESQ_GQQ');
                connect.close()
            break
        except:
            bot.send_message(message.from_user.id, "Ошибка подключения. Повторите позже")
            break




        # print(connect.open)
bot.polling()