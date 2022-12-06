import datetime
import time
import telebot
import pymysql

def upd_send(id):
    # update признака отправки сообщения
    with connect:
        sql_update_query = """update bot_db.reminder set sent = 1 where id = (%s)"""
        val = id
        cur.execute(sql_update_query, val)
    # print("Record Updated successfully ")


def send_message(token, reply_to_msg_id, chat_id,id):
    bot = telebot.TeleBot(token)
    bot.send_message(chat_id, "Напоминаю", reply_to_message_id=reply_to_msg_id)
    upd_send(id)


def alarm(now_hour, now_minutes, connect, cur):
    with connect:
        sql = "select reply_to_msg_id, user_id, TOKEN, chat_id, id, hours, minutes from bot_db.reminder where sent != 1 and hours = (%s) and minutes = (%s)"
        val = (
            now_hour,
            now_minutes

        )
    count = cur.execute(sql, val)

    myresult = cur.fetchall()
    # print(myresult)


    #
    for row in myresult:
        # reply_to_msg_id = row[0],
        # user_id = row[1],
        # TOKEN = row[2],
        # chat_id = row[3],
        # id = row[4],
        # hours = row[5],
        # minutes = row [6]

        send_message(row[2], row[0], row[3], row[4])

    # for x in myresult:
    #     print(x)

while True:
    now = datetime.datetime.now()
    now_hour = int(now.hour) + 3;
    now_minutes = int(now.minute);
    #connect = pymysql.connect('localhost', 'root', 'root', 'bot_db')
    connect = pymysql.connect('localhost', 'andreyvls', 'RB26dett!', 'bot_db')
    cur = connect.cursor()

    alarm(now_hour, now_minutes, connect, cur)
    # print("sleep  " + str(now))
    time.sleep(30);



# update telebot set sent = 1