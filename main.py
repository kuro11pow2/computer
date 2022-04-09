from abc import *
from enum import Enum
from queue import Queue


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
        self.setStateWait()

        self.ins = [None] * len(ins)
        self.outs = [None] * len(outs)
        self.insName = ins
        self.outsName = outs

    def setInput(self, idx: int, val: int) -> None:
        self.ins[idx] = val

    def setStateWait(self) -> None:
        self.state = SimState.WAIT
    
    def setStateEval(self) -> None:
        self.state = SimState.EVAL
    
    def __repr__(self) -> str:
        s = f"[{self.__class__.__name__}] {self.id=}, {self.connectionsTo=}  ("
        for i, (inp, name) in enumerate(zip(self.ins, self.insName)):
            s += f"{name}: None" if inp == None else f"{name}: {inp:0>4X}"
            s += (", " if i < len(self.ins) - 1 else ") -> (")
        for outp, name in zip(self.outs, self.outsName):
            s += f"{name}: None" if outp == None else f"{name}: {outp:0>4X}"
            s += (", " if i < len(self.outs) - 1 else ")")
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
        if self.state != SimState.EVAL:
            raise Exception("Adder.eval() called in wrong state")
        self.outs = [sum(self.ins)]


def testAdder() -> bool:
    print()
    print("Test Adder")
    
    adder = Adder(0, [None])
    print(adder)

    adder.setInput(0, 0xF)
    adder.setInput(1, 0xF0)
    print(adder)

    adder.setStateEval()
    adder.eval()
    adder.setStateWait()
    print(adder)

    if adder.outs == [0xFF]:
        print(f"Adder test passed")
        return True
    else:
        print(f"Adder test failed")
        return False


testAdder()


class Task:
    def __init__(self, connectionsTo: list[ConnectionInfo], val: int) -> None:
        self.connectionsTo = connectionsTo
        self.inputVal = val


class CircuitSim:
    def __init__(self):
        self.units: dict[int, CircuitUnit] = dict()
        self.queue: Queue[Task] = Queue()
        self.queueLen = 0
        self.taskCount = 0
        self.timestepCount = 0
    
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
        updatedUnits: set[CircuitUnit] = set()

        for _ in range(count):
            task = self.popTask()

            for connection in task.connectionsTo:
                unit = self.units[connection.unitId]
                unit.setInput(connection.entryIdx, task.inputVal)
                updatedUnits.add(unit)
                self.taskCount += 1

        print(self)
        
        for unit in updatedUnits:
            unit.setStateEval()
            unit.eval()
            unit.setStateWait()

            if (unit.connectionsTo == None):
                continue

            for outVal in unit.outs:
                self.putTask(Task(unit.connectionsTo, outVal))

    def __repr__(self) -> str:
        s = f"[{self.__class__.__name__}] "
        s += f"{self.queueLen=}, {self.taskCount=}, {self.timestepCount=}\n"
        for i, unit in enumerate(self.units.values()):
            s += f"\t{unit}" + (f"\n" if i < len(self.units) - 1 else "")
        return s


def testCircuitSim():
    print()
    print("Test CircuitSim")

    sim = CircuitSim()

    # make units
    sim.units[0] = Adder(0, [ConnectionInfo(2, 0)])
    sim.units[1] = Adder(1, [ConnectionInfo(2, 1)])
    sim.units[2] = Adder(2, None)

    # make inputs
    sim.putTask(Task([ConnectionInfo(0, 0)], 0x1))
    sim.putTask(Task([ConnectionInfo(0, 1)], 0x10))
    sim.putTask(Task([ConnectionInfo(1, 0)], 0x2))
    sim.putTask(Task([ConnectionInfo(1, 1)], 0x20))
    print(sim)
    
    sim.eval()
    print(sim)

    sim.eval()
    print(sim)

    lastUnit = sim.units[len(sim.units) - 1]
    output = lastUnit.outs[len(lastUnit.outsName) - 1]
    if output == 0x33:
        print("CircuitSim test passed")
    else:
        print("CircuitSim test failed")


testCircuitSim()
