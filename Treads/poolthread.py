""" Пул потоків

В Python існує ще один механізм написання асинхронного коду. Ви можете скористатися 
пакетом concurrent.futures. Він дозволяє піднятися на вищий рівень абстракції, коли 
вам просто потрібно паралельно виконати ряд однотипних завдань і немає необхідності 
вдаватися до низькорівневих деталей реалізації. 
(https://docs.python.org/3/library/concurrent.futures.html)

Основна ідея полягає у використанні реалізації абстрактного класу Executor. У 
concurrent.futures є дві реалізації цього абстрактного базового класу: 
ProcessPoolExecutor — для виконання коду окремих процесів (з ним ми 
познайомимося пізніше) та ThreadPoolExecutor — для виконання в окремих потоках.

Кожен такий Executor приховує набір потоків або процесів, яким ви можете дати роботу 
та отримати результат її виконання. Вам не потрібно вручну управляти створенням потоків 
та їх коректним завершенням.Звичайно, все ще потрібно пам'ятати про доступ до загальних 
ресурсів та примітиви синхронізації."""

import concurrent.futures
import logging
from random import randint
from time import sleep


def greeting(name):
    """Імітація привітання з випадковою затримкою."""
    # Логування імені, яке буде привітатися
    logging.debug('greeting for:%s ', {name})
    # Випадкова затримка від 0 до 3 секунд
    sleep(randint(0, 3))
    return f"Hello {name}"

# Аргументи для функції greeting
arguments = (
    "Bill",
    "Jill",
    "Till",
    "Sam",
    "Tom",
    "John",
)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    # Створення пулу потоків з двома робочими потоками
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Паралельне виконання функції greeting з різними аргументами
        results = list(executor.map(greeting, arguments))

    logging.debug(results)

TEXT =  """ У цьому прикладі ми створюємо ThreadPoolExecutor та задаємо, що робота буде
виконуватися не більше ніж 2 потоками. Пул можна створити в менеджері контексту як у 
прикладі, щоб бути впевненим, що всі ресурси будуть коректно повернуті до системи після 
завершення. Але це не обов'язково, можна створити пул і потім викликати у нього метод 
shutdown, щоб завершити всі потоки та повернути ресурси системі.

Далі ми передаємо в пул функцію, яку потрібно виконати у кілька потоків, та набір аргументів 
цієї функції — кожен для виконання в окремому потоці. В executor є метод map, він використовується, 
коли потрібно паралельно виконати функцію з різними вхідними аргументами в окремих потоках.
Результатом виклику map буде ітератор за результатами виконання в окремих потоках.

У консолі ви побачите щось схоже:

ThreadPoolExecutor-0_0 greeting for: Bill
ThreadPoolExecutor-0_1 greeting for: Jill
ThreadPoolExecutor-0_0 greeting for: Till
ThreadPoolExecutor-0_1 greeting for: Sam
ThreadPoolExecutor-0_0 greeting for: Tom
ThreadPoolExecutor-0_1 greeting for: John
MainThread ['Hello Bill', 'Hello Jill', 'Hello Till', 'Hello Sam', 'Hello Tom', 'Hello John']

Результат, звичайно, може відрізнятися через випадкові затримки.

Зверніть увагу, що код паралельно виконується не більше ніж двома потоками — 
ThreadPoolExecutor-0_0 та ThreadPoolExecutor-0_1. Результат повертається лише після 
того, як усі вхідні дані оброблені."""
print(TEXT)
