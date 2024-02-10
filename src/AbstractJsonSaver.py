from abc import ABC, abstractmethod


class AbstractJsonSaver(ABC):

    @abstractmethod
    def get_vacancy_from_api(self, data:list):
        pass

    @abstractmethod
    def save_file(self):
        pass

    @abstractmethod
    def read_file(self):
        pass
