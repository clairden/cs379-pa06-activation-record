"""
PA 4: The USILang Symbol Table -- starter.

Complete Environment and check_program below. See
PA_04_The_USILang_Symbol_Table.md, Part B, for the full requirements.
"""

from typing import Optional

from parser import Assignment, BinOp, Declaration, Number, Program, Variable


class SemanticError(Exception):
    pass


class Environment:
    def __init__(self, parent: Optional["Environment"] = None) -> None:
        self.parent = parent
        self._names: dict = {}  # name -> declaration line, THIS scope only

    def define(self, name: str, line: int) -> None:
        """
        Store name -> line in THIS scope. Raise SemanticError if `name`
        is already defined in THIS scope (not a parent scope --
        shadowing a parent name is allowed).
        """
        # TODO
        if name in self._names:
            original_line = self._names[name]
            raise SemanticError(f"Redeclaration Error: on line {line}"
                                f"{name} previously defined on {original_line}")

        else:
            self._names[name] = line

    def resolve(self, name: str) -> int:
        """
        Look up `name` in this scope, then climb `parent` links.
        Return the declaration line, or raise SemanticError if not
        found anywhere in the chain.
        """
        # TODO
        current = self

        while current != None:
            if name in current._names:
                return current._names[name]

            current = current.parent

        raise SemanticError(...)


def check_program(ast: Program) -> Environment:
    """
    Walk `ast.statements` in order, using one top-level Environment.
    For a Declaration: resolve every Variable in its expr BEFORE
    defining the new name (so `let x = x;` fails as use-before-decl).
    For an Assignment: resolve the assigned-to name, then resolve
    every Variable in its expr. Errors must surface at the first
    offending statement, not be collected and reported together.
    """
    # TODO
    env = Environment(parent=None)

    def check_expr(expr):
        if isinstance(expr, Variable):
            env.resolve(expr.name)

        elif isinstance(expr, Number):
            pass

        elif isinstance(expr, BinOp):
            check_expr(expr.left)
            check_expr(expr.right)

    for statement in ast.statements:

        if isinstance(statement, Declaration):

            check_expr(statement.expr)
            env.define(statement.name, statement.line)


        elif isinstance(statement, Assignment):

            env.resolve(statement.name)
            check_expr(statement.expr)

    return env
