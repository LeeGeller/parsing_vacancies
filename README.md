# ***Парсинг API HH.***

## ***Структура***

### **src**
Абстрактные классы:
* [AbstractGetApiHh.py](https://github.com/LeeGeller/work_with_API_hh/blob/main/src/AbstractGetApiHh.py)
* [AbstractJsonSaver.py](https://github.com/LeeGeller/work_with_API_hh/blob/main/src/AbstractJsonSaver.py)

Получаем инфо по API HH:  [GetApiHh.py](https://github.com/LeeGeller/work_with_API_hh/blob/main/src/GetApiHh.py)
Возможность работать с файлами: [JsonSaver.py](https://github.com/LeeGeller/work_with_API_hh/blob/main/src/JsonSaver.py)
* save_file - сохранять
* read_file - читать
* add_vacancy_to_file - добавлять вакансии в файл
* delete_vacancy - удалять вакансии из файла

Создание класса с вакансиями: [Vacancy.py](https://github.com/LeeGeller/work_with_API_hh/blob/main/src/Vacancy.py)
* get_vacancy_list - создание списка из вакансий (инициализация через class Vacancy)
* __lt__ - сравнивает вакансии

**tests**
* Тесты классов

**main.py**
* Упрощенное взаимодействие с пользователем.
