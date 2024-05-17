import logging
import re
import paramiko
import os
from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

import psycopg2
from psycopg2 import Error

# Подключаем логирование
logging.basicConfig(

    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
#Креды для подключения к ВМ
TOKEN = os.getenv('TOKEN')
RM_HOST = os.getenv('RM_HOST')
RM_USER = os.getenv('RM_USER')
RM_PASSWORD = os.getenv('RM_PASSWORD')
RM_PORT = os.getenv('RM_PORT')
#Креды для подключения к БД
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_PORT = os.getenv('DB_PORT')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def get_emails(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PASSWORD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_DATABASE)
        cursor = connection.cursor()
        connection.commit()
        cursor.execute("select address from email_addresses;")
        data = cursor.fetchall()
        emailAddress = []  # Создаем список, в который будем записывать email-адреса
        for row in data:
            emailAddress += row

        logging.info(f"EMAIL адреса (Cписок): {emailAddress}")
        stringEmail = ''
        for i in range(len(emailAddress)):
            stringEmail += f'{i + 1}. {emailAddress[i]}\n'
        update.message.reply_text(stringEmail)

    except (Exception, Error) as error:
        logging.info(f"Ошибка при работе с PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_phone_numbers(update: Update, context):
    connection = None
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PASSWORD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_DATABASE)
        cursor = connection.cursor()
        connection.commit()
        cursor.execute("select number from phone_numbers;")
        data = cursor.fetchall()
        number = []  # Создаем список, в который будем записывать email-адреса
        for row in data:
            number += row

        logging.info(f"Номера телефонов (Cписок): {number}")
        stringNumber = ''
        for i in range(len(number)):
            stringNumber += f'{i + 1}. {number[i]}\n'
        update.message.reply_text(stringNumber)

    except (Exception, Error) as error:
        logging.info(f"Ошибка при работе с PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()



def get_repl_logs(update: Update, context):
    #Переделать подключение логов
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('docker logs master_db | grep repl')
    data = stdout.read() + stderr.read()
    data = data.decode('utf-8')
    logging.info(f' Полученные логи: {data}')
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            update.message.reply_text(data[x:x + 4096])
    else:
        update.message.reply_text(data)


def get_release(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('cat /etc/*release')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_uname(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_uptime(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_df(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('df -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
def get_free(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
def get_mpstat(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
def get_w(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
def get_auths(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('last -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)

def get_critical(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('journalctl -p crit -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
def get_ps(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)
def get_ss(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('ss')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    if len(data) > 4096:
        for x in range(0, len(data), 4096):
            update.message.reply_text(data[x:x + 4096])
    else:
        update.message.reply_text(data)
def get_apt_list(update: Update, context):
    user_input = update.message.text
    if user_input == 'yes':
        client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
        stdin, stdout, stderr = client.exec_command('dpkg -l | awk \'{{print $2,$3}}\'')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        if len(data) > 4096:
            for x in range(0, len(data), 4096):
                update.message.reply_text(data[x:x+4096])
        else:
            update.message.reply_text(data)
    else:
        client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
        stdin, stdout, stderr = client.exec_command(f'dpkg -l | grep {user_input} | awk \'{{print $2,$3}}\' ')
        data = stdout.read() + stderr.read()
        client.close()
        data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(data)
    return ConversationHandler.END
def get_services(update: Update, context):
    client.connect(hostname=RM_HOST, username=RM_USER, password=RM_PASSWORD, port=RM_PORT)
    stdin, stdout, stderr = client.exec_command('service --status-all')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(data)



def get_apt_list_command(update: Update, context):
    update.message.reply_text('Введите имя пакета или введите \'yes\' для вывода всех установленных пакетов: ')

    return 'get_apt_list'

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

#Email
Email_list_write_db = []
def write_email(update: Update, context):
    user_input = update.message.text
    if user_input == "Y":
        connection = None
        try:
            connection = psycopg2.connect(user=DB_USER,
                                          password=DB_PASSWORD,
                                          host=DB_HOST,
                                          port=DB_PORT,
                                          database=DB_DATABASE)
            cursor = connection.cursor()
            for i in range(len(Email_list_write_db)):
                logging.info(f"Email write {Email_list_write_db[i]}")
                cursor.execute(f"INSERT INTO email_addresses (address) VALUES ('{Email_list_write_db[i]}');")

            connection.commit()
            logging.info("Email записаны в бд")
            update.message.reply_text("Email записаны в бд")
            cursor.execute("select address from email_addresses;")
            data = cursor.fetchall()
            emailAddress = []  # Создаем список, в который будем записывать email-адреса
            for row in data:
                emailAddress += row

            logging.info(f"EMAIL адреса (Cписок): {emailAddress}")
            stringEmail = ''
            for i in range(len(emailAddress)):
                stringEmail += f'{i + 1}. {emailAddress[i]}\n'
            update.message.reply_text(stringEmail)
        except (Exception, Error) as error:
            logging.info(f"Ошибка при работе с PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()
        return ConversationHandler.END
    else:
        update.message.reply_text("Email не записаны в бд")
        return ConversationHandler.END  # Завершаем работу обработчика диалога

def find_email(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) email

    emailRegex = re.compile(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+)')  #
    emailList = emailRegex.findall(user_input)
    #Записываем найденные email в переменную
    global Email_list_write_db
    Email_list_write_db = emailList
    logging.info(f' Найденные email для записи: {Email_list_write_db}')
    # Ищем Email адреса
    logging.info(f' Найденные email list: {emailList}')
    if not emailList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Email не найдены')
        return ConversationHandler.END  # Завершаем выполнение функции

    emailAddress = ''  # Создаем строку, в которую будем записывать email-адреса
    for i in range(len(emailList)):
        emailAddress += f'{i + 1}. {emailList[i]}\n'  # Записываем очередной email-адреса
    #context.user_data[emailList] = emailList
    update.message.reply_text(emailAddress)# Отправляем сообщение пользователю
    update.message.reply_text('Записать найденные email в БД? (Y/N)')
    return 'write_email'# Переходим к функции записи

def find_email_command(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-ов: ')

    return 'find_email'

#Phone_number
phone_list_write_db = []
def write_phone_number(update: Update, context):
    user_input = update.message.text
    if user_input == "Y":
        connection = None
        try:
            connection = psycopg2.connect(user=DB_USER,
                                          password=DB_PASSWORD,
                                          host=DB_HOST,
                                          port=DB_PORT,
                                          database=DB_DATABASE)
            cursor = connection.cursor()
            for i in range(len(phone_list_write_db)):
                logging.info(f" Найденные номера телефонов {phone_list_write_db[i]}")
                cursor.execute(f"INSERT INTO phone_numbers (number) VALUES ('{phone_list_write_db[i]}');")

            connection.commit()
            logging.info("Номера телефонов записаны в бд")
            update.message.reply_text("Номера телефонов записаны в бд")
            cursor.execute("select number from phone_numbers;")
            data = cursor.fetchall()
            phone_numbers = []  # Создаем список, в который будем записывать email-адреса
            for row in data:
                phone_numbers += row

            logging.info(f"Номера телефонов (Cписок): {phone_numbers}")
            stringPhone = ''
            for i in range(len(phone_numbers)):
                stringPhone += f'{i + 1}. {phone_numbers[i]}\n'
            update.message.reply_text(stringPhone)

        except (Exception, Error) as error:
            logging.info(f"Ошибка при работе с PostgreSQL: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()
        return ConversationHandler.END
    else:
        update.message.reply_text("Номера телефонов не записаны в бд")
        return ConversationHandler.END  # Завершаем работу обработчика диалога


def find_phone_number(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'\+?7[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|\+?7[ -]?\d{10}|8[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|8[ -]?\d{10}')  # формат 8 (000) 000-00-00
    phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов
    global phone_list_write_db
    phone_list_write_db = phoneNumberList
    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return  # Завершаем выполнение функции

    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'  # Записываем очередной номер

    update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
    update.message.reply_text('Записать найденные номера телефонов в базу данных(Y/N)')
    return 'write_phone_number'  #

def find_phone_number_command(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'


def verify_password_command(update: Update, context):
    update.message.reply_text('Введите пароль: ')

    return 'verify_password'

def verify_password(update: Update, context):
    user_input = update.message.text  # Получаем пароль введенный пользователем

    passwordRegex = re.compile(r'(?=.*[0-9])(?=.*[!@#$%^&*().])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*().]{8,}')  #

    passwordList = passwordRegex.findall(user_input)  # Проверяем, удовлетворяет ли пароль требованиям парольной политики
    logging.info(f' Введенный пароль: {passwordList}')
    if not passwordList:  # Если пароль  не удовлетворяет требованиям
        update.message.reply_text(f'Пароль: "{user_input}" не удовлетворяет требованиям парольной политики')
          # Завершаем выполнение функции
    else:
        update.message.reply_text(f'Пароль: "{user_input}" удовлетворяет требованиям парольной политики')
    return ConversationHandler.END  # Завершаем работу обработчика диалога

def main():
    # Создайте программу обновлений и передайте ей токен вашего бота
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    convHandlerFindEmailAddress = ConversationHandler(
        entry_points=[CommandHandler('find_email', find_email_command)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
            'write_email': [MessageHandler(Filters.text & ~Filters.command, write_email)],
        },
        fallbacks=[]
    )

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', find_phone_number_command)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
            'write_phone_number': [MessageHandler(Filters.text & ~Filters.command, write_phone_number)],

        },
        fallbacks=[]
    )

    convHandlerPasswordCheck = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_password_command)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )

    convHandlerGetAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_list_command)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))


    dp.add_handler(convHandlerFindEmailAddress)
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerPasswordCheck)
    dp.add_handler(convHandlerGetAptList)

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
