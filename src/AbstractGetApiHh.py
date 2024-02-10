from abc import ABC, abstractmethod


class AbstractGetApiHh(ABC):
    @abstractmethod
    def get_vacancy_from_api(self):
        pass
