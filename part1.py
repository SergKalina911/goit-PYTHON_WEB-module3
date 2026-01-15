"""                                     Заняття 1: Багатопоточність у Python


                                        Вступ до багатопотоковості



                        Сфера застосування

​Що робить застосунок, доки чекає відповіді від сервера або чекає, доки файл прочитається із жорсткого диска? 
Зазвичай у такі моменти застосунок нічого не робить і просто чекає на результат операції. Це не є проблемою, 
тільки, якщо вам не потрібно прискорити роботу вашого застосунку. Особливо це критично для ситуацій, коли 
застосунок робить багато дуже схожих блокуючих викликів (запитів на віддалений сервер, операцій читання/запису 
файлів). У такі моменти, звичайно, хочеться оптимізувати роботу застосунку та виконувати кілька блокуючих 
операцій паралельно. Код, що виконує паралельно кілька завдань, називається асинхронним. Найпростіший спосіб 
реалізувати асинхронність — це виконувати завдання в окремих потоках всередині одного процесу.

Процес — область пам'яті (віртуальна) + набір ресурсів + 1 і більше потоків.

Потік — послідовність інструкцій та системних викликів всередині процесу.

Всі потоки мають доступ до всіх ресурсів свого процесу. Усі процеси ізольовані один від одного, і будь-яка 
міжпроцесна взаємодія відбувається тільки через операції введення/виведення (системні виклики).



                        IO and CPU bound tasks

​Завдання, які виконують операції введення/виведення (читання/запис файлів, запити в мережі тощо), називаються 
IO (Input Output)-bound завданнями. Домогтися паралелізму виконання IO завдань у Python можна, використовуючи 
потоки.

Однак потрібно пам'ятати, що асинхронний код завжди на порядок складніший для розуміння та відлагодження. Для 
багатопотокових застосунків складно писати тести та складно перевіряти всілякі ситуації, які відбуваються рідко 
та залежать від порядку викликів у різних потоках. Загальне правило для програмування будь-якою мовою: якщо є 
можливість обійтися синхронним кодом, то так і потрібно зробити.

Інший тип блокуючих викликів — це важкі з точки зору обчислень операції.

Реальний застосунок завжди повинен якимось чином реагувати на дії користувача і, якщо ваш застосунок під час 
виконання складних обчислень перестає відповідати на запити, то користувач може вирішити, що застосунок просто 
завис. Виходить, що для зручності користувача застосунок повинен відповідати на запити, навіть коли робить якісь 
складні та довгі обчислення.

Такі завдання називаються CPU-bound завданнями. Як і для IO-bound завдань, можна винести виконання блокуючих 
операцій (складних обчислень) в окремий потік, щоб застосунок продовжував взаємодіяти з користувачем, здійснюючи 
обчислення.

Загалом, операційна система передає управління потокам (як і передача управління процесами). Це означає, що 
будь-якої миті, перед будь-яким викликом ОС (Операційна Система) може призупинити виконання коду потоку та 
розпочати виконувати код іншого потоку, щоб потім так само далі призупинити і його для передачі управління.

До появи багатоядерних процесорів справжній паралелізм був неможливим. Звичайно, коли управління передається 
різним потокам по кілька тисяч разів на секунду, з погляду користувача це виглядає як паралельне виконання кількох 
завдань. У сучасних процесорах зазвичай є мінімум два ядра і тепер ми можемо писати код, який виконується справді 
паралельно. Це з однієї сторони додає можливостей, але й додає складнощів, оскільки тепер потрібно бути ще 
уважнішими при написанні асинхронного коду, адже припуститися помилки ще простіше.

Гарна стаття про асинхронний код. https://medium.com/swift-india/concurrency-parallelism-threads-processes-async-and-sync-related-39fd951bc61d


                        Global Interpreter Lock (GIL)

​Потоки можуть виконуватися дійсно паралельно (якщо ядер процесора більше 1), процеси — тим більше. Але у Python є 
механізм, який примусово блокує виконання коду різними потоками одного Python процесу в один і той самий час.

    1. Тільки один потік всередині процесу Python виконується, всі інші (якщо такі є) знаходяться в режимі 'Sleep'.
    2. Операції, пов'язані з введенням/виведенням (системні виклики) не блокуються GIL, але не їх послідовність.

Це означає, що якщо ви зробите кілька IO викликів у різних потоках, то вам не гарантується черговість завершення 
цих потоків, але гарантується, що коли виконується код будь-якого з потоків, всі інші потоки чекають черги і 
нічого не роблять. Це буде так, навіть якщо код виконується на сучасному процесорі з кількома ядрами


            Чому в Python є GIL?

    1. Простий і зрозумілий збирач сміття.
    2. Виключає можливість одночасного доступу до ресурсів/пам'яті. Немає потреби враховувати особливості 
    конкретної ОС для обробки таких ситуацій.
    3. Це спадщина епохи одноядерних процесорів, коли додаткові потоки/процеси уповільнювали виконання програми.

Python розроблявся в епоху одноядерних процесорів і навіть теоретично ніхто тоді не міг припустити дійсне 
одночасне виконання коду в різних потоках. Через це було зроблено низку архітектурних рішень, які вже не змінити, 
і на Python накладено обмеження GIL.


            Як обійти GIL:

    1. Написати частину коду, яку потрібно запускати паралельно, на Cython і використовувати потоки.
    2. Використовувати Multiprocessing.


            Чому не потрібно цього робити:

    1. Python — скриптова мова і швидкість роботи не її сильна сторона. Якщо потрібна швидкість, то, можливо, є 
    сенс розглянути інший інструмент.
    2. Створення процесів використовує деяку кількість ресурсів системи (пам'ять та процесорний час).
    3. Перемикання між процесами також використовує процесорний час.


                                        Створення потоків у Python


Документація про доступні в Python механізми написання потокового коду.
https://docs.python.org/3/library/concurrency.html


                        Потік як клас

​Щоб створити потік, найпростіше імпортувати клас Thread з модуля threading і наслідуватись від цього класу. Далі 
вам потрібно визначити метод run у вашого класу, цей метод буде виконуватись в окремому потоці. Щоб розпочати 
виконання коду в окремому потоці, потрібно викликати метод start, який визначений у Thread. Давайте напишемо клас 
MyThread, що в окремому потоці спить вказаний час і після цього виводить у консоль 'Wake up!':
"""

from threading import Thread
import logging
from time import sleep


class MyThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        sleep(2)
        logging.debug('Wake up!')
        logging.debug(f"args: {self.args}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    for i in range(5):
        thread = MyThread(args=(f"Count thread - {i}",))
        thread.start()
    print('Usefull message')


"""
Якщо виконати цей скрипт, то в консолі ви побачите:

Usefull message
Thread-5 Wake up!
Thread-5 args: ('Count thread - 4',)
Thread-3 Wake up!
Thread-3 args: ('Count thread - 2',)
Thread-2 Wake up!
Thread-2 args: ('Count thread - 1',)
Thread-1 Wake up!
Thread-1 args: ('Count thread - 0',)
Thread-4 Wake up!
Thread-4 args: ('Count thread - 3',)

Це означає, що основний потік застосунку спочатку вивів 'Usefull message' і після нього через 2 секунди п'ять 
потоків MyThread вивели своє 'Wake up!', і тільки після цього скрипт завершився.


                        Потік як функтор

​Є інший спосіб виконати код окремого потоку. Для цього потрібно, щоб код виконання був функтором (функцією або 
класом, який має метод __call__). Тоді об'єкт можна передати як іменований аргумент target у Thread:
"""

from threading import Thread
from time import sleep
import logging


class UsefulClass():
    def __init__(self, delay_time):
        self.delay = delay_time

    def __call__(self):
        sleep(self.delay)
        logging.debug('Wake up!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    t2 = UsefulClass(2)
    thread = Thread(target=t2)
    thread.start()
    print('Some stuff')

# Результат:
# Some stuff
# Thread-1 Wake up!


""" 
                        Потік у функції

​У процесі створення екземпляра класу Thread можна передати аргументу target функцію та передати їй аргументи:
"""

from threading import Thread
from time import sleep
import logging


def example_work(delay):
    sleep(delay)
    logging.debug('Wake up!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    for i in range(5):
        thread = Thread(target=example_work, args=(i,))
        thread.start()

"""

Результат буде:
Thread-1 Wake up!
Thread-2 Wake up!
Thread-3 Wake up!
Thread-4 Wake up!
Thread-5 Wake up!

Зверніть увагу, що аргументи, які потрібно передати у функцію, передаються як кортеж args у Thread. Іменовані 
аргументи для функції можна так само передати як словник kwargs у Thread.


                        Очікування виконання потоку

​Коли потрібно в основному застосунку дочекатися виконання потоку, можна скористатися блокуючим методом join."""

from threading import Thread
import logging
from time import sleep


def example_work(params):
    sleep(params)
    logging.debug('Wake up!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    logging.debug('Start program')
    threads = []
    for i in range(5):
        thread = Thread(target=example_work, args=(i,))
        thread.start()
        threads.append(thread)

    [el.join() for el in threads]

    logging.debug('End program')

"""
У консолі ви побачите:

MainThread Start program
Thread-1 Wake up!
Thread-2 Wake up!
Thread-3 Wake up!
Thread-4 Wake up!
Thread-5 Wake up!
MainThread End program

Основний потік дочекався [el.join() for el in threads], доки завершаться всі потоки thread зі списку threads, і 
тільки потім вивів End program.

Ви також можете перевірити — чи виконується потік, викликавши метод is_alive:"""

from threading import Thread
from time import sleep
import logging


class UsefulClass:
    def __init__(self, second_num):
        self.delay = second_num

    def __call__(self):
        sleep(self.delay)
        logging.debug('Wake up!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    t2 = UsefulClass(2)
    thread = Thread(target=t2)
    thread_locking = Thread(target=t2)

    thread.start()
    print(thread.is_alive(), thread_locking.is_alive())
    thread_locking.start()
    thread.join()
    thread_locking.join()
    print(thread.is_alive(), thread_locking.is_alive())
    print('After all...')

"""
True False
Thread-2 Wake up!
Thread-1 Wake up!
False False
After all...

Це може бути корисним, якщо ви хочете перевіряти стан потоку самостійно і не блокувати застосунок в очікуванні 
завершення.


                        Потоки Timer

​Екземпляри класу Timer починають працювати з деякою затримкою, яку визначає програміст. Крім того, ці потоки можна 
скасувати будь-якої миті в період затримки. Наприклад, ви передумали стартувати певний потік."""

from threading import Timer
import logging
from time import sleep


def example_work():
    logging.debug('Start!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    first = Timer(0.5, example_work)
    first.name = 'First thread'
    second = Timer(0.7, example_work)
    second.name = 'Second thread'
    logging.debug('Start timers')
    first.start()
    second.start()
    sleep(0.6)
    second.cancel()

    logging.debug('End program')

"""
Тут ми запланували виконання двох потоків, через 0.5 та 0.7 секунд. Але потім через 0.6 секунди скасували 
виконання другого потоку second.cancel()

Отримаємо таке виведення:

MainThread Start timers
First thread Start!
MainThread End program


                                        
                                        Контроль доступу до ресурсів

Оскільки ОС може на будь-якому виклику перервати виконання потоку та передати контроль іншому потоку, ви не можете 
бути впевненим, що робота із загальним ресурсом буде коректно завершеною і ресурс не опиниться в невизначеному 
стані.


                        Блокування

​Для цього є механізм блокування. У Python є два примітива блокувань: Lock та RLock. Lock трохи швидший і більш 
низькорівневий, але він не рекурсивний і може бути ситуація потрапляння в DeadLock, коли виконання коду 
заблокується, кілька потоків чекатимуть, доки хтось віддасть Lock, а його ніхто ніколи вже не віддасть. Це і є 
ситуація, коли програма "зависла".

RLock трохи повільніший, зате виключає взаємне блокування. Рекомендується завжди використовувати саме його, якщо 
немає вагомих причин використовувати Lock.

    NOTE
    Якщо провести аналогію з життя, то Lock це коли у кожного потоку один і той самий ключ і будь-який потік може 
    відкрити замок, хто б його не закрив із потоків. З RLock ситуація трохи інша, у кожного потоку свій ключ і 
    свій замок. 

Потік може відкрити лише свій замок своїм ключем і не відкриє замок, якщо його закрив інший потік."""

from threading import Thread, RLock
import logging
from time import time, sleep

lock = RLock()


def func(locker, delay):
    timer = time()
    locker.acquire()
    sleep(delay)
    locker.release()
    logging.debug(f'Done {time() - timer}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    t1 = Thread(target=func, args=(lock, 2))
    t2 = Thread(target=func, args=(lock, 2))
    t1.start()
    t2.start()
    logging.debug('Started')


"""
У цьому прикладі ми запустили два потоки і один загальний RLock. У консолі ви побачите:

MainThread Started
Thread-1 Done 2.0003550052642822
Thread-2 Done 4.000735521316528

Таке виведення означає, що один із потоків "взяв" lock і поки він його не "відпустив", інший чекав доки lock 
звільниться. Блокування ресурсу досягається виконанням команди locker.acquire(). Це робиться, щоб загальним 
ресурсом міг користуватися лише один потік на один момент часу, і лише коли потік закінчить роботу із загальним 
ресурсом, він відпускає lock, у нашому випадку команда locker.release(), і хтось інший зможе попрацювати з 
ресурсом. Так гарантується, що загальний ресурс не потрапить у невизначений стан, коли хтось почав із ним роботу 
та не закінчив, а хтось інший почав, і так далі.

Але найчастіше для блокування використовують контекст виконання:"""

from threading import Thread, RLock
import logging
from time import time, sleep

lock = RLock()


def func(locker, delay):
    timer = time()
    with locker:
        sleep(delay)
    logging.debug(f'Done {time() - timer}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    t1 = Thread(target=func, args=(lock, 2))
    t2 = Thread(target=func, args=(lock, 2))
    t1.start()
    t2.start()
    logging.debug('Started')

# Результат буде тим самим:
# MainThread Started
# Thread-1 Done 2.0014190673828125
# Thread-2 Done 4.002039194107056

"""
                        Семафори​

Другий примітив синхронізації — це семафори.

Семафори підходять до блокування іншим шляхом та вказують, що кілька потоків можуть користуватися ресурсом 
одночасно і цим обмежують кількість потоків. Наприклад, ми не хочемо надсилати десятки тисяч запитів до мережі 
одночасно, щоб не створювати навантаження на обладнання і вкажемо семафор, щоб не більше ста потоків могли 
одночасно надсилати запити. Щойно якийсь із потоків закінчить роботу і семафор його відпустить, то наступний 
потік із черги очікування зможе зробити свій запит.

Як приклад розглянемо виконання 10 потоків і обмежимо виконання за допомогою семафору до двох одночасно:"""

from threading import Semaphore, Thread
import logging
from time import sleep


def worker(condition):
    with condition:
        logging.debug(f'Got semaphore')
        sleep(1)
        logging.debug(f'finished')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    pool = Semaphore(2)
    for num in range(10):
        thread = Thread(name=f'Th-{num}', target=worker, args=(pool, ))
        thread.start()

"""
У цьому прикладі ми створили семафор, що обмежує до 2. Виконавши код, побачимо:

Th-0 Got semaphore
Th-1 Got semaphore
Th-1 finished
Th-0 finished
Th-2 Got semaphore
Th-3 Got semaphore
Th-3 finished
Th-2 finished
Th-4 Got semaphore
Th-5 Got semaphore
Th-5 finished
Th-4 finished
Th-6 Got semaphore
Th-7 Got semaphore
Th-7 finished
Th-6 finished
Th-8 Got semaphore
Th-9 Got semaphore
Th-9 finished
Th-8 finished

Результат у вас може відрізнятися, це справа випадку, коли і який потік візьме семафор. Але суть буде та сама, 
один потік чекатиме своєї черги, доки семафор звільниться. Крім того, якщо потоки одночасно почнуть писати в 
консоль їх виведення може перемішатися і матиме вигляд, начебто дві людини одночасно намагаються набрати 
повідомлення на одній клавіатурі.

Наступним кроком ми розглянемо синхронізацію роботи потоків за допомогою умов та подій.


"""