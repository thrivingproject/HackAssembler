"""
This module drives translation process.
Assumes source assembly contains no symbolic references.
Bugs: No error checking, reporting, or handling.
"""

import sys
from os import path
from parser import Parser
import coder
from symbol_table import SymbolTable

asm_path = sys.argv[1]
path_root, ext = path.splitext(asm_path)
# Needed to prevent non-asm files from being parsed
if ext != ".asm":
    raise ValueError("Input file must have .asm extension")

# First pass needed to build symbol table
parser = Parser(asm_path)
sym_table = SymbolTable()
line_no = 0
while parser.has_more_lines():
    parser.advance()
    i_type = parser.instructionType()
    # Needed so we only add to line no for C and A instructions
    if i_type != Parser.InstructionType.L_INSTRUCTION:
        line_no += 1
    else:
        symbol = parser.symbol()
        # Label symbols can't only be declared more than once
        if sym_table.contains(symbol):
            raise ValueError(f"Symbol {symbol} defined multiple times")
        else:
            # Add 1 to get ROM address of next instruction
            sym_table.add_entry(symbol, line_no + 1)

# Second pass needed to handle variable symbols and generate binary
with open(path_root + ".hack", "w", encoding="utf-8") as f:
    parser = Parser(asm_path)
    while parser.has_more_lines():
        parser.advance()
        line = ""

        match parser.instructionType():
            case Parser.InstructionType.A_INSTRUCTION:
                # Need to cast to int since bin accepts int
                translation = bin(int(parser.symbol()))[2:]  # Cut off '0b'
                # Pad with zeros since bin uses as fewest bits as is possible
                line += translation.zfill(16)
            case Parser.InstructionType.C_INSTRUCTION:
                line += (
                    "111"
                    + coder.comp(parser.comp())
                    + coder.dest(parser.dest())
                    + coder.jump(parser.jump())
                )
            # Skip L-Instructions
            case _:
                continue

        f.write(line + "\n" if parser.has_more_lines() else line)
