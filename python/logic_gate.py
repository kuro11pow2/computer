from abc import abstractmethod

class LogicCircuit:
    def __init__(self, nInputs, nOutputs):
        """
        nInputs: number of input bit
        nOutputs: number of output bit
        """
        self.nInputs = nInputs
        self.nOutputs = nOutputs
        self.waitingInput:list[bool] = [None] * nInputs
        # self.input: bits given to the circuit
        self.input:list[bool] = [None] * nInputs
        # self.output: bits returned by the circuit
        self.output:tuple[bool] = tuple([None] * nOutputs)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}$ {self.input} -> {self.output}, wait: {self.waitingInput}"
    
    def set(self, n, input):
        self.waitingInput[n] = self.waitingInput[n] or input
    
    @abstractmethod
    def eval(self):
        raise NotImplementedError()

    def get(self):
        return self.output


class NorGate(LogicCircuit):
    def __init__(self):
        super().__init__(nInputs=2, nOutputs=1)
    
    def eval(self):
        if any(map(lambda x: x == None, self.waitingInput)):
            raise Exception("Input not set")
        
        self.input = list(self.waitingInput)
        self.waitingInput = [None] * self.nInputs
        self.output = (not (self.input[0] or self.input[1]),)

class AndGate(LogicCircuit):
    def __init__(self):
        super().__init__(nInputs=2, nOutputs=1)
    
    def eval(self):
        if any(map(lambda x: x == None, self.waitingInput)):
            raise Exception("Input not set")
        
        self.input = list(self.waitingInput)
        self.waitingInput = [None] * self.nInputs
        
        norA = NorGate()
        norB = NorGate()
        norBack = NorGate()

        norA.set(0, self.input[0])
        norA.set(1, self.input[0])
        norA.eval()
        print(f"{norA=}")
        norB.set(0, self.input[1])
        norB.set(1, self.input[1])
        norB.eval()
        print(f"{norB=}")
        norBack.set(0, norA.get()[0])
        norBack.set(1, norB.get()[0])
        norBack.eval()
        print(f"{norBack=}")
        self.output = (norBack.get()[0],)


def testNorGate():
    nor = NorGate()
    nor.set(0, True), nor.set(1, True)
    nor.eval()
    print(f"{nor}")
    if nor.get() != (False,):
        raise Exception("Nor gate failed")
    else:
        print("Nor gate passed")
    
    nor = NorGate()
    nor.set(0, True), nor.set(1, False)
    nor.eval()
    print(f"{nor}")
    if nor.get() != (False,):
        raise Exception("Nor gate failed")
    else:
        print("Nor gate passed")

    nor = NorGate()
    nor.set(0, False), nor.set(1, True)
    nor.eval()
    print(f"{nor}")
    if nor.get() != (False,):
        raise Exception("Nor gate failed")
    else:
        print("Nor gate passed")

    nor = NorGate()
    nor.set(0, False), nor.set(1, False)
    nor.eval()
    print(f"{nor}")
    if nor.get() != (True,):
        raise Exception("Nor gate failed")
    else:
        print("Nor gate passed")
        

def testAndGate():
    andGate = AndGate()
    andGate.set(0, True), andGate.set(1, True)
    andGate.eval()
    print(f"{andGate}")
    if andGate.get() != (True,):
        raise Exception("And gate failed")
    else:
        print("And gate passed")

    andGate = AndGate()
    andGate.set(0, True), andGate.set(1, False)
    andGate.eval()
    print(f"{andGate}")
    if andGate.get() != (False,):
        raise Exception("And gate failed")
    else:
        print("And gate passed")

    andGate = AndGate()
    andGate.set(0, False), andGate.set(1, True)
    andGate.eval()
    print(f"{andGate}")
    if andGate.get() != (False,):
        raise Exception("And gate failed")
    else:
        print("And gate passed")

    andGate = AndGate()
    andGate.set(0, False), andGate.set(1, False)
    andGate.eval()
    print(f"{andGate}")
    if andGate.get() != (False,):
        raise Exception("And gate failed")
    else:
        print("And gate passed")

if __name__ == "__main__":

    testAndGate()