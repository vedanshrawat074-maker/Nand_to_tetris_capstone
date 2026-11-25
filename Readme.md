# Nand to Tetris – I Capstone Project

**Name:** Vedansh Rawat  
**Roll Number:** 2501730362  
**Course:** Nand to Tetris – I (ETCNTC301)  
**Institution:** K.R. Mangalam University  
**School:** School of Engineering & Technology

## Project Overview

This capstone project implements key components of the Nand to Tetris computer system. It includes the hardware architecture using HDL, a Python-based Hack assembler, and an assembly program that draws a rectangle on the screen in response to keyboard input.

## Project Components

### Part A – Hardware Implementation

The following HDL files implement the computer architecture:

- `CPU.hdl` – Implements the Hack CPU.
- `Memory.hdl` – Implements the computer's memory system.
- `Computer.hdl` – Connects the CPU, memory, and ROM components.

### Part B – Hack Assembler

A two-pass assembler written in Python translates Hack assembly (`.asm`) programs into Hack machine code (`.hack`).

Features include:
- Translation of A-instructions and C-instructions into binary.
- Label handling using a symbol table.
- Allocation of variables starting from RAM address 16.
- Warning when duplicate labels are detected.

Test programs:
- `Add.asm`
- `Max.asm`
- `Rect.asm`
- `Pong.asm`

### Part C – Screen Drawing Program

`Box.asm` draws a black rectangular box on the Hack screen while a keyboard key is pressed. The box disappears when the key is released.

The rectangle dimensions and position are based on the roll number calculation:

- **K = 62**
- **K mod 3 = 2**
- **Box width = 16 × (2 + 1) = 48 pixels**
- **Starting screen row = 62**
- **Box height = 20 rows**
- **Starting screen address = 16384 + (32 × 62) = 18368**
- **Words per row = 3**

## Repository Structure

```text
capstone/
├── CPU.hdl
├── Memory.hdl
├── Computer.hdl
├── assembler.py
├── Add.asm
├── Add.hack
├── Max.asm
├── Max.hack
├── Rect.asm
├── Rect.hack
├── Pong.asm
├── Pong.hack
├── Box.asm
├── Box.hack
├── DupLabel.asm
└── README.md
```

The project report is included separately in the repository.

## Tools Used

- Python
- Hack Assembly Language
- HDL
- Nand to Tetris Hardware Simulator
- Visual Studio Code

## Testing and Verification

The HDL components were tested using the Nand to Tetris Hardware Simulator. The assembler was tested with the supplied assembly programs, and its generated machine code was compared with the corresponding reference files. The Box program was tested by pressing and releasing a key in the Hack computer simulator.

## Conclusion

This project demonstrates the implementation of a basic computer architecture, the translation of assembly language into machine code, and interaction with the Hack computer's screen and keyboard. It helped connect hardware design concepts with low-level programming and computer organization.