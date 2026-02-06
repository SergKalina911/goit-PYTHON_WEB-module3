""" Пакет multiprocessing

Пакет multiprocessing — це пакет для виконання коду в окремих процесах з 
інтерфейсом подібним до інтерфейсу пакета threading. 
https://docs.python.org/3/library/multiprocessing.html

Для використання процесів необхідно імпортувати клас Process модуля multiprocessing. 
З ним можна працювати декількома способами:
1. У процесі створення екземпляра класу Process іменованому аргументу target передати 
функцію, яка буде виконуватися в окремому процесі
2. Реалізувати похідний клас від класу Process та перевизначити метод run

У наступному прикладі ми створили п'ять процесів, у трьох з яких виконали функцію 
example_work, а у двох — це клас MyProcess, який наслідується від класу Process. 
У процесів є код завершення роботи (0 означає успішне завершення роботи у штатному 
режимі). І після завершення роботи атрибут exitcode містить код завершення. В іншому API 
multiprocessing багато в чому повторює threading."""

from multiprocessing import Process
import logging
from time import sleep

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class MyProcess(Process):
    """ Похідний клас від Process """
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        """ Ініціалізація процесу """
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args

    def run(self) -> None:
        """ Перевизначений метод run """
        logger.debug(self.args)


def example_work(params):
    """ Функція для виконання в окремому процесі """
    sleep(0.5)
    logger.debug(params)


if __name__ == '__main__':
    # Головний процес
    processes = []
    # Створення процесів з функцією example_work та класом MyProcess
    for i in range(3):
        # Створення процесу
        pr = Process(target=example_work, args=(f"Count process function - {i}", ))
        # Запуск процесу
        pr.start()
        # Додавання процесу до списку
        processes.append(pr)

    for i in range(2):
        # Створення процесу з класом
        pr = MyProcess(args=(f"Count process class - {i}",))
        pr.start()
        processes.append(pr)
    print(processes)
    # Очікування завершення процесів
    [el.join() for el in processes]
    # Виведення кодів завершення процесів
    [print(el.exitcode, end=' ') for el in processes]
    # Завершення головного процесу
    logger.debug('End program')
    print(processes)

# Виведення буде наступним:

# ('Count process class - 1',)
# ('Count process class - 0',)
# Count process function - 0
# Count process function - 1
# Count process function - 2
# End program
# 0 0 0 0 0
