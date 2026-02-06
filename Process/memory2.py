""" Спільна пам'ять для процесів у Python
Щоб створити спільну пам'ять для процесів, необхідно визначити тип даних, який буде 
знаходитися у виділеній області пам'яті. Це порушує звичний для Python підхід, коли 
не потрібно думати про те, який тип даних буде використовуватися і скільки місця він 
може займати. 
Давайте розберемо складніший приклад, з використанням структур у спільній пам'яті.

У цьому прикладі ми створили:
- структуру Point, яка описує координати точки на площині;
- дробове число number;
- рядкову змінну string (підтримуються тільки byte-рядки);
- масив array, який містить координати точок відповідно до структури Point.

Зверніть увагу, для опису полів структури їх потрібно помістити в список кортежів _fields_, 
де кожен кортеж — це ім'я та тип поля.

Масив Array поводиться багато в чому як список і дозволяє зберігати в ньому різнотипні дані, 
але його розмір статичний і додавати/видаляти елементи не можна. Так само як і змінювати тип 
існуючих.

Також у структурі даних ми передали механізм блокування через параметр lock. Як Value, так і 
Array забезпечують блокування ресурсу, до якого можна отримати доступ, щоб як читати, так і 
оновлювати дані."""

from multiprocessing import Process, RLock, current_process
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class Point(Structure):
    """ Структура, що описує точку на площині """
    _fields_ = [('x', c_double), ('y', c_double)]


def modify(num: Value, string: Array, arr: Array):
    """ Функція, що модифікує спільні дані """
    logger.debug(f'Started {current_process().name}')
    logger.debug(f"Change num: {num.value}")
    # Модифікуємо спільні дані з блокуванням доступу до них
    with num.get_lock():
        # Оновлюємо значення числа (підносимо до квадрату)
        num.value **= 2
    logger.debug(f"to num: {num.value}")
    # Оновлюємо рядок та масив точок у спільній пам'яті з блокуванням доступу до них
    with string.get_lock():
        # Оновлюємо значення рядка (робимо всі літери великими)
        string.value = string.value.upper()
# Оновлюємо значення точок у масиві (підносимо координати до квадрату) з блокуванням доступу до них
    with arr.get_lock():
        for a in arr:
            a.x **= 2
            a.y **= 2
    logger.debug(f'Done {current_process().name}')


if __name__ == '__main__':
    # Створюємо спільні змінні з блокуванням доступу до них
    lock = RLock()
    # Спільні змінні у пам'яті процесів
    number = Value(c_double, 1.5, lock=lock)
    string = Array('c', b'hello world', lock=lock)
    array = Array(Point, [(1, -6), (-5, 2), (2, 9)], lock=lock)
# Створюємо два процеси, які будуть модифікувати спільні дані
    p = Process(target=modify, args=(number, string, array))
    p2 = Process(target=modify, args=(number, string, array))
    # Запускаємо процеси та очікуємо їх завершення
    p.start()
    p2.start()
    p.join()
    p2.join()
    # Виводимо змінені спільні дані на екран
    print(number.value)
    print(string.value)
    print([(arr.x, arr.y) for arr in array])
# Виведення:
# Started Process-2
# Change num: 1.5
# to num: 2.25
# Done Process-2
# Started Process-1
# Change num: 2.25
# to num: 5.0625
# Done Process-1
# 5.0625
# b'HELLO WORLD'
# [(1.0, 1296.0), (625.0, 16.0), (16.0, 6561.0)]


# Пояснення:
# Спільна пам'ять для процесів у Python дозволяє ефективно обмінюватися даними між процесами.
# Використання структур і масивів у спільній пам'яті дозволяє зберігати складніші типи даних.
# Блокування доступу до спільної пам'яті гарантує цілісність даних при одночасному доступі з
# різних процесів.
