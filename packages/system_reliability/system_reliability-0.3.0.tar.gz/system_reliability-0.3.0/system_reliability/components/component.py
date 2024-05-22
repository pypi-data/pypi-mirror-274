from abc import ABC, abstractmethod

from system_reliability.enums import MethodConnection

class Component(ABC):
    probability_analytical: float

    @abstractmethod
    def calculate_probability_simulated(self) -> bool:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
    
    @abstractmethod
    def to_dict_analytical(self, mode: MethodConnection) -> dict:
        pass
