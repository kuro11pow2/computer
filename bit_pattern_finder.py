from finite_state_machine import State
from enum import Enum


class BitPatterFinderState(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    

class BitPatterFinderValue(Enum):
    zero = 0
    one = 1


class BitPatterFinder(State):
    stateTransitionMatrix = [
        [BitPatterFinderState.A, BitPatterFinderState.B],
        [BitPatterFinderState.C, BitPatterFinderState.B],
        [BitPatterFinderState.A, BitPatterFinderState.D],
        [BitPatterFinderState.C, BitPatterFinderState.E],
        [BitPatterFinderState.C, BitPatterFinderState.B],
    ]
    stateOutputs = [
        BitPatterFinderValue.zero, 
        BitPatterFinderValue.zero, 
        BitPatterFinderValue.zero, 
        BitPatterFinderValue.zero, 
        BitPatterFinderValue.one]

    def __init__(self, string):
        super().__init__(BitPatterFinderState.A)
        self.string = string
    
    def __repr__(self) -> str:
        return f"{self.string}, {super().__repr__()}"
    
    def find(self):
        output = ""
        for c in self.string:
            if c == '0':
                self.set(BitPatterFinderValue.zero)
            elif c == '1':
                self.set(BitPatterFinderValue.one)
            else:
                raise Exception("Invalid character")

            self.eval()
            output += str(self.get().value)
            print(self)


        return output
        

if __name__ == "__main__":
    def testBitPatterFinder():
        finder = BitPatterFinder("1011011")

        if finder.find() != "0001001":
            raise Exception("Test failed")
        else:
            print("Test passed")

    testBitPatterFinder()