from ..enums import MethodConnection


from ..date import SimulationResult, BlockDict, CulculateResult

from .component import Component

class Block(Component):
    
    def __init__(self, *components: Component, connection: MethodConnection):
        self.components = components
        self.connection = connection
        self.probability_analytical = self.calculate_probability_analytical()
    
    block_main = None
    block_step: str = None  
    simulated_step: int = None 
    simulated_results = []
       
    def calculate_probability_by_method_analytical(self, probability):
        match self.connection:
            case MethodConnection.Parallel:
                return 1 - probability
            case MethodConnection.Serial:
                return probability
    
    def calculate_probability_analytical(self):
        probability = 1
        for component in self.components:
            probability *= self.calculate_probability_by_method_analytical(component.probability_analytical)
        
        return self.calculate_probability_by_method_analytical(probability)
    
    def simulated_probability(self, num_trials) -> SimulationResult:
        success_count = 0
        
        for trial in range(num_trials):            
            is_successful = self.calculate_probability_simulated()
            
            if is_successful:
                success_count += 1
                
            self.simulated_results.append(self.to_dict())
            
        return SimulationResult(
            success_count=success_count,
            num_trials=num_trials,
            probability=success_count / num_trials,
            details=self.simulated_results
        )
            
    def calculate_probability_by_method_simulated(self, prob_one: bool, prob_two: bool) -> bool:
        match self.connection:
            case MethodConnection.Parallel:
                return prob_one or prob_two
            case MethodConnection.Serial:
                return prob_one and prob_two
    
    def calculate_probability_simulated(self) -> bool:    
        probability = 1 if self.connection == MethodConnection.Serial else 0 
        
        for component in self.components:
            probability = self.calculate_probability_by_method_simulated(probability, component.calculate_probability_simulated())
        
        self.probability_simulated = probability
        
        return probability
    
    def to_dict(self) -> BlockDict:
        return BlockDict(
            type_component=self.__class__.__name__,
            connection=self.connection.value,
            probability=self.probability_simulated,
            components=[component.to_dict() for component in self.components],
        )

    
    def calculate(self):
        simulated = self.simulated_probability(num_trials=10000)
        
        return CulculateResult(
            simulated_results=simulated
        )