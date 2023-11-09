import telebot
from bs4 import BeautifulSoup
import requests
import re


bot = telebot.TeleBot('6477725412:AAEE0L4dOH4hqwU5VbTbq37SqPLFfIG5rHI')
subj = ''
subjects = {
    'русский язык': 'rus',
    'информатика': 'inf',
    'биология': 'bio',
    'химия': 'chem',
    'физика': 'phys'
}

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, напиши мне название предмета(прим. Биология, Информатика)")
        bot.register_next_step_handler(message, define_subj)
    else:
        bot.send_message(message.from_user.id, "Для страта /start")


def define_subj(message):
    key = message.text.lower()

    if key in subjects.keys():
        bot.send_message(message.from_user.id, "Теперь напиши мне номер варианта")
        global subj
        subj = subjects[key]
        bot.register_next_step_handler(message, find_answears)
    else:
        bot.send_message(message.from_user.id, "Похоже, у меня такого предмета\n/start чтобы начать заново")

def find_answears(message):
    try:
        bot.send_message(message.from_user.id, 'Уже решаю!')

        start_url = f'https://{subj}-ege.sdamgia.ru/test?id='
        id_url = int(message.text)
        search_url = f'https://{subj}-ege.sdamgia.ru/problem?id='
        login_url = 'https://ege.sdamgia.ru/newapi/login'
        data = {
            "user": "jakposkyy@gmail.com",
            "password": "Qwerty12345"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }

        # with requests.Session() as se_fr:
        #     se_fr.headers = {
        #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        #     }

        session = requests.Session()
        session.headers = headers
        response = session.post(login_url, json=data)

        with requests.Session() as se:
            se.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            }

        page = session.get(f'{start_url}{str(id_url)}')

        soup = BeautifulSoup(page.content, "html.parser")

        all_tasks = soup.findAll('div', attrs={'id': re.compile('^comments')})

        for task in all_tasks:
            task_id = task['id'].replace("comments", "")

            page_task = se.get(f'{search_url}{task_id}')
            soup_task = BeautifulSoup(page_task.content, "html.parser")

            # print(soup_task)

            solution = soup_task.find('div', attrs={'class': 'answer'})
            answear = \
            str(solution).replace('<div class="answer" style="display:none"><span style="letter-spacing: 2px;">Ответ: ',
                                  "").split("<")[0]
            bot.send_message(message.from_user.id, answear)
        bot.send_message(message.from_user.id, 'Ответы идут по порядку \nДля нового теста жми /start')
    except:
        bot.send_message(message.from_user.id, 'Что-то пошло не так \nДля нового теста жми /start')


bot.polling(none_stop=True, interval=0)