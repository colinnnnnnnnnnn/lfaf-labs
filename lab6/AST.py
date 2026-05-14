from abc import ABC, abstractmethod
from typing import List

class Node(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    def to_dict(self):
        """Helper for visualizing AST as a dictionary/JSON"""
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self):
        self.statements: List[Statement] = []

    def __str__(self):
        return "\n".join(str(stmt) for stmt in self.statements)
    
    def to_dict(self):
        return {"Program": [stmt.to_dict() for stmt in self.statements]}

class LetStatement(Statement):
    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value

    def __str__(self):
        return f"let {self.name} = {self.value};"
    
    def to_dict(self):
        return {"LetStatement": {"name": self.name, "value": self.value.to_dict() if self.value else None}}

class PrintStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"print({self.expression});"
    
    def to_dict(self):
        return {"PrintStatement": {"expression": self.expression.to_dict() if self.expression else None}}

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"{self.expression};"
    
    def to_dict(self):
        return {"ExpressionStatement": self.expression.to_dict() if self.expression else None}

class BlockStatement(Statement):
    def __init__(self):
        self.statements: List[Statement] = []

    def __str__(self):
        stmts = "\n\t".join(str(s) for s in self.statements)
        return f"{{\n\t{stmts}\n}}"
    
    def to_dict(self):
        return {"BlockStatement": [stmt.to_dict() for stmt in self.statements]}

class IfStatement(Statement):
    def __init__(self, condition: Expression, consequence: BlockStatement, alternative: BlockStatement = None):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        res = f"if ({self.condition}) {self.consequence}"
        if self.alternative:
            res += f" else {self.alternative}"
        return res
    
    def to_dict(self):
        out = {
            "condition": self.condition.to_dict() if self.condition else None,
            "consequence": self.consequence.to_dict() if self.consequence else None
        }
        if self.alternative:
            out["alternative"] = self.alternative.to_dict()
        return {"IfStatement": out}

class Identifier(Expression):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value
    
    def to_dict(self):
        return {"Identifier": self.value}

class IntegerLiteral(Expression):
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def to_dict(self):
        return {"IntegerLiteral": self.value}

class FloatLiteral(Expression):
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def to_dict(self):
        return {"FloatLiteral": self.value}

class StringLiteral(Expression):
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'"{self.value}"'
    
    def to_dict(self):
        return {"StringLiteral": self.value}

class InfixExpression(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
    
    def to_dict(self):
        return {
            "InfixExpression": {
                "left": self.left.to_dict() if self.left else None,
                "operator": self.operator,
                "right": self.right.to_dict() if self.right else None
            }
        }

class FunctionCall(Expression):
    def __init__(self, function_name: str, arguments: List[Expression]):
        self.function_name = function_name
        self.arguments = arguments

    def __str__(self):
        args = ", ".join(str(a) for a in self.arguments)
        return f"{self.function_name}({args})"
    
    def to_dict(self):
        return {
            "FunctionCall": {
                "function": self.function_name,
                "arguments": [arg.to_dict() for arg in self.arguments]
            }
        }
