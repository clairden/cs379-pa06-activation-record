"""
PA 4 dependency: paste in YOUR OWN completed PA 3 parser.py here
(same file, copied from your PA 3 repo -- see PA_03's lexer.py note).

Complete the parsing functions below. AST node types are already
defined -- do not modify them. See the assignment,
Part B, for the full requirements.
"""

from dataclasses import dataclass, field
from typing import List

from lexer import Token, tokenize


@dataclass
class Program:
    statements: list


@dataclass
class Declaration:
    name: str
    expr: object
    line: int


@dataclass
class Assignment:
    name: str
    expr: object
    line: int


@dataclass
class BinOp:
    op: str
    left: object
    right: object
    line: int


@dataclass
class Number:
    value: int
    line: int


@dataclass
class Variable:
    name: str
    line: int


class ParseError(Exception):
    pass


class _ParserState:
    """Given: a small cursor wrapper over the token list. Not required to use, but handy."""

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_: str) -> Token:
        tok = self.peek()
        if tok.type != type_:
            raise ParseError(f"Line {tok.line}: expected {type_}, found {tok.type} ({tok.lexeme!r}).")
        return self.advance()


def parse_factor(state: _ParserState):
    # TODO
    tok = state.peek()

    if tok.type == "LPAREN":
        state.advance() #consume left parentheses token
        expr = parse_expr(state) #expr call
        state.expect("RPAREN") #consume right parentheses token
        return expr

    elif tok.type == "NUMBER":  
        state.advance()
        return Number(value=int(tok.lexeme), line=tok.line)

    elif tok.type == "IDENT":
        state.advance()
        return Variable(name=tok.lexeme, line=tok.line)

    elif tok.type == "MINUS":
        state.advance()
        rightnum = parse_factor(state) #recurse minus factor call
        return BinOp(op = "-", left = Number(value = 0, line = tok.line), right = rightnum, line = tok.line)

    else:
        raise ParseError(
            f"Line {tok.line}: expected NUMBER, IDENT, LPAREN or MINUS"
            f"Found {tok.type} ({tok.lexeme})"
        )


def parse_term(state: _ParserState):
    # TODO
    tok = state.peek()
    left = parse_factor(state)
    

    while state.peek().type in ("STAR", "SLASH"):
        operToken = state.peek()
        state.advance()
        right = parse_factor(state) #next factor
        left = BinOp(op = operToken.lexeme, left = left, right = right, line = operToken.line)

    return left


def parse_expr(state: _ParserState):
    # TODO
    tok = state.peek()
    left = parse_term(state)

    while state.peek().type in ("PLUS", "MINUS"):
        operToken = state.peek()
        state.advance()
        right = parse_term(state)
        left = BinOp(op = operToken.lexeme, left = left, right = right, line = operToken.line)

    return left


def parse_declaration(state: _ParserState) -> Declaration:
    # TODO
    let_token = state.expect("LET")
    ident_token = state.expect("IDENT")
    state.expect("ASSIGN")
    expr = parse_expr(state)
    state.expect("SEMI")
    return Declaration(name = ident_token.lexeme, expr=expr, line = let_token.line)


def parse_assignment(state: _ParserState) -> Assignment:
    # TODO
    ident_token = state.expect("IDENT")
    state.expect("ASSIGN")
    expr = parse_expr(state)
    state.expect("SEMI")
    return Assignment(name = ident_token.lexeme, expr=expr, line = ident_token.line)


def parse_statement(state: _ParserState):
    # TODO: peek at state.peek().type to choose declaration vs. assignment
    tok = state.peek()

    if tok.type == "LET":
        return parse_declaration(state)

    elif tok.type == "IDENT":
        return parse_assignment(state)

    else:
        raise ParseError (
            f"Line {tok.line}: expected 'let' or IDENT to start a statement, "
            f"found {tok.type} ({tok.lexeme})."
        )


def parse_program(state: _ParserState) -> Program:
    # TODO: loop parse_statement() until end
    statements = []

    while state.peek().type != "EOF":
        statements.append(parse_statement(state))

    return Program(statements=statements)


def parse(tokens: List[Token]) -> Program:
    state = _ParserState(tokens)
    return parse_program(state)
