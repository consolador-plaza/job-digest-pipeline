from abc import ABC

from abc import abstractmethod



class BaseParser(ABC):


    SOURCE = None


    @abstractmethod

    def parse(

        self,

        payload
    ):

        pass