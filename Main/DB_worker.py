import psycopg2


class DB_worker:

    def __new__(cls, DB_dict=None):
        if DB_dict is None:
            DB_dict = {'HOST': 'localhost',
                       'USERNAME': 'postgres',
                       "USER_PASSWORD": 'postgres',
                       "DB_CHEMA": 'test'}
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB_worker, cls).__new__(cls)
        return cls.instance

    def __init__(self, DB_dict=None):
        if DB_dict is None:
            DB_dict = {'HOST': 'localhost',
                       'USERNAME': 'postgres',
                       "USER_PASSWORD": 'postgres',
                       "DB_CHEMA": 'test'}
        self.CON = psycopg2.connect(user=DB_dict['USERNAME'],
                                    password=DB_dict["USER_PASSWORD"], host=DB_dict['HOST'], port="5432",
                                    database=DB_dict["DB_CHEMA"])
        print("Соединение с БД установлено")

    def get_version(self):
        with self.CON:
            cur = self.CON.cursor()
            cur.execute("SELECT VERSION()")

            version = cur.fetchone()

            return "Database version: {}".format(version[0])

    def insert_costs(self, chat_id, date, num, category):

        with self.CON:
            cur = self.CON.cursor()
            try:
                cur.execute(
                """
                INSERT INTO maintest (chat_id,message_date,summa,category) 
                VALUES (%s,%s,%s,%s)
                """, (chat_id, date, num, category))
                self.CON.commit()
                print("Трата успешно добавлена")
            except Exception:
                self.CON.rollback()

    def get_sum(self, chat_id, message_date_first, message_date_last):
        summa = 0
        with self.CON:
            cur = self.CON.cursor()

            cur.execute("""
            SELECT summa FROM maintest 
            WHERE message_date>=%s and message_date<=%s and chat_id=%s
            """, (message_date_first, message_date_last, chat_id))
            for num in cur:
                summa += num[0]
        return summa
