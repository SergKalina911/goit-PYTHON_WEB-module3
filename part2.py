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
import sys
# затримка для встигнення підключитися до консолі
# print( "You have 5 seconds to connect to the console..." )
sleep(5)
# Налаштування логування
logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

# Похідний клас від Process
class MyProcess(Process):
    # Ініціалізація з додатковими аргументами
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
# Перевизначення методу run
    def run(self) -> None:
        logger.debug(self.args)

# Функція для виконання в окремому процесі
def example_work(params):
    sleep(0.5)
    # Логування отриманих параметрів
    logger.debug(params)
    # Завершення процесу з кодом 0
    # sys.exit(0)


if __name__ == '__main__':
    # Створення та запуск процесів
    processes = []
    for i in range(3):
        # Створення процесу з функцією target
        pr = Process(target=example_work, args=(f"Count process function - {i}", ))
        # Запуск процесу
        pr.start()
        # Додавання процесу до списку
        processes.append(pr)
# Створення та запуск процесів з класом MyProcess
    for i in range(2):
        # Створення процесу з класом MyProcess
        pr = MyProcess(args=(f"Count process class - {i}",))
        # Запуск процесу
        pr.start()
        # Додавання процесу до списку
        processes.append(pr)
    # Dрук списку процесів
    print(processes)
    # Очікування завершення всіх процесів
    [el.join() for el in processes]
    # Виведення кодів завершення процесів
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


                        Contexts and start methods

Загальні зауваження та поради при роботі з процесами https://docs.python.org/3.8/library/multiprocessing.html#programming-guidelines

Залежно від платформи multiprocessing підтримує 3 способи створення нового процесу:

    - spawn — запускає новий процес Python, наслідуються лише ресурси, необхідні для запуску run(). Присутній в 
    Unix і Windows. Є способом за замовчуванням для Windows і macOS.
    - fork — дочірній процес, що є точною копією батьківського (включаючи всі потоки), доступний тільки на Unix. 
    За замовчуванням використовується на Unix. Зробити безпечний fork досить проблематично і це може бути причиною 
    неочевидних проблем.
    - forkserver — створюється процес-фабрика (сервер для породження процесів за запитом). Наслідуються тільки 
    необхідні ресурси, що використовуються fork для запуску нового процесу, але завдяки однопотоковій реалізації процесу-фабрики, це робиться безпечно. Доступний тільки на Unix платформах з підтримкою передачі файлових дескрипторів через pipes (що може суперечити безпековій політиці на багатьох системах).

Для вибору методу використовується multiprocessing.set_start_method(method)"""

# import multiprocessing
# ...

# if __name__ == '__main__':
#     multiprocessing.set_start_method('forkserver')
#     ...
#     processes = []
#     for i in range(3):
#         pr = Process(target=example_work, args=(f"Count process function - {i}", ))
#         pr.start()
#         processes.append(pr)
#     ...
#     for i in range(2):
#         pr = MyProcess(args=(f"Count process class - {i}",))
#         pr.start()
#         processes.append(pr)
#     ...
#     [el.join() for el in processes]
#     [print(el.exitcode, end=' ') for el in processes]
#     logger.debug('End program')
    
""" У цьому прикладі ми встановили метод запуску процесів 'forkserver' - механізм створення дочірніх процесів. 
Залежно від платформи, на якій виконується код, можуть бути доступні не всі методи запуску процесів.


                        Interprocess communication

​Для міжпроцесорної взаємодії виокремлюють наступні інструменти:

    - файли;
    -сокети;
    - канали (всі POSIX ОС);
    -роздільна пам'ять (всі POSIX ОС);
    -семафори (всі POSIX ОС);
    -сигнали або переривання (крім Windows);
    -семафори (всі POSIX ОС);
    - черга повідомлень;

Найбільшу складність при роботі з процесами представляє обмін даними між процесами, оскільки у кожного процесу 
своя ізольована область пам'яті. Механізми обміну даними залежать від ОС (Операційної Системи). 
Найуніверсальніший — файли. Але ви також можете скористатися мережевими інтерфейсами (localhost), примітивами на 
основі мережевих інтерфейсів (pipe) та загальною пам'яттю, де це можливо.

У будь-якому разі, крім загальної пам'яті, для обміну даними між процесами всі об'єкти серіалізуються та 
десеріалізуються. Цей додатковий крок створює навантаження на CPU.

Найшвидшим та найекономнішим з погляду ресурсів способом обміну даними є спільна пам'ять.


                        Спільна пам'ять

Спільна пам'ять підтримується не всіма операційними системами та може бути заборонена політикою безпеки.

Щоб створити область спільної пам'яті, потрібно вказати ОС, скільки пам'яті потрібно виділити. Для обчислення 
обсягу пам'яті обов'язково потрібно вказати тип даних, який буде використовуватись, та кількість елементів для 
складних типів. Крім того, механізми обмеження доступу до спільного ресурсу також потрібно забезпечити самостійно, 
інакше дані можна зіпсувати при спробі одночасного доступу для зміни із різних процесів."""



from multiprocessing import Process, Value, RLock, current_process
from time import sleep
import logging
import sys
# затримка для встигнення підключитися до консолі
# print( "You have 5 seconds to connect to the console..." )
# sleep(5)
# Налаштування логування
logger = logging.getLogger()
#встановлення обробника виведення в консоль 
stream_handler = logging.StreamHandler()
# додавання обробника до логгера
logger.addHandler(stream_handler)
# встановлення рівня логування
logger.setLevel(logging.DEBUG)

# Функція, яка буде виконуватися в окремому процесі
def worker(val: Value):
    # Логування початку роботи процесу
    logger.debug(f'Started {current_process().name}')
    sleep(1)
    # Захист критичної секції за допомогою блокування
    with val.get_lock():
        # Збільшення значення в спільній пам'яті
        val.value += 1
    # Логування завершення роботи процесу
    logger.debug(f'Done {current_process().name}')
    # Завершення процесу
    sys.exit(0)


if __name__ == '__main__':
    # Створення об'єкта Value для спільної пам'яті з блокуванням
    lock = RLock()
    value = Value('d', 0, lock=lock)
    # Створення та запуск процесів
    pr1 = Process(target=worker, args=(value, ))
    pr1.start()
    pr2 = Process(target=worker, args=(value, ))
    pr2.start()
    # Очікування завершення процесів
    pr1.join()
    pr2.join()
    # Виведення значення зі спільної пам'яті
    print(value.value)  # 2.0
    
""" 
Виведення:

Started Process-1
Started Process-2
Done Process-1
Done Process-2
2.0

У цьому прикладі ми скористалися механізмом спільної пам'яті Value. Тип даних було обрано десятковий ('d'). 
Докладніше про доступні типи та їх назви можна дізнатися з документації.
https://docs.python.org/3.8/library/ctypes.html#fundamental-data-types

Щоб створити спільну пам'ять для процесів, необхідно визначити тип даних, який буде знаходитися у виділеній 
області пам'яті. Це порушує звичний для Python підхід, коли не потрібно думати про те, який тип даних буде використовуватися і скільки місця він може займати.

Давайте розберемо складніший приклад, з використанням структур у спільній пам'яті:
"""              

from multiprocessing import Process, RLock, current_process
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
import logging
sleep(5)
# Налаштування логування
logger = logging.getLogger()
# встановлення обробника виведення в консоль
stream_handler = logging.StreamHandler()
# додавання обробника до логгера
logger.addHandler(stream_handler)
# встановлення рівня логування
logger.setLevel(logging.DEBUG)

# Визначення структури Point з двома полями x та y
class Point(Structure):
    # Визначення полів структури
    _fields_ = [('x', c_double), ('y', c_double)]

# Функція для модифікації значень у спільній пам'яті
def modify(num: Value, string: Array, arr: Array):
    # Логування початку роботи процесу
    logger.debug(f'STARTED {current_process().name}')
    # Затримка для імітації роботи
    logger.debug(f"Change num: {num.value}")
    # Модифікація значень у спільній пам'яті з використанням блокувань
    with num.get_lock():
        # Квадрат значення num
        num.value **= 2
    # логування зміненого значення
    logger.debug(f"to num: {num.value}")
    # Модифікація рядка у спільній пам'яті
    with string.get_lock():
        # Перетворення рядка на верхній регістр
        string.value = string.value.upper()
    logger.debug(f'Change string to: {string.value}')
    # Модифікація масиву структур у спільній пам'яті
    with arr.get_lock():
        # Квадрат полів x та y для кожної структури в масиві
        for a in arr:
            a.x **= 2
            a.y **= 2
    # Логування завершення роботи процесу
    logger.debug(f'Done {current_process().name}')

# Головний блок виконання
if __name__ == '__main__':
    # Створення об'єктів спільної пам'яті з блокуваннями
    lock = RLock()
    number = Value(c_double, 1.5, lock=lock)
    string = Array('c', b'hello world', lock=lock)
    array = Array(Point, [(1, -6), (-5, 2), (2, 9)], lock=lock)

    p = Process(target=modify, args=(number, string, array))
    p2 = Process(target=modify, args=(number, string, array))
    p.start()
    p2.start()
    p.join()
    p2.join()
    print(number.value)
    print(string.value)
    print([(arr.x, arr.y) for arr in array])

"""
Виведення буде приблизно таким:

Started Process-2
Change num: 1.5
to num: 2.25
Done Process-2
Started Process-1
Change num: 2.25
to num: 5.0625
Done Process-1
5.0625
b'HELLO WORLD'
[(1.0, 1296.0), (625.0, 16.0), (16.0, 6561.0)]

У цьому прикладі ми створили:
- структуру Point, яка описує координати точки на площині;
- дробове число number;
- рядкову змінну string (підтримуються тільки byte-рядки);
- масив array, який містить координати точок відповідно до структури Point.

Зверніть увагу, для опису полів структури їх потрібно помістити в список кортежів _fields_, де кожен кортеж — це 
ім'я та тип поля.

Масив Array поводиться багато в чому як список і дозволяє зберігати в ньому різнотипні дані, але його розмір 
статичний і додавати/видаляти елементи не можна. Так само як і змінювати тип існуючих.

Також у структурі даних ми передали механізм блокування через параметр lock. Як Value, так і Array забезпечують 
блокування ресурсу, до якого можна отримати доступ, щоб як читати, так і оновлювати дані.