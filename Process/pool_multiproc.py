""" Пул процесів

Створення процесів за допомогою пакета multiprocessing

​Для спрощення комунікації у пакеті multiprocessing є клас, який реалізує пул процесів 
за аналогією з concurrent.futures.

Основне застосування — це виконання паралельно однакових завдань із деяким набором 
однотипних вхідних даних.

Пул процесів з multiprocessing дає більше контролю, ніж пул з concurrent.futures.

Основні можливості:

- розбиває вхідну послідовність на блоки та виконує паралельну обробку поблоково, так 
можна зменшити обсяг використовуваної пам'яті;
- асинхронне виконання трохи прискорює отримання результатів, якщо порядок не важливий;
- передача кортежу аргументів у target-функцію;

Детально з можливостями можна ознайомитись на сторінці офіційної документації.
https://docs.python.org/3.8/library/multiprocessing.html#module-multiprocessing.pool"""

from multiprocessing import Pool, current_process
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def worker(x):
    """Процес-робітник, що виконує завдання: піднесення до квадрату."""
    # Отримуємо ім'я процесу для логування й повідомляємо про старт робітника та його
    # вхідне значення x для обчислення.
    logger.debug(f"pid={current_process().pid}, x={x}")
    return x*x


if __name__ == '__main__':
    # Створюємо пул процесів з двома робітниками, які будуть виконувати завдання
    # піднесення до квадрату. Використовуємо контекстний менеджер для автоматичного
    # закриття пулу після завершення роботи. Усередині контекстного менеджера
    # виконуємо різні варіанти обробки завдань: послідовно з map, асинхронно з apply_async,
    # з кортежем аргументів за допомогою starmap та starmap_async. Після завершення
    # всіх завдань закриваємо пул і чекаємо на завершення всіх процесів за допомогою join().
    with Pool(processes=2) as pool:
        logger.debug(pool.map(worker, range(10)))
        # або асинхронно
        result = pool.apply_async(worker, (10,))
        logger.debug(result.get(timeout=1))
        # або з кортежем аргументів
        result = pool.starmap(worker, [(20,), (30,), (40,)])
        logger.debug(result)
        # або асинхронно з кортежем аргументів
        result = pool.starmap_async(worker, [(50,), (60,), (70,)])
        logger.debug(result.get(timeout=1))
        pool.close()
        pool.join()
    logger.debug("Finished")

# Результат виконання:
# pid=4932, x=0
# pid=13720, x=2
# pid=4932, x=1
# pid=13720, x=3
# pid=4932, x=4
# pid=13720, x=6
# pid=4932, x=5
# pid=13720, x=7
# pid=4932, x=8
# pid=4932, x=9
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
# pid=13720, x=10
# 100
# pid=4932, x=20
# pid=13720, x=30
# pid=4932, x=40
# [400, 900, 1600]
# pid=13720, x=50
# pid=4932, x=60
# pid=13720, x=70
# [2500, 3600, 4900]
# Finished
