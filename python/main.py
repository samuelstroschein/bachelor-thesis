from ast import literal_eval as make_tuple
from algorithm_v1 import AlgorithmV1

algo = AlgorithmV1((6, 0))
while True:
    print(algo.step())
    new_range = make_tuple(
        input("Give new range in form of (x,y) where x > y"))
    algo.set_next_step_range(new_range)
