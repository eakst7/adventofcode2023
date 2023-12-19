#!/usr/bin/env python3
# pylint: disable=global-statement
# pylint: disable=missing-docstring
# pylint: disable=multiple-statements

from dataclasses import dataclass
from icecream import ic
from enum import Enum
import re
from typing import Literal

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

def parse_part(input: str) -> Part:
    input = input[1:-1]
    (x,m,a,s) = [ int(n[2:]) for n in input.split(",") ]

    part = {}
    part["x"] = x
    part["m"] = m
    part["a"] = a
    part["s"] = s

    return part

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



workflows: dict[WorkflowName,Workflow]
def process(filename: str) -> int:
    global workflows

    readinput(filename)
    total: int = 0

    rules,parts = input_data.split("\n\n")
    
    workflows = {}
    for rule in rules.split("\n"):
        wf = parse_workflow(rule)
        workflows[wf.name] = wf

    for part in parts.split("\n"):
        pt = parse_part(part)
        result = do_workflow(pt, "in")

        if result:
            total += pt["x"] + pt["m"] + pt["a"] + pt["s"]
        ic(pt,result)



    print(f"{total=}")
    return total

if __name__ == "__main__":
    process("input1.txt")
