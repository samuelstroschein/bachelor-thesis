from typing import List, Tuple


class AlgorithmV1:
    def __init__(self, starting_range: Tuple[float, float]) -> None:
        # starting tuple = (x,y) where x must be greater than y
        assert(starting_range[0] > starting_range[1])
        self.step_ranges: List[Tuple[float, float]] = [starting_range]

    def step(self) -> List[float]:
        """
        Generate a new vector of values from high to low.

        The returned vector acts as parameters to print for a calibration tower. 
        """
        assert(self.step_ranges[-2] != self.step_ranges[-1]
               if len(self.step_ranges) > 1 else True)
        result = []
        current_range = self.step_ranges[-1]
        values_to_generate = 5
        step_size = (current_range[0] - current_range[1]
                     ) / (values_to_generate - 1)
        next_value = current_range[1]  # start with lowest value
        for _ in range(values_to_generate):
            result.append(next_value)
            next_value = round(next_value + step_size, 2)
        return result

    def set_next_step_range(self, range: Tuple[float, float]) -> None:
        self.step_ranges.append(range)
