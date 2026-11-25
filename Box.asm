// Box.asm  (K = 62)
// Draws a black box while any key is pressed, erases it when released.
// Start row = 62  -> start address = SCREEN + 32*62 = 16384 + 1984 = 18368
// Height = 20 rows
// Width  = 16 * ((62 mod 4) + 1) = 48 pixels = 3 words per row

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE           // key pressed -> draw black
    @color
    M=0             // no key -> color = white (erase)
    @PAINT
    0;JMP
(DRAW)
    @color
    M=-1            // color = black
(PAINT)
    @18368          // address of row 62, column 0
    D=A
    @addr
    M=D
    @20
    D=A
    @rows
    M=D             // rows = 20
(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // word 0 (pixels 0-15)
    A=A+1
    M=D             // word 1 (pixels 16-31)
    A=A+1
    M=D             // word 2 (pixels 32-47)
    @32
    D=A
    @addr
    M=D+M           // move to next row
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @LOOP
    0;JMP
