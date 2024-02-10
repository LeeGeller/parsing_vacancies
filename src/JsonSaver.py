import json

from config import DATA
from src.AbstractJsonSaver import AbstractJsonSaver
from src.GetApiHh import GetApiHh


class JsonSaver(AbstractJsonSaver):
    @classmethod
    def save_file(cls, data: list):
        """Save file"""
        with open(DATA, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    @classmethod
    def read_file(cls):
        """Read file"""
        with open(DATA, encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def add_vacancy_to_file(cls, data: list):
        old_list = cls.read_file()
        new_list = data + old_list
        cls.save_file(new_list)

    @classmethod
    def delete_vacancy(cls, vacancy: str):
        new_list = []

        old_list = cls.read_file()

        for params in old_list:
            if params['name'] != vacancy:
                new_list.append(params)

        cls.save_file(new_list)
