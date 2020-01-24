import datetime as DT
import time

from DB_worker import DB_worker
from Message import Message
from Response_worker import Response_worker
from Update_worker import Update_worker


class Bot:
    def __new__(cls, url, token):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Bot, cls).__new__(cls)
        return cls.instance

    def __init__(self, url, token):
        self.base_url = url + token + '/'
        self.Update_worker = Update_worker(self.base_url)
        self.DB_worker = DB_worker()
        self.Response_worker = Response_worker(self.base_url)
        print("Инициализация менеджеров прошла успешно!")

    def get_messages(self):
        return self.Update_worker.get_messages(self.Update_worker.get_update())

    def send_response(self, messages):
        self.Response_worker.send_response(messages)

    def start(self):
        flag = True
        response_list = []
        while flag:
            messages = self.get_messages()
            if not messages:
                time.sleep(0.034)
            for message in messages:
                print(["message.type - " + message.Type,
                       "message.text - " + message.text
                       ])
                if message.Type == "bot_command" or message.text[0] == '/':
                    if message.text.startswith("/add"):
                        current_text = message.text[5:]
                        num = current_text[:current_text.find(" ")]
                        category = current_text[current_text.find(' ') + 1:]
                        if len(current_text) != 0 and len(num) != 0 and len(category) != 0 and num.isdigit():
                            self.DB_worker.insert_costs(message.Chat_id, message.date, num, category)
                            response_list.append(Message(
                                "response", message.Chat_id, message.date,
                                f"Сумма {num} добавлена в категорию {category}"
                            ))
                        else:
                            print("Ошибка!! - пустые параметры /add")
                            response_list.append(Message(
                                "response", message.Chat_id, message.date,
                                "Incorrect parameters, write /help to get more information"
                            ))
                    elif message.text.startswith("/see_sum"):
                        try:
                            current_text = message.text[9:]
                            print(current_text)
                            print(current_text[:current_text.find(" ")])
                            message_date_first = DT.datetime.strptime(current_text[:current_text.find(" ")],
                                                                      '%Y-%m-%d').timestamp()
                            message_date_last = DT.datetime.strptime(current_text[current_text.find(' ') + 1:],
                                                                     '%Y-%m-%d').timestamp()
                            DB_return = self.DB_worker.get_sum(message.Chat_id, message_date_first, message_date_last)
                            response_list.append(Message("response", message.Chat_id, message.date,
                                                         f"Your sends from {current_text[:current_text.find(' ')]} to {current_text[current_text.find(' ') + 1:]} is - {DB_return}"))
                        except Exception as err:
                            print(err)
                            response_list.append(Message("response", message.Chat_id, message.date,
                                                         "Incorrect date form, pls write like '/see_sum YY-MM-DD YY-MM-DD' \n" +
                                                         "Or use /help to get more information"))


                    elif message.text.startswith("/add_category"):
                        var = None
                    elif message.text.startswith("/remove_category"):
                        var = None
                    # database.remove_category = message.text[18:len(message.text)]
                    elif message.text.startswith("/categories"):
                        var = None
                    # bot.send_response(message.Chat_id,database.show_categories())
                    elif message.text.startswith("/statistics"):
                        var = None
                    # database.give_statistic =
                    elif message.text.startswith("/help"):
                        response_list.append(
                            Message("response", message.Chat_id, message.date, "Sorry, now /help is't working :("))
                    else:
                        response_list.append(Message("response", message.Chat_id, message.date,
                                                     "Unknown command, please write /help"))

                if message.Type == 'text' and message.text[0] != '/':
                    response_list.append(
                        Message("response", message.Chat_id, message.date, message.text))

                if message.Type == "Exception":
                    response_list.append(
                        Message("response", message.Chat_id, message.date, message.text))
            self.send_response(response_list)
