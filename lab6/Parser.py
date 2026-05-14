from Lexer import Token
from AST import *
from typing import List

class Precedence:
    LOWEST = 1
    EQUALS = 2
    SUM = 4
    PRODUCT = 5
    CALL = 7

PRECEDENCES = {
    'EQUALS': Precedence.EQUALS,
    'PLUS': Precedence.SUM,
    'MINUS': Precedence.SUM,
    'MULTIPLY': Precedence.PRODUCT,
    'DIVIDE': Precedence.PRODUCT,
    'LPAREN': Precedence.CALL
}

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
        self.peek_token = self.tokens[self.pos + 1] if len(self.tokens) > 1 else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        self.peek_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None

    def current_precedence(self):
        if not self.current_token:
            return Precedence.LOWEST
        return PRECEDENCES.get(self.current_token.type, Precedence.LOWEST)

    def peek_precedence(self):
        if not self.peek_token:
            return Precedence.LOWEST
        return PRECEDENCES.get(self.peek_token.type, Precedence.LOWEST)

    def parse_program(self) -> Program:
        program = Program()
        while self.current_token and self.current_token.type != 'EOF':
            stmt = self.parse_statement()
            if stmt:
                program.statements.append(stmt)
            self.advance()
        return program

    def parse_statement(self) -> Statement:
        if self.current_token.type == 'LET':
            return self.parse_let_statement()
        elif self.current_token.type == 'PRINT':
            return self.parse_print_statement()
        elif self.current_token.type == 'IF':
            return self.parse_if_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self) -> LetStatement:
        # current is LET
        self.advance()
        if self.current_token.type != 'IDENTIFIER':
            raise Exception(f"Expected identifier, got {self.current_token.type}")
        
        name = self.current_token.value
        self.advance()

        if self.current_token.type != 'ASSIGN':
            raise Exception(f"Expected '=', got {self.current_token.type}")
        
        self.advance()
        value = self.parse_expression(Precedence.LOWEST)

        if self.peek_token and self.peek_token.type == 'SEMICOLON':
            self.advance()

        return LetStatement(name, value)

    def parse_print_statement(self) -> PrintStatement:
        # current is PRINT
        self.advance()
        
        if self.current_token.type == 'LPAREN':
            self.advance()
            val = self.parse_expression(Precedence.LOWEST)
            if self.peek_token and self.peek_token.type == 'RPAREN':
                self.advance()
        else:
            val = self.parse_expression(Precedence.LOWEST)

        if self.peek_token and self.peek_token.type == 'SEMICOLON':
            self.advance()
            
        return PrintStatement(val)
        
    def parse_if_statement(self) -> IfStatement:
        # current is IF
        self.advance()
        
        if self.current_token.type != 'LPAREN':
            raise Exception(f"Expected '(', got {self.current_token.type}")
        self.advance()
        
        condition = self.parse_expression(Precedence.LOWEST)
        
        if self.peek_token and self.peek_token.type == 'RPAREN':
            self.advance()
            
        self.advance()
        consequence = self.parse_block_statement()
        
        alternative = None
        if self.peek_token and self.peek_token.type == 'ELSE':
            self.advance()
            self.advance()
            alternative = self.parse_block_statement()
            
        return IfStatement(condition, consequence, alternative)

    def parse_block_statement(self) -> BlockStatement:
        block = BlockStatement()
        if self.current_token.type != 'LBRACE':
            raise Exception(f"Expected '{{', got {self.current_token.type}")
            
        self.advance()
        while self.current_token and self.current_token.type not in ('RBRACE', 'EOF'):
            stmt = self.parse_statement()
            if stmt:
                block.statements.append(stmt)
            self.advance()
            
        return block

    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression(Precedence.LOWEST)
        if self.peek_token and self.peek_token.type == 'SEMICOLON':
            self.advance()
        return ExpressionStatement(expr)

    def parse_expression(self, precedence: int) -> Expression:
        if self.current_token.type == 'IDENTIFIER':
            left_exp = str(self.current_token.value)
            left_node = Identifier(left_exp)
        elif self.current_token.type == 'INTEGER':
            left_node = IntegerLiteral(int(self.current_token.value))
        elif self.current_token.type == 'FLOAT':
            left_node = FloatLiteral(float(self.current_token.value))
        elif self.current_token.type == 'STRING':
            left_node = StringLiteral(self.current_token.value)
        elif self.current_token.type in ('SIN', 'COS'):
            # Math functions treating as identifiers or specific builtin calls
            left_node = Identifier(self.current_token.type.lower())
        elif self.current_token.type == 'LPAREN':
            self.advance()
            left_node = self.parse_expression(Precedence.LOWEST)
            if self.peek_token and self.peek_token.type == 'RPAREN':
                self.advance()
        else:
            raise Exception(f"Unexpected token for expression start: {self.current_token}")

        while self.peek_token and self.peek_token.type != 'SEMICOLON' and precedence < self.peek_precedence():
            if self.peek_token.type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUALS'):
                self.advance()
                left_node = self.parse_infix_expression(left_node)
            elif self.peek_token.type == 'LPAREN':
                self.advance()
                left_node = self.parse_call_expression(left_node)
            else:
                return left_node

        return left_node

    def parse_infix_expression(self, left: Expression) -> Expression:
        operator = self.current_token.value
        precedence = self.current_precedence()
        self.advance()
        right = self.parse_expression(precedence)
        return InfixExpression(left, operator, right)

    def parse_call_expression(self, function: Expression) -> Expression:
        args = []
        if self.peek_token and self.peek_token.type == 'RPAREN':
            self.advance()
            return FunctionCall(str(function), args)
            
        self.advance()
        args.append(self.parse_expression(Precedence.LOWEST))
        
        while self.peek_token and self.peek_token.type == 'COMMA':
            self.advance() # move to comma
            self.advance() # move to next expr
            args.append(self.parse_expression(Precedence.LOWEST))
            
        if self.peek_token and self.peek_token.type == 'RPAREN':
            self.advance()
            
        return FunctionCall(str(function), args)
