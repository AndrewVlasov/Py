import time
import telebot
import  datetime
import pymysql


#подключение к телеграмму
global token;
#token = '1119149371:AAHaiPLOqbkYOzmGckeO8KhO5WNFiIT35Iw'; #nissmos15
token = '1244303360:AAGleWCAJiQ5icryXPoLePAhWKPOvLw8Cs4'; #reminder24
bot = telebot.TeleBot(token)


# Отправка статистики

#connect = pymysql.connect('localhost', 'root', 'root', 'bot_db')
connect = pymysql.connect('localhost', 'andreyvls', 'RB26dett!', 'bot_db')
cur = connect.cursor()

def send_statistic(user_id):
    with connect:
        # Всего записей
        count = "select count(*) from bot_db.reminder"
        count_user_today = "select count(distinct user_id) from bot_db.reminder where date(updated) = current_date"
        cur.execute(count)
        myresult = cur.fetchall();
        for row in myresult:
            bot.send_message(user_id, "Всего записей  " + str(row[0]));

        # Записей за сегодня
        count_today = "select count(*) from bot_db.reminder where date(updated) = current_date"
        cur.execute(count_today)
        myresult = cur.fetchall();
        for row in myresult:
            bot.send_message(user_id, "Записей за сегодня  " + str(row[0]));

        # Всего пользователей
        count_user = "select count(distinct user_id) from bot_db.reminder"
        cur.execute(count_user)
        myresult = cur.fetchall();
        for row in myresult:
            bot.send_message(user_id, "Всего пользователей  " + str(row[0]));

        # уникальных пользователей сегодня
        count_user_today = "select count(distinct user_id) from bot_db.reminder where date(updated) = current_date"
        cur.execute(count_user_today)
        myresult = cur.fetchall();
        for row in myresult:
            bot.send_message(user_id, "уникальных пользователей сегодня  " + str(row[0]));




# обрабатываем входящее сообщение (команду)
@bot.message_handler(content_types=['text'])
def start(message):
    # Переменные, которые нужны нам для напоминания
    global message_id;
    global what;
    global chat_id;
    global user_id;
    global first_name;
    global username;
    global last_name;

    if message.text == '/help':
        bot.send_message(message.from_user.id, "Напиши мне что запомнить и во сколько напомнить, я сделаю свою работу");
    elif message.text == '/stat':
        user_id = '235045596';
        send_statistic(user_id); # отправка статистики
    else:
        message_id = str(message.message_id);
        what = message.text;
        chat_id = str(message.chat.id);
        user_id = str(message.from_user.id);
        first_name = message.from_user.first_name;
        username = message.from_user.username;
        last_name = message.from_user.last_name;
        len_what = len(what);
        #print(len_what);

        while len_what < 800:
            #print(len_what);
            bot.send_message(message.from_user.id, 'Напиши часы по московскому времени (интервал от 0 - 23)');
            bot.register_next_step_handler(message, get_hh);  # следующий шаг – функция get_name
            break
        else:
                print("Exception");
                bot.send_message(message.from_user.id,
                                 'Oops! Длина сообщения больше 800 символов. Попробуйте снова...')
                # break
                # breakpoint();



        # print(message_id)


def get_hh(message):
      global hours;
      while True:
          try:
              hours = int(message.text)
              # print("это число")
              bot.send_message(message.from_user.id, 'Напиши минуты во сколько нужно напомнить');
              bot.register_next_step_handler(message, get_mm);
              break
          except ValueError:
              # print("это не число")
              bot.send_message(message.from_user.id, 'Oops!  Часы должы быть представлены числом от 0 до 23. Попробуйте снова...')
              bot.register_next_step_handler(message, get_hh);
              time.sleep(10)
              break

      # print(hours);

def get_mm(message):
        global minutes;
        while True:
            try:
                minutes = int(message.text)
                # print("это число")
                # print(message);
                set_alarm(message);
                done(chat_id, message_id);
                break
            except ValueError:
                # print("это не число")
                bot.send_message(message.from_user.id,
                                 'Oops!  Минуты должы быть представлены числом от 0 до 59. Попробуйте снова...')
                # breakpoint()
                bot.register_next_step_handler(message, get_mm);
                time.sleep(10)
                break
        # print(minutes);



def done(chat_id, reply_to_msg_id):
    bot.send_message(chat_id, "Ура, я запомнил это", reply_to_message_id=reply_to_msg_id)


def set_alarm(message):
        now = datetime.datetime.now()
        today = datetime.date.today();
        month = today.month;
        day = today.day;

        current_time = now.strftime("%H:%M:%S")
        cur_hours = now.hour + 3;  #размещение на сервере
        cur_minutes = now.minute;
        # print("Current Time =", current_time)

        selected_time = str(hours) + ":" + str(minutes);
        # print("Selected time = ", selected_time)
        current_time = str(cur_hours) + ":" + str(cur_minutes);

        bot.send_message(message.from_user.id, "Время напоминания  " + selected_time);
        bot.send_message(message.from_user.id, "Текущее время   " + current_time);

        # print ((str(now.hour) + str(now.minute)) == (str(hours) + str(minutes)));

        #Подключение к БД
        #connect = pymysql.connect('localhost', 'root', 'root', 'bot_db')
        connect = pymysql.connect('localhost', 'andreyvls', 'RB26dett!', 'bot_db')

        # send_message()

        with connect:
            cur = connect.cursor()
            sql = "INSERT INTO bot_db.reminder (TOKEN, reply_to_msg_id, what, date_rem, hours, minutes, user_id, username, first_name, last_name, chat_id, sent, month_rem, day_rem, message)" \
                  "VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                token,
                str(message_id),
                str(what),
                today,
                int(hours),
                int(minutes),
                str(user_id),
                username,
                first_name,
                last_name,
                chat_id,
                0,
                month,
                day,
                str(message)

            )
            cur.execute(sql, val)
           # print(val)

connect.close()

bot.polling()