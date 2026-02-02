""" 
                        Потік у функції

​У процесі створення екземпляра класу Thread можна передати аргументу target функцію та 
передати їй аргументи:
"""
import threading
from threading import Thread
from time import sleep
import logging

# Функція, яка буде виконуватися в окремому потоці
def example_work(delay):
    sleep(delay)
    logging.debug('Wake up!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    # Створюємо та запускаємо потоки
    for i in range(5):
        # Створюємо потік, передаючи функцію та її аргументи
        thread = Thread(target=example_work, args=(i,))
        thread.start()

# Очікуємо завершення всіх потоків
    for thread in threading.enumerate():
        if thread is not threading.main_thread():
            thread.join()
         
# Результат буде:
# Thread-1 Wake up!
# Thread-2 Wake up!
# Thread-3 Wake up!
# Thread-4 Wake up!
# Thread-5 Wake up!