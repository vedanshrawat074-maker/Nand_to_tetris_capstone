#!/usr/bin/env python3
"""Hack assembler (two-pass).  Usage: python assembler.py Prog.asm [Prog.hack]

Pass 1: strip comments/blank lines, record labels -> instruction addresses.
Pass 2: translate to 16-bit binary, resolve labels, allocate variables from 16.
Extra feature (K = 62, K mod 3 = 2): warn if the same label is defined twice.
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001',
    '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
def dest_bits(dest):
    """Accept the letters A, D, M in any order (MD, DM, AM, MA, ...)."""
    if len(set(dest)) != len(dest) or any(ch not in 'ADM' for ch in dest):
        raise ValueError('invalid destination: ' + dest)
    return ('1' if 'A' in dest else '0') + ('1' if 'D' in dest else '0') + \
           ('1' if 'M' in dest else '0')

JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}


def predefined():
    table = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
             'SCREEN': 16384, 'KBD': 24576}
    for i in range(16):
        table['R%d' % i] = i
    return table


def clean(line):
    """Remove comments and all whitespace."""
    return ''.join(line.split('//')[0].split())


def first_pass(lines, symbols):
    """Record labels. Returns list of (line_number, instruction)."""
    instructions = []
    label_lines = {}
    address = 0
    for num, raw in enumerate(lines, 1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith('(') and line.endswith(')'):
            label = line[1:-1]
            if label in label_lines:
                # --- extra feature for K mod 3 == 2 ---
                print("Warning: Line %d: duplicate label '%s' "
                      "(first defined on line %d)" % (num, label, label_lines[label]))
            else:
                label_lines[label] = num
            symbols[label] = address  # later definition overrides
        else:
            instructions.append((num, line))
            address += 1
    return instructions


def translate_c(line):
    dest, comp, jump = '', line, ''
    if '=' in line:
        dest, comp = line.split('=', 1)
    if ';' in comp:
        comp, jump = comp.split(';', 1)
    if comp not in COMP or jump not in JUMP:
        raise ValueError('invalid instruction: ' + line)
    return '111' + COMP[comp] + dest_bits(dest) + JUMP[jump]


def second_pass(instructions, symbols):
    out = []
    next_var = 16
    for num, line in instructions:
        if line.startswith('@'):
            sym = line[1:]
            if sym.isdigit():
                value = int(sym)
            else:
                if sym not in symbols:
                    symbols[sym] = next_var
                    next_var += 1
                value = symbols[sym]
            out.append(format(value, '016b'))
        else:
            try:
                out.append(translate_c(line))
            except ValueError as e:
                sys.exit('Line %d: %s' % (num, e))
    return out


def assemble(path, out_path=None):
    with open(path) as f:
        lines = f.read().splitlines()
    symbols = predefined()
    instructions = first_pass(lines, symbols)
    binary = second_pass(instructions, symbols)
    out_path = out_path or path.rsplit('.', 1)[0] + '.hack'
    with open(out_path, 'w') as f:
        f.write('\n'.join(binary) + '\n')
    return out_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: python assembler.py Prog.asm [Prog.hack]')
    print('Wrote', assemble(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
