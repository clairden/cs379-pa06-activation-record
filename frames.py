"""
PA 6: The Activation Record -- starter.

Complete ActivationRecord and CallStack below. See
PA_06_The_Activation_Record.md, Part B, for the full requirements.

Note on scope: PA1-5 never added function-call SYNTAX to USILang's
grammar (deliberately -- see PA5's pipeline-context note). PA6's
Part B interface is pure Python classes with no mention of parser
changes either, so test_frames.py drives ActivationRecord/CallStack
directly in Python (simulating what a parsed function call sequence
would do) rather than parsing real USILang function syntax. Your job
this week is the frame model itself, not a grammar extension.
"""

from typing import Dict, List, Optional

from symtable import Environment


class ActivationRecord:
    def __init__(
        self,
        function_name: str,
        parameters: Dict[str, object],
        locals_env: Environment,
        return_address: str,
        static_link: Optional["ActivationRecord"],
        dynamic_link: Optional["ActivationRecord"],
    ) -> None:
        # TODO: store all six arguments as attributes of the same names.
        self.function_name = function_name
        self.parameters = parameters
        self.locals_env = locals_env
        self.return_address = return_address
        self.static_link = static_link
        self.dynamic_link = dynamic_link


class CallStack:
    def __init__(self) -> None:
        # TODO: internal storage for the stack of frames.
        self.frames = []

    def push(self, record: ActivationRecord) -> None:
        # TODO
        self.frames.append(record)

    def pop(self) -> ActivationRecord:
        """Remove and return the top frame."""
        # TODO
        self.frames.pop()

    def current(self) -> ActivationRecord:
        """Return (without removing) the top frame."""
        # TODO
        return self.frames[-1]

    def trace(self) -> List[str]:
        """
        Return one formatted string per live frame, BOTTOM of the
        stack first (oldest call first). Format is up to you, but
        each line must include the function_name and its parameters.
        """
        # TODO
        result = []
        for record in self.frames:
            result.append(
                f"{record.function_name}: {record.parameters}\n"
                f"Local environment: {record.locals_env}\n"
                f"Return address: {record.return_address}\n"
                f"Static Link: {record.static_link}\n"
                f"Dynamic Link: {record.dynamic_link}"
                )

        return result