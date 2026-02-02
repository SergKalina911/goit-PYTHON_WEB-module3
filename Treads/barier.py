""" Бар'єр Barrier

​Останній примітив синхронізації, який ми розглянемо в Python — це бар'єр Barrier. Він 
дозволяє задати умову, щоб кілька потоків продовжили роботу лише після того, як задане 
число потоків добереться у виконанні коду до цього "бар'єру".

Використовується, коли вам потрібно, щоб робота застосунку продовжилася лише після того, 
як усі потоки зроблять якусь частину своєї роботи та дійдуть до деякої точки, з якою можна 
знову продовжувати.
Розглянемо наступний приклад:"""

from random import randint
from threading import Thread, Barrier
import logging
from time import sleep, ctime


def worker(barier: Barrier):
    """Потік чекає на бар'єрі."""
    # Виведення часу початку роботи потоку
    logging.debug('Start thread:%s' ,ctime())
    sleep(randint(1, 3))  # Simulate some work
    # Очікування на бар'єрі
    r = barier.wait()
    # Виведення результату очікування
    logging.debug('count:%s', r)
    logging.debug('Barrier overcome:%s' ,ctime())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    # Створення бар'єру для 5 потоків
    barrier = Barrier(5)
# Створення та запуск 10 потоків
    for num in range(10):
        thread = Thread(name=f'Th-{num}', target=worker, args=(barrier, ))
        thread.start()
# Виведення:

# Th-0 Start thread: Tue Oct 18 12:13:21 2022
# Th-1 Start thread: Tue Oct 18 12:13:21 2022
# Th-2 Start thread: Tue Oct 18 12:13:21 2022
# Th-3 Start thread: Tue Oct 18 12:13:21 2022
# Th-4 Start thread: Tue Oct 18 12:13:21 2022
# Th-5 Start thread: Tue Oct 18 12:13:21 2022
# Th-6 Start thread: Tue Oct 18 12:13:21 2022
# Th-7 Start thread: Tue Oct 18 12:13:21 2022
# Th-8 Start thread: Tue Oct 18 12:13:21 2022
# Th-9 Start thread: Tue Oct 18 12:13:21 2022
# Th-4 count: 4
# Th-0 count: 0
# Th-1 count: 1
# Th-6 count: 2
# Th-3 count: 3
# Th-4 Barrier overcome: Tue Oct 18 12:13:22 2022
# Th-0 Barrier overcome: Tue Oct 18 12:13:22 2022
# Th-1 Barrier overcome: Tue Oct 18 12:13:22 2022
# Th-6 Barrier overcome: Tue Oct 18 12:13:22 2022
# Th-3 Barrier overcome: Tue Oct 18 12:13:22 2022
# Th-7 count: 4
# Th-2 count: 0
# Th-9 count: 3
# Th-8 count: 1
# Th-5 count: 2
# Th-7 Barrier overcome: Tue Oct 18 12:13:24 2022
# Th-2 Barrier overcome: Tue Oct 18 12:13:24 2022
# Th-9 Barrier overcome: Tue Oct 18 12:13:24 2022
# Th-8 Barrier overcome: Tue Oct 18 12:13:24 2022
# Th-5 Barrier overcome: Tue Oct 18 12:13:24 2022

TEXT = """ Потік може дістатися бар'єру і чекати його за допомогою функції wait().
Це блокуючий виклик, який повернеться, коли решта потоків (попередньо налаштована 
кількість barrier = Barrier(5)) дістануться бар'єру.

Функція очікування wait() повертає ціле число, яка вказує на кількість учасників, 
що залишилися до бар'єру. Якщо потік був останнім, що прибув, то повернене значення 
буде нульовим.

Як бачимо в нашому прикладі, спочатку виконалися потоки

Th-4 Barrier overcome: Tue Oct 18 12:13:22 2022
Th-0 Barrier overcome: Tue Oct 18 12:13:22 2022
Th-1 Barrier overcome: Tue Oct 18 12:13:22 2022
Th-6 Barrier overcome: Tue Oct 18 12:13:22 2022
Th-3 Barrier overcome: Tue Oct 18 12:13:22 2022

А потім наступні п'ять потоків

Th-7 Barrier overcome: Tue Oct 18 12:13:24 2022
Th-2 Barrier overcome: Tue Oct 18 12:13:24 2022
Th-9 Barrier overcome: Tue Oct 18 12:13:24 2022
Th-8 Barrier overcome: Tue Oct 18 12:13:24 2022
Th-5 Barrier overcome: Tue Oct 18 12:13:24 2022

Головна вимога, щоб кількість потоків, що запускаються, в нашому випадку 10 - range(10), 
була кратною кількості бар'єру, у нашому випадку 5 - Barrier(5). Інакше деякі потоки можуть 
залишитися вічно чекати на бар'єрі, якщо їхня кількість не досягне"""
    # print( barrier.wait())
    # print(TEXT)
