""" 
                                        Заняття 2: Процеси в Python


                        Пакет multiprocessing

Пакет multiprocessing — це пакет для виконання коду в окремих процесах з інтерфейсом подібним до інтерфейсу пакета 
threading. https://docs.python.org/3/library/multiprocessing.html

Основна причина появи multiprocessing — це GIL (Global Interpreter Lock) і той факт, що threading API не дозволяє 
розпаралелювати CPU-bound завдання. Оскільки в один момент часу завжди виконується код тільки в одному потоці, 
навіть на багатоядерних сучасних процесорах, отримати приріст продуктивності для завдань, пов'язаних з 
інтенсивними обчисленнями, за допомогою threading не вийде.

Щоб виконувати обчислення дійсно паралельно там, де це дозволяє обладнання, в Python використовуються окремі 
процеси. Так, у кожному окремому процесі буде запущено свій інтерпретатор Python зі своїм GIL.

Для використання процесів необхідно імпортувати клас Process модуля multiprocessing. З ним можна працювати 
декількома способами:
1. У процесі створення екземпляра класу Process іменованому аргументу target передати функцію, яка буде виконуватися 
в окремому процесі
2. Реалізувати похідний клас від класу Process та перевизначити метод run

Розглянемо приклад:
"""

from multiprocessing import Process
import logging
from time import sleep

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class MyProcess(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args

    def run(self) -> None:
        logger.debug(self.args)


def example_work(params):
    sleep(0.5)
    logger.debug(params)


if __name__ == '__main__':
    processes = []
    for i in range(3):
        pr = Process(target=example_work, args=(f"Count process function - {i}", ))
        pr.start()
        processes.append(pr)

    for i in range(2):
        pr = MyProcess(args=(f"Count process class - {i}",))
        pr.start()
        processes.append(pr)

    [el.join() for el in processes]
    [print(el.exitcode, end=' ') for el in processes]
    logger.debug('End program')

"""
Виведення буде наступним:

('Count process class - 1',)
('Count process class - 0',)
Count process function - 0
Count process function - 1
Count process function - 2
End program
0 0 0 0 0 

У цьому прикладі ми створили п'ять процесів, у трьох з яких виконали функцію example_work, а у двох — це клас 
MyProcess, який наслідується від класу Process. У процесів є код завершення роботи (0 означає успішне завершення 
роботи у штатному режимі). І після завершення роботи атрибут exitcode містить код завершення. В іншому API 
multiprocessing багато в чому повторює threading.


