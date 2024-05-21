from dataclasses import dataclass
from typing import List

@dataclass
class BlockDict:
    type_component: str
    connection: str
    probability: bool
    components: List

@dataclass
class ElementDict:
    type_component: str
    probability_analytical: float
    random_value: float
    probability: bool

@dataclass
class SimulationResult:
    success_count: int
    num_trials: int
    probability: float
    details: List[ElementDict | BlockDict]

@dataclass
class CulculateResult:
    simulated_results: SimulationResult