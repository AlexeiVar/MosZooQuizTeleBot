import smtplib  # Библиотека, чтобы посылать письма
from email.message import EmailMessage  # Чтобы посылать письма с изображениями и в целом их посылать лучше так
import os
from dotenv import load_dotenv
import json

load_dotenv()
# "Словарь" для хранения пользователей
user_list = {}

# Список животных не был задан в условии задания, выбрал на свое усмотрение животных, немного поправив под вопросы
# все животные выбраны с https://moscowzoo.ru/about/guardianship/waiting-guardianship поскольку викторина должна быть
# связана с системой опеки
with open("resources/questions.json", encoding='UTF8') as file:
    questions = json.load(file)


class APIException(Exception):  # Просто класс ошибки
    pass


# Этот класс нужен чтобы множество пользователей могли использовать бота одновременно,
# он хранит свой счетчик для вопросов, свой список животных и хранится по id чата в словаре,
# в настоящей работе бота бы пришлось иногда перезапускать, чтобы очистить словарь пользователей

class User:
    def __init__(self):
        self.counter = 0  # Счетчик на каком вопросе
        # "Словарь" животных, цифра это то сколько балов набрано для него, ответом потом будет тот у кого баллов выше
        # так как это словарь то значения будут одинаковые во всех файлах
        self.points_list = questions['points_list']

    def add_counter(self):
        self.counter += 1

    # Метод для начисления очков животным
    def give_points(self, list_ans):
        for i in range(len(list_ans)):
            i = str(i + 1)
            self.points_list[list_ans[i]] += 1


# Класс для викторины
class Quiz:
    # Получаю вопрос и ответ
    @staticmethod
    def get_question(i):
        i = str(i + 1)
        text = questions[i]['question']
        answers = questions[i]['answers']
        return text, answers


class MailSender:
    def __init__(self):
        self.smtpObj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        self.smtpObj.login(os.getenv('EMAIL'), os.getenv('EMAIL_PASSWORD'))

    def send(self, result, first_name, last_name):
        msg = EmailMessage()
        msg['Subject'] = "Вопрос о программе опеки"
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = os.getenv('CONTACT_EMAIL')
        msg.set_content(f"{first_name} {last_name} получил результат {result} и теперь интересуется в программе опеки "
                        f"и имеет несколько вопросов о программе, вскоре от него должно поступить письмо.")
        with open(f'resources/{result}.jpg', 'rb') as photo:
            img_data = photo.read()
        msg.add_attachment(img_data, maintype="image", subtype="jpeg")
        self.smtpObj.send_message(msg)
        msg.set_content(" ")

    def send_feedback(self, first_name, last_name, feedback):
        msg = EmailMessage()
        msg['subject'] = "Обратная связь о работе бота"
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = os.getenv('CONTACT_EMAIL')
        msg.set_content(f"{first_name} {last_name} посылает обратную связь о работе бота:\n{feedback}")
        self.smtpObj.send_message(msg)
        msg.set_content(" ")
