""" Менеджер ресурсів
Докладніше див.
https://docs.python.org/3/library/multiprocessing.html#managers

Вимогливіший до ресурсів, але й зручніший у використанні механізм обміну даними 
між процесами — це Менеджер ресурсів. Основна перевага — можливість працювати по 
всій мережі та реалізувати розподілені обчислення між кількома комп'ютерами в одній 
мережі, реалізація Python-like списків та словників.

Недоліки:
- Необхідність синхронізувати доступ до загальних ресурсів;
- Обмеження типів, що підтримуються;
- Складне API. 

У наступному прикладі ми запустили п'ять процесів і додали до словника m, для кожного 
процесу його pid — ідентифікатор процесу. Все це було створено та управлялося 
менеджером Manager.

Увага! Використання менеджера ресурсів уповільнює роботу програми, оскільки кожен запит 
до спільного ресурсу вимагає передачі даних між процесами через сокети. 

Ще є важливе зауваження. Проксі-об'єкти Manager не можуть поширювати зміни, внесені до 
об'єктів, що змінюються всередині контейнера. Іншими словами, якщо у вас є об'єкт 
manager.list(), будь-які зміни в самому керованому списку розповсюджуються на всі інші 
процеси. Але якщо у вас є звичайний список Python всередині цього списку, будь-які зміни 
у внутрішньому списку не поширюються, тому що менеджер не має можливості виявити зміни.

Щоб розповсюдити зміни, ви також повинні використовувати об'єкти manager.list() для 
вкладених списків. (необхідний Python 3.6 або вище) або вам потрібно безпосередньо змінити 
об'єкт manager.list() (див. примітку нижче за посиланням).
https://docs.python.org/3.5/library/multiprocessing.html#multiprocessing.managers.SyncManager.list"""

from multiprocessing import Process, Manager, current_process
from random import randint
from time import sleep
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def worker(delay, val: Manager):
    name = current_process().name
    logger.debug(f'Started: {name}')
    sleep(delay)
    val[name] = current_process().pid
    logger.debug(f'Done: {name}')


if __name__ == '__main__':
    with Manager() as manager:
        m = manager.dict()
        processes = []
        for i in range(5):
            pr = Process(target=worker, args=(randint(1, 3), m))
            pr.start()
            processes.append(pr)

        [pr.join() for pr in processes]
        print(m)
    logger.debug('Main process done')
   
# Вивід програми:
# Started: Process-2
# Started: Process-3
# Started: Process-5
# Started: Process-4
# Started: Process-6
# Done: Process-3
# Done: Process-5
# Done: Process-2
# Done: Process-6
# Done: Process-4
# {'Process-3': 7444, 'Process-5': 15976, 'Process-2': 15564, 'Process-6': 18896, 'Process-4': 14244}
# Main process done
