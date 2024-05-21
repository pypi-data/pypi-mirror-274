from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Optional

from divinegift import db
from divinegift.errors import DBNotConnectedError


class AimsUtils:
    def __init__(self):
        self.connection: Optional[db.DBClient] = None

    def connect(self, db_conn):
        self.connection = db.DBClient(db_conn)

    def check_connection(self):
        if not self.connection:
            raise DBNotConnectedError(f'Use connect() first!')

    def get_task_code(self, index, rectype, table_scheme):
        """
        Определение задачи по IND (7.4.3 Crew Administration and Training Qualification Codes)
        :param index: Индекс из БД
        :param rectype: 0 - Получить название задачи; 1 - Код задачи тренера; 2 - Код задачи тренируемого
        :param table_scheme: Схема БД
        :return:
        """
        self.check_connection()

        nIND = None
        if 1 <= index <= 41:
            nIND = index
        elif 1 + 127 <= index <= 41 + 127:
            nIND = index - 127

        if nIND:
            d = self.connection.get_data_row(f"""select * from {table_scheme}.TABLES vt
            where vt.RECDESC = 'CREWCODES2'""")
            fields = d.get('fields')

            trainee_code = ''.join([c.decode() if isinstance(c, bytes) else chr(c) for c in fields[nIND + 30 - 1:nIND + 30]])
            trainer_code = ''.join([c.decode() if isinstance(c, bytes) else chr(c) for c in fields[3059 + nIND * 71 - 1:3059 + nIND * 71]])
            task_name = ''.join([c.decode() if isinstance(c, bytes) else chr(c) for c in fields[3000 + nIND * 71 - 1:3000 + nIND * 71 + 58] if c not in (0, 1)])

            if rectype == 0:
                return task_name
            elif rectype == 1:
                return trainer_code
            elif rectype == 2:
                return trainee_code

    @staticmethod
    def dst_rule_to_date(year, month, week_day, week_day_num, minutes):
        """
        Определение даты перевода летнего/зимнего времени (для AIMS-овского формата представления правила)
        :param year: год, для которого необходимо определить дату
        :param month: месяц
        :param week_day: день недели (понедельник - 1, вторник - 2, и тд)
        :param week_day_num: порядковый номер дня недели в месяце (0 - последний, 1 - первый, 2 - второй, и тд)
        :param minutes: количество минут, во сколько осуществляется перевод
        :return: datetime
        """
        step = 0
        first_day = datetime(year, month, 1)
        init_day = first_day - timedelta(days=first_day.weekday()) + week_day - 1

        if init_day < first_day:
            init_day += 7

        res = datetime(1980, 1, 1)
        while init_day < first_day + relativedelta(months=1, days=-1):
            step += 1
            if week_day_num == 0:
                res = init_day
            elif step == week_day_num:
                res = init_day
                break
            init_day += 7
        return res + timedelta(days=minutes // 60 // 24)


if __name__ == '__main__':
    pass
