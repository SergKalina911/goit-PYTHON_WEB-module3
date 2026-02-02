""" Ви також можете перевірити — чи виконується потік, викликавши метод is_alive: """

from threading import Thread
from time import sleep
import logging

# Клас, який виконує корисну роботу
class UsefulClass:
    """ Ініціалізація з затримкою """
    def __init__(self, second_num):
        # Зберігаємо затримку
        self.delay = second_num
    # Метод виклику, який буде виконуватися в потоці
    def __call__(self):
        sleep(self.delay)
        logging.debug('Wake up!')


if __name__ == '__main__':
    # Налаштування логування для відображення повідомлень з потоків
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    # Створення двох потоків з різними затримками
    t2 = UsefulClass(2)
    thread = Thread(target=t2)
    thread_locking = Thread(target=t2)
    # Запуск першого потоку
    thread.start()
    # Невелика затримка, щоб переконатися, що потік почав виконання
    sleep(0.1)
    # друк стану потоків
    print(" Is thread1 alive ? - ",thread.is_alive(), "Is thread2 alive? - ", thread_locking.is_alive())
    # Запуск другого потоку
    thread_locking.start()
    # Очікування завершення обох потоків
    thread.join()
    thread_locking.join()
    # друк стану потоків після завершення
    print(" Is thread1 alive ? - ",thread.is_alive(), "Is thread2 alive? - ", thread_locking.is_alive())
    print('After all...')

# True False
# Thread-2 Wake up!
# Thread-1 Wake up!
# False False
# After all...
#Це може бути корисним, якщо ви хочете перевіряти стан потоку самостійно і не блокувати застосунок в 
#очікуванні завершення.