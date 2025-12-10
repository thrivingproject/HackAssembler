"""
This module drives translation process.
Assumes source assembly contains no symbolic references.
Bugs: No error checking, reporting, or handling.
"""

import sys
from os import path

from parser import Parser

asm_path = sys.argv[1]
path_root, _ = path.splitext(asm_path)
hack_path = path_root + ".hack"

parser = Parser(asm_path)

with open(hack_path, "w", encoding="utf-8") as f:
    while parser.has_more_lines():
        parser.advance()
        f.write(str(parser.instructionType()) + "\n")
