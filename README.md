***Парсинг API HH.***

***Структура***

**src**
Абстрактные классы:
- AbstractGetApiHh.py
- AbstractJsonSaver.py

Получаем инфо по API HH: GetApiHh.py
Возможность работать с файлами: JsonSaver.py
- save_file - сохранять
- read_file - читать
- add_vacancy_to_file - добавлять вакансии в файл
- delete_vacancy - удалять вакансии из файла

Создание класса с вакансиями: Vacancy.py
- get_vacancy_list - создание списка из вакансий (инициализация через class Vacancy)
- __lt__ - сравнивает вакансии

**tests**
Тесты классов

**main.py**
Упрощенное взаимодействие с пользователем.
