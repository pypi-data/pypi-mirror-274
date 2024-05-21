from abc import ABC, abstractmethod

class Component(ABC):
    probability_analytical: float

    @abstractmethod
    def calculate_probability_simulated(self) -> bool:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
