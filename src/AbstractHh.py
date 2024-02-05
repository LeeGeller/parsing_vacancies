from abc import ABC, abstractmethod


class AbstractHh(ABC):

    @abstractmethod
    def get_vacancy_from_api(self):
        pass

    @abstractmethod
    def save_info(self):
        pass

    # @abstractmethod
    # def get_vacancy_info(self):
    #     pass

    # @abstractmethod
    # def remove_vacancy(self):
    #     pass
