#!/usr/bin/env python3
# pylint: disable=global-statement
# pylint: disable=missing-docstring
# pylint: disable=multiple-statements

import re
from dataclasses import dataclass
from enum import Enum
from typing import Literal

from icecream import ic

input_data: str

type Part = dict[str,int]

class Op(Enum):
    GT = 0
    LT = 1

@dataclass
class Condition:
    var: str
    op: Op
    val: int

    def __repr__(self):
        op = ">" if self.op == Op.GT else "<"
        s = self.var + " " + op + " " + self.val
        return s

type Accept = Literal["A"]
type Reject = Literal["R"]
type WorkflowName = str

@dataclass
class Workflow:
    name: str
    conditions: list[tuple[Condition,WorkflowName|Accept|Reject]]

def parse_workflow(input: str) -> Workflow:
    conditions: list[tuple[Condition,WorkflowName]] = []

    (_,name,rules,_) = re.split(r"(.+)\{(.+)\}", input.strip())
    rules = rules.split(",")
    for rule in rules:
        if ":" in rule:
            expression, workflow_name = rule.split(":")
            var = expression[0]
            match expression[1]:
                case "<": op = Op.LT
                case ">": op = Op.GT
                case _: raise Exception
            val = int(expression[2:])
            conditions.append( (Condition(var,op,val),workflow_name) )
        else:
            workflow_name = rule
            conditions.append( (None,workflow_name) )

    return Workflow(name, conditions)

def readinput(filename: str):
    global input_data
    with open(filename, "r", encoding="utf-8") as fp:
        input_data = fp.read().strip()

def do_workflow(part: Part, wf_name: WorkflowName) -> bool:
    wf = workflows[wf_name]

    for condition,next_workflow in wf.conditions:
        if condition is None:
            match next_workflow:
                case "A":
                    return True
                case "R":
                    return False
                case _:
                    return do_workflow(part,next_workflow)

        partval = part[condition.var]
        compval = condition.val
        match condition.op:
            case Op.GT:
                if partval > compval:
                    match next_workflow:
                        case "A":
                            return True
                        case "R":
                            return False
                        case _:
                            return do_workflow(part,next_workflow)
            case Op.LT:
                if partval < compval:
                    match next_workflow:
                        case "A":
                            return True
                        case "R":
                            return False
                        case _:
                            return do_workflow(part,next_workflow)

@dataclass
class FromTo:
    low: int
    high: int

@dataclass
class Constraints:
    x: FromTo
    m: FromTo
    a: FromTo
    s: FromTo

    def combinations(self) -> int:
        x = max(0,self.x.high-self.x.low+1)
        m = max(0,self.m.high-self.m.low+1)
        a = max(0,self.a.high-self.a.low+1)
        s = max(0,self.s.high-self.s.low+1)

        return x * m * a * s
    
    def __str__(self) -> str:
        return f"x{self.x.low}-{self.x.high} m{self.m.low}-{self.m.high} a{self.a.low}-{self.a.high} s{self.s.low}-{self.s.high} --> {self.combinations()}"

def run_workflow(depth: int, fromwf: str, name: str, constraints: Constraints) -> int:
    wf = workflows[name]

    next_constraints = Constraints(
            FromTo(constraints.x.low, constraints.x.high),
            FromTo(constraints.m.low, constraints.m.high),
            FromTo(constraints.a.low, constraints.a.high),
            FromTo(constraints.s.low, constraints.s.high))

    combinations = 0
    for (condnum,(condition,next_workflow)) in enumerate(wf.conditions):
        constraints = Constraints(
            FromTo(next_constraints.x.low, next_constraints.x.high),
            FromTo(next_constraints.m.low, next_constraints.m.high),
            FromTo(next_constraints.a.low, next_constraints.a.high),
            FromTo(next_constraints.s.low, next_constraints.s.high))
        
        if condition is None:
            match next_workflow:
                case "A":
                    print(f"{'  ' * depth} {fromwf}->{name} ({condnum}) {constraints}")
                    combinations += constraints.combinations()
                case "R":
                    combinations += 0
                case _:
                    combinations += run_workflow(depth + 1, fromwf + "->" + name, next_workflow,constraints)
        else:
            compval = condition.val
            match condition.op:
                case Op.LT:
                    match condition.var:
                        case "x":
                            constraints.x.high = min(constraints.x.high, compval-1)
                            next_constraints.x.low = max(next_constraints.x.low, compval)
                        case "m":
                            constraints.m.high = min(constraints.m.high, compval-1)
                            next_constraints.m.low = max(next_constraints.m.low, compval)
                        case "a":
                            constraints.a.high = min(constraints.a.high, compval-1)
                            next_constraints.a.low = max(next_constraints.a.low, compval)
                        case "s":
                            constraints.s.high = min(constraints.s.high, compval-1)
                            next_constraints.s.low = max(next_constraints.s.low, compval)
                case Op.GT:
                    match condition.var:
                        case "x":
                            constraints.x.low = max(constraints.x.low, compval+1)
                            next_constraints.x.high = min(constraints.x.high, compval)
                        case "m":
                            constraints.m.low = max(constraints.m.low, compval+1)
                            next_constraints.m.high = min(constraints.m.high, compval)
                        case "a":
                            constraints.a.low = max(constraints.a.low, compval+1)
                            next_constraints.a.high = min(constraints.a.high, compval)
                        case "s":
                            constraints.s.low = max(constraints.s.low, compval+1)
                            next_constraints.s.high = min(constraints.s.high, compval)

            match next_workflow:
                case "A":
                    print(f"{'  ' * depth} {fromwf}->{name} ({condnum}) {constraints}")
                    combinations += constraints.combinations()
                case "R":
                    combinations += 0
                case _:
                    combinations += run_workflow(depth + 1, fromwf + "->" + name, next_workflow,constraints)

    return combinations


workflows: dict[WorkflowName,Workflow]
def process(filename: str) -> int:
    global workflows

    readinput(filename)
    total: int = 0

    rules,_ = input_data.split("\n\n")
    
    workflows = {}
    for rule in rules.split("\n"):
        wf = parse_workflow(rule)
        workflows[wf.name] = wf

    constraints = Constraints(
        FromTo(1,RANGE_MAX),
        FromTo(1,RANGE_MAX),
        FromTo(1,RANGE_MAX),
        FromTo(1,RANGE_MAX)
    )
    total = run_workflow(0, "", "in", constraints)

    print(f"{total=}")
    return total

# RANGE_MAX = 100
RANGE_MAX = 4000
if __name__ == "__main__":
    process("input2.txt")
