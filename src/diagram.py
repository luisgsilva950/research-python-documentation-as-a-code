from abc import abstractmethod, ABC


class Diagram(ABC):

    @abstractmethod
    def save_as_svg(self, filename: str):
        raise NotImplemented
