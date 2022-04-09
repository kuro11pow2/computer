from enum import Enum
from queue import Queue
from abc import *


class SimState(Enum):
    WAIT = 0
    EVAL = 1


class ConnectionInfo:
    def __init__(self, unitId: int, entryIdx: int) -> None:
        self.unitId = unitId
        self.entryIdx = entryIdx
    
    def __repr__(self) -> str:
        return f"{self.unitId=}, {self.entryIdx=}"


class CircuitUnit(metaclass=ABCMeta):
    def __init__(self, id: int, connectionsTo: list[ConnectionInfo], ins: list[str], outs: list[str]) -> None:
        self.id = id
        self.connectionsTo = connectionsTo

        self.ins = [0] * len(ins)
        self.outs = [0] * len(outs)
        self.insName = ins
        self.outsName = outs

    def setInput(self, idx: int, val: int) -> None:
        self.ins[idx] = val
    
    def __repr__(self) -> str:
        s = f"[{self.__class__.__name__}] {self.id=}, {self.connectionsTo=} - "
        for i, (ins, name) in enumerate(zip(self.ins, self.insName)):
            s += f"{name}: {ins:0>4X}" + (", " if i < len(self.ins) - 1 else " -> ")
        for outs, name in zip(self.outs, self.outsName):
            s += f"{name}: {outs:0>4X}"  + (", " if i < len(self.outs) - 1 else "")
        return s

    def eval(self) -> None:
        raise NotImplementedError

class Adder(CircuitUnit):
    def __init__(self, id: int, connectionsTo: list[ConnectionInfo]):
        """
        :param id: unit id
        :param connectionsTo: connectionsTo[i] is i-th output's ConnectionInfo
        """
        super().__init__(id=id, connectionsTo=connectionsTo, ins=["A", "B"], outs=["Result"])

    def eval(self) -> None:
        self.outs = [sum(self.ins)]


def testAdder() -> bool:
    adder = Adder(0, [None])
    print(adder)

    adder.setInput(0, 0xF)
    adder.setInput(1, 0xF0)
    print(adder)

    adder.eval()
    print(adder)

    if adder.outs == [0xFF]:
        print(f"Adder test passed {adder.ins} -> {adder.outs}")
        return True
    else:
        print(f"Adder test failed {adder.ins} -> {adder.outs}")
        return False


testAdder()


class Task:
    def __init__(self, connectionsTo: list[ConnectionInfo], val: int) -> None:
        self.connectionsTo = connectionsTo
        self.inputVal = val


class CircuitSim:
    def __init__(self):
        self.setStateWait()
        self.units: dict[int, CircuitUnit] = dict()
        self.queue: Queue[Task] = Queue()
        self.queueLen = 0
        self.taskEvalCount = 0
        self.timestepCount = 0

    def setStateWait(self) -> None:
        self.state = SimState.WAIT
    
    def setStateEval(self) -> None:
        self.state = SimState.EVAL
    
    def putTask(self, task: Task) -> None:
        self.queue.put(task)
        self.queueLen += 1
    
    def popTask(self) -> Task:
        if (self.queueLen == 0):
            raise Exception("Queue is empty")
        task = self.queue.get()
        self.queueLen -= 1
        return task

    def eval(self) -> None:
        count = self.queueLen
        
        if (count == 0):
            return

        self.timestepCount += 1
        for _ in range(count):
            task = self.popTask()

            for connection in task.connectionsTo:
                unit = self.units[connection.unitId]
                unit.setInput(connection.entryIdx, task.inputVal)
                unit.eval()
                self.taskEvalCount += 1

                for outVal in unit.outs:
                    self.putTask(Task(unit.connectionsTo, outVal))

    def __repr__(self) -> str:
        s = f"[{self.__class__.__name__}] "
        s += f"{self.queueLen=}, {self.taskEvalCount=}, {self.timestepCount=}\n"
        for i, unit in enumerate(self.units.values()):
            s += f"\t{unit}" + (f"\n" if i < len(self.units) - 1 else "")
        return s

    


def testCircuitSim():
    sim = CircuitSim()

    # make units
    sim.units[0] = Adder(0, [ConnectionInfo(2, 0)])
    sim.units[1] = Adder(1, [ConnectionInfo(2, 1)])
    sim.units[2] = Adder(2, [ConnectionInfo(None, None)])

    # make inputs
    sim.putTask(Task([ConnectionInfo(0, 0)], 0x1))
    sim.putTask(Task([ConnectionInfo(0, 1)], 0x10))
    sim.putTask(Task([ConnectionInfo(1, 0)], 0x2))
    sim.putTask(Task([ConnectionInfo(1, 1)], 0x20))
    print(sim)
    
    sim.setStateEval()
    sim.eval()
    print(sim)

    sim.setStateWait()
    sim.eval()
    print(sim)

testCircuitSim()