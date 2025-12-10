from enum import Enum


class Parser:
    """Parses the input into instructions and instructions into fields"""

    class InstructionType(Enum):
        A_INSTRUCTION = 1
        C_INSTRUCTION = 2
        L_INSTRUCTION = 3

    _lines: list[str]
    _index: int
    _current_instruction: str

    def __init__(self, asm_path) -> None:
        self._index = -1
        self._lines = []
        with open(asm_path, "rt", encoding="utf-8") as f:
            for line in f:
                # strip() needed so lines indentions are removed
                self._lines.append(line.strip())

    def has_more_lines(self) -> bool:
        """Are there more lines in the assembly file to parse?"""
        return self._index + 1 < len(self._lines)

    def advance(self) -> None:
        """Advance to the next valid instruction, skipping comments and blank lines"""
        self._index += 1
        self._current_instruction = self._lines[self._index]
        if (
            self._current_instruction.startswith("//")
            # Check for "" since strip() turns lines with just "\n" into ""
            or self._current_instruction == ""
        ) and self.has_more_lines():
            self.advance()

    def instructionType(self) -> InstructionType:
        """Return the type of currently selected instruction"""
        if self._current_instruction.startswith("@"):
            return self.InstructionType.A_INSTRUCTION
        elif self._current_instruction.startswith("("):
            return self.InstructionType.L_INSTRUCTION
        else:
            return self.InstructionType.C_INSTRUCTION

    def symbol(self) -> str: ...

    def _get_eq_index(self):
        """Returns the index of the '=' sign in the current C-Instruction, or 0 if none.

        0 is used instead of `str.find()`'s -1 for indexing.
        """
        try:
            eq_sign = self._current_instruction.index("=")
        except ValueError:
            eq_sign = 0
        return eq_sign

    def dest(self) -> str:
        """Returns the symbolic _dest_ part of the current C-Instruction"""
        return self._current_instruction[: self._get_eq_index()]

    def comp(self) -> str:
        """Returns the symbolic _comp_ part of the current C-Instruction"""
        return self._current_instruction[
            self._get_eq_index() : self._current_instruction.find(";")
        ]

    def jump(self) -> str:
        """Returns the symbolic _jump_ part of the current C-Instruction"""
        return self._current_instruction[
            self._current_instruction.find(";") + 1 :
        ]
