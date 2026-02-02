""" Потоки Timer
​Екземпляри класу Timer починають працювати з деякою затримкою, яку визначає програміст. 
Крім того, ці потоки можна скасувати будь-якої миті в період затримки. Наприклад, ви передумали 
стартувати певний потік. Тут ми запланували виконання двох потоків, через 0.5 та 0.7 секунд. 
Але потім через 0.6 секунди скасували виконання другого потоку second.cancel()"""

from threading import Timer
import logging
from time import sleep


def example_work():
    """ Функція, яку виконує потік Timer """
    logging.debug('Start!')


if __name__ == '__main__':
    # Налаштування логування
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
# Створення та запуск потоків Timer
    first = Timer(0.5, example_work)
    first.name = 'First thread'
    second = Timer(0.7, example_work)
    second.name = 'Second thread'
    # Запуск потоків
    logging.debug('Start timers')
    first.start()
    second.start()
    # Затримка перед скасуванням другого потоку
    sleep(0.6)
    second.cancel()
# Завершення програми
    logging.debug('End program')

# Отримаємо таке виведення:
# MainThread Start timers
# First thread Start!
# MainThread End program
