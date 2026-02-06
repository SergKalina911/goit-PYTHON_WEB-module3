""" Спільна пам'ять

Спільна пам'ять підтримується не всіма операційними системами та може бути 
заборонена політикою безпеки.

Щоб створити область спільної пам'яті, потрібно вказати ОС, скільки пам'яті 
потрібно виділити. Для обчислення обсягу пам'яті обов'язково потрібно вказати 
тип даних, який буде використовуватись, та кількість елементів для складних типів. 
Крім того, механізми обмеження доступу до спільного ресурсу також потрібно 
забезпечити самостійно, інакше дані можна зіпсувати при спробі одночасного доступу 
для зміни із різних процесів.

У наступному прикладі ми скористалися механізмом спільної пам'яті Value. Тип даних 
було обрано десятковий ('d'). Докладніше про доступні типи та їх назви можна дізнатися 
з документації.
https://docs.python.org/3.8/library/ctypes.html#fundamental-data-types"""

from multiprocessing import Process, Value, RLock, current_process
from time import sleep
import logging
import sys

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def worker(val: Value):
    """ Фукція-робітник, яка збільшує значення у спільній пам'яті на 1. """
    logger.debug('Started:%s', current_process().name)
    sleep(1)
    # Блокування доступу до спільної пам'яті під час зміни значення
    with val.get_lock():
        val.value += 1
    logger.debug('Done:%s ',current_process().name)
    # Преривання процесу завершенням з кодом 0 (успішне завершення)
    sys.exit(0)


if __name__ == '__main__':
# Створення об'єкта спільної пам'яті з блокуванням доступу до неї RLock (реентерабельна блокування)
    lock = RLock()
    # Створення спільної пам'яті для зберігання одного десяткового числа
    value = Value('d', 0, lock=lock)
    # Створення двох процесів, які будуть працювати з однією спільною пам'яттю
    pr1 = Process(target=worker, args=(value, ))
    pr1.start()
    pr2 = Process(target=worker, args=(value, ))
    pr2.start()
# Очікування завершення процесів
    pr1.join()
    pr2.join()
# Виведення значення зі спільної пам'яті
    print(value.value)  # 2.0

# Виведення
# Started Process-1
# Started Process-2
# Done Process-1
# Done Process-2
# 2.0
