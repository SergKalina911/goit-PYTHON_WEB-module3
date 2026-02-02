""" Condition

​Є примітиви синхронізації, які дозволяють потокам очікувати сигнал від інших потоків — це 
Condition. 
Створимо дві різні функції: одна master повідомлятиме, що worker може продовжити роботу. При цьому 
вони будуть виконуватись у різних потоках.
Спочатку master у потоці виконує якусь роботу. Після цього він виконує метод condition.notify_all() 
чим дозволяє запустити інші потоки, доки вони чекають виконання. Вони очікують на виконання в точці 
виклику методу condition.wait().
Якщо ж master повинен дозволити роботу лише одному з worker, можна викликати метод 
condition.notify(),
тоді тільки один з тих, хто очікує дозволу worker продовжить роботу. Другий чекатиме, доки не буде 
виконано наступне condition.notify."""

from threading import Thread, Condition
import logging
from time import sleep


def worker(condit: Condition):
    """ Worker function """

    #  Готові працювати
    logging.debug('Worker ready to work')
    # Очікуємо на сигнал від master
    with condit:
        # Чекаємо на дозвіл від master
        condit.wait()
        # Отримали дозвіл на роботу
        logging.debug('The worker can do the work')


def master(condit: Condition):
    """ Master function """

    # Робимо якусь роботу
    logging.debug('Master doing some work')
    sleep(2)
    # Повідомляємо worker, що вони можуть працювати
    with condit:
        # Повідомляємо, що worker може працювати
        logging.debug('Informing that workers can do the work')
        # Дозволяємо всім worker працювати
        condit.notify_all()
        # Або дозволяємо працювати лише одному worker
        # condition.notify()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    condition = Condition()
    master = Thread(name='master', target=master, args=(condition,))

    worker_one = Thread(name='worker_one', target=worker, args=(condition, ))
    worker_two = Thread(name='worker_two', target=worker, args=(condition,))
    worker_one.start()
    worker_two.start()
    master.start()

logging.debug('End program')

# Після виконання коду прикладу, у консолі ви побачите:

# worker_one Worker ready to work
# worker_two Worker ready to work
# master Master doing some work
# MainThread End program
# master Informing that workers can do the work
# worker_one The worker can do the work
# worker_two The worker can do the work
