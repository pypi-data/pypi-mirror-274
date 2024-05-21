import re
from datetime import datetime
from typing import Optional
from divinegift import logger

from functools import wraps


class Timer:
    def __init__(self, logger_: Optional[logger.Logger] = None):
        self._st = datetime.now()
        self._sp: Optional[datetime] = None
        self.desc: Optional[str] = None
        self.logger = logger_ if logger_ else logger.Logger()

    def start(self, desc: Optional[str] = None):
        """
        :param desc: description which will be printed before time
        :return:
        """
        self._st = datetime.now()
        self.desc = desc

    def stop(self, format_: Optional[str] = None, print_: bool = True):
        """
        :param format_: format, maybe None, 's' - sec, 'm' - min, 'h' - hours
        :param print_: log it by logger or just print
        :return:
        """
        def pr(diff_, format_):
            if format_:
                diff__ = '{:0.5f}'.format(diff_)
            else:
                diff__ = diff_
            str_ = f'{f"[{self.desc}] " if self.desc else ""}{diff__} {format_}'
            if print_:
                print(str_)
            else:
                self.logger.log_info(str_)

        def pr2(diff_, format_):
            if 'h' in format_.lower() or 'm' in format_.lower():
                hours = int(diff_ / 3600)
                minutes = int(diff_ / 60)
                seconds = int(diff_ % 3600)
                str_ = f'{f"[{self.desc}] " if self.desc else ""}{hours:02}:{minutes:02}:{seconds:02}'
            # elif 'm' in format_.lower():
            #     minutes = int(diff_ / 60)
            #     seconds = int(diff_ % 60)
            #     str_ = f'{f"[{self.desc}] " if self.desc else ""}{minutes:02}:{seconds:02}'
            else:
                str_ = f'{f"[{self.desc}] " if self.desc else ""}{diff_:02} sec'
            if print_:
                print(str_)
            else:
                self.logger.log_info(str_)

        self._sp = datetime.now()
        diff = self._sp - self._st
        if not format_:
            pr(diff, '')
        elif format_ == 's':
            pr(diff.total_seconds(), 'sec')
        elif format_ == 'm':
            s = diff.total_seconds()
            m = s / 60
            if m < 0.01:
                pr(s, 'sec')
            else:
                pr(m, 'min')
        elif format_ == 'h':
            s = diff.total_seconds()
            m = s / 60
            h = m / 60
            if h < 0.01:
                if m < 0.01:
                    pr(s, 'sec')
                else:
                    pr(m, 'min')
            else:
                pr(h, 'hr')
        elif re.search(r'([Hh]{1,2}:)?([Mm]{1,2}:)?[Ss]{1,2}', format_):
            pr2(diff.total_seconds(), format_)


def exec_time(_func=None, *, format_: Optional[str] = None, print_: bool = True, desc: Optional[str] = None):
    """
    Decorator which shows execution time
    :param _func: Decorated function
    :param format_: format, maybe None, 's' - sec, 'm' - min, 'h' - hours
    :param print_: log it by logger or just print
    :param desc: description which will be printed before time
    """

    def _exec_time(func_):
        t = Timer()

        @wraps(func_)
        def wrapper(*args, **kwargs):
            t.start(desc)
            res = func_(*args, **kwargs)
            t.stop(format_, print_)
            return res
        return wrapper

    if _func:
        return _exec_time(_func)

    return _exec_time


if __name__ == '__main__':
    t = Timer()
    t.stop(format_='s', print_=True)

    @exec_time
    def foo():
        print('foo')

    @exec_time(format_='h', print_=True, desc='Test bar')
    def bar(str_):
        from time import sleep
        sleep(10)
        print(str_)


    @exec_time(format_='mm:ss', print_=True, desc='Test bar')
    def bar2(str_):
        from time import sleep
        sleep(10)
        print(str_)

    foo()
    bar('var')
    bar2('var2')
