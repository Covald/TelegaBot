import requests


class Response_worker:
    def __new__(cls, base_url):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Response_worker, cls).__new__(cls)
        return cls.instance

    def __init__(self, base_url):
        self.base_url = base_url
        print("Менеджер ответов загружен")

    def send_response(self, response_messages):
        for message in response_messages:
            response = {
                'chat_id': message.Chat_id,
                'text': message.text
            }
            response_messages.pop(0)
            requests.post(self.base_url + 'sendMessage', response)
            print('Отправлен ответ - ' + str(response) + "\n")
