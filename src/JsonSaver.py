import json

from config import DATA
from src.AbstractJsonSaver import AbstractJsonSaver
from src.GetApiHh import GetApiHh


class JsonSaver(AbstractJsonSaver):
    def save_file(self, data: list):
        """Save file"""
        with open(DATA, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    def read_file(self):
        """Read file"""
        with open(DATA, encoding='utf-8') as file:
            return json.load(file)


v = GetApiHh()
v.get_vacancy_from_api('python')
j = JsonSaver()
j.save_file(v.all_vacancy)
print(j.read_file())
