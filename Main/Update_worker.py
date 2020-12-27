import requests

from Message import Message


class Update_worker:
    def __new__(cls, url):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Update_worker, cls).__new__(cls)
        return cls.instance

    def __init__(self, base_url):
        self.base_url = base_url
        print("Менеджер получения апдейтов загружен")

    def get_update(self):
        list_of_updates = []
        response = requests.get(self.base_url + "getUpdates")
        response_json = response.json()
        for num_update in range(len(response_json["result"])):
            list_of_updates.append(response_json['result'][num_update])
        print("Получены обновления - " + str(list_of_updates) + "\n")
        if len(list_of_updates) != 0:
            last_update = list_of_updates[-1]
            num_last_update = last_update["update_id"]
            requests.get(self.base_url + "getUpdates", {'offset': num_last_update + 1})
        return list_of_updates

    def get_messages(self, updates):
        messages = []
        try:
            for update in updates:
                try:
                    current_message = update["message"]
                    chat_id = current_message["chat"]["id"]
                    username = current_message["from"]["username"]
                    message_date = current_message["date"]
                    try:
                        type_of_message = current_message['entities'][0]['type']
                        if type_of_message == 'bot_command':
                            message_text = current_message['text']
                            messages.append(Message(type_of_message, chat_id, message_date, message_text, username))

                    except KeyError:
                        try:
                            type_of_message = 'text'
                            message_text = current_message['text']
                            print(message_text)
                            messages.append(Message(type_of_message, chat_id, message_date, message_text, username))
                        except KeyError:
                            type_of_message = "Exception"
                            message_text = "Incorrect message, pls use /help to get more information"
                            messages.append(Message(type_of_message, chat_id, message_date, message_text, username))
                except KeyError:
                    print("Ошибка запроса!")
            print("Распарсены сообщения в кол-ве: " + str(len(messages)) + "\n")
            return messages
        except NameError:
            return messages
