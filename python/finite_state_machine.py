from abc import *
from enum import Enum


class State(metaclass=ABCMeta):    
    stateTransitionMatrix = None
    stateOutputs = None
    def __init__(self, initState):
        self.__waitingInput: Enum = None
        self.__input: Enum = None
        self.__state: Enum = initState
        self.__output: Enum = self.stateOutputs[self.__state.value]
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}$ {self.__input} -> ({self.__state}, {self.__output}), wait: {self.__waitingInput}"

    def set(self, input):
        if self.__waitingInput != None:
            raise Exception("Input already set")
        self.__waitingInput = input

    def eval(self):
        self.__waitingInput, self.__input = None, self.__waitingInput
        self.__state = self.stateTransitionMatrix[self.__state.value][self.__input.value]
        self.__output = self.stateOutputs[self.__state.value]

    def run(self):
        outputs = ""

        for input in self.inputs:
            self.set(input)
            self.eval()
            outputs += str(self.get().value)
            
        return outputs

    def get(self):
        return self.__output
