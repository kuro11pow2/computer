from finite_state_machine import State
from enum import Enum


class BitPatternFinderState(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    

class BitPatternFinderValue(Enum):
    zero = 0
    one = 1


class BitPatternFinder(State):
    stateTransitionMatrix = [
        [BitPatternFinderState.A, BitPatternFinderState.B],
        [BitPatternFinderState.C, BitPatternFinderState.B],
        [BitPatternFinderState.A, BitPatternFinderState.D],
        [BitPatternFinderState.C, BitPatternFinderState.E],
        [BitPatternFinderState.C, BitPatternFinderState.B],
    ]
    stateOutputs = [
        BitPatternFinderValue.zero, 
        BitPatternFinderValue.zero, 
        BitPatternFinderValue.zero, 
        BitPatternFinderValue.zero, 
        BitPatternFinderValue.one]

    def __init__(self, inputs):
        super().__init__(BitPatternFinderState.A)
        self.inputs = list(map(lambda x : BitPatternFinderValue.zero if x == "0" else BitPatternFinderValue.one, inputs))
    
    def __repr__(self) -> str:
        return f"{self.inputs}, {super().__repr__()}"
        

if __name__ == "__main__":
    def testBitPatternFinder():
        inputs = "1011011"
        finder = BitPatternFinder(inputs)

        expected = "0001001"
        observed = finder.run()

        if observed == expected:
            print(f"Test passed: {inputs} -> {observed}, expected: {expected}")
        else:
            raise Exception("Test failed")

    testBitPatternFinder()