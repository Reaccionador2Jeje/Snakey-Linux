; Snakey Desktop 8 — native NES edition
; MOS 6502 / NROM-256 / ca65
; All UI is drawn by the NES PPU. No Linux or host-side runtime is used.

.segment "HEADER"
.byte "NES", $1A
.byte 2, 1
.byte $00, $00
.res 8, $00

; Zero-page state:
; $00 screen (0 launcher, 1 Files, 2 Console, 3 Settings, 4 About)
; $01 launcher/app selection
; $02 current controller sample
; $03 previous controller sample
; $04 newly pressed buttons
; $05 palette mode
; $06/$07 string pointer
; $08 command result
.segment "CODE"
Reset:
    sei
    cld
    ldx #$40
    stx $4017
    ldx #$FF
    txs
    inx
    stx $2000
    stx $2001
    stx $4010
@vblank1:
    bit $2002
    bpl @vblank1
@vblank2:
    bit $2002
    bpl @vblank2
    lda #$00
    sta $00
    sta $01
    sta $02
    sta $03
    sta $04
    sta $05
    sta $08
    jsr SetPalette
    jsr DrawScreen

MainLoop:
@wait:
    bit $2002
    bpl @wait
    jsr ReadController
    lda $04
    and #$10
    beq @down
    lda $01
    beq @down
    dec $01
    jsr DrawScreen
@down:
    lda $04
    and #$20
    beq @back
    lda $00
    beq @launcher_down
    lda $01
    cmp #$02
    bcs @back
    inc $01
    jsr DrawScreen
    jmp @back
@launcher_down:
    lda $01
    cmp #$03
    bcs @back
    inc $01
    jsr DrawScreen
@back:
    lda $04
    and #$02
    beq @confirm
    lda $00
    beq @confirm
    lda #$00
    sta $00
    sta $01
    jsr DrawScreen
@confirm:
    lda $04
    and #$01
    beq @loop
    lda $00
    beq @open_app
    cmp #$02
    beq @console_action
    cmp #$03
    beq @settings_action
    jmp @loop
@open_app:
    lda $01
    clc
    adc #$01
    sta $00
    lda #$00
    sta $01
    jsr DrawScreen
    jmp @loop
@console_action:
    lda $01
    sta $08
    jsr DrawScreen
    jmp @loop
@settings_action:
    lda $05
    eor #$01
    sta $05
    jsr SetPalette
    jsr DrawScreen
@loop:
    jmp MainLoop

ReadController:
    lda #$01
    sta $4016
    lda #$00
    sta $4016
    sta $02
    ldx #$00
@read:
    lda $4016
    and #$01
    beq @next
    lda ControllerMasks,x
    ora $02
    sta $02
@next:
    inx
    cpx #$08
    bne @read
    lda $03
    eor #$FF
    and $02
    sta $04
    lda $02
    sta $03
    rts

SetPalette:
    lda #$00
    sta $2001
    bit $2002
    lda #$3F
    sta $2006
    lda #$00
    sta $2006
    lda #$0F
    sta $2007
    lda $05
    beq @normal
    lda #$0F
    sta $2007
    lda #$16
    sta $2007
    lda #$27
    sta $2007
    lda #$30
    sta $2007
    jmp @done
@normal:
    lda #$30
    sta $2007
    lda #$21
    sta $2007
    lda #$11
    sta $2007
@done:
    rts

ClearScreen:
    lda #$00
    sta $2001
    bit $2002
    lda #$20
    sta $2006
    lda #$00
    sta $2006
    lda #$00
    ldx #$04
@page:
    ldy #$00
@clear:
    sta $2007
    iny
    bne @clear
    dex
    bne @page
    rts

; DrawText: $06/$07 points to a zero-terminated sequence of CHR tile IDs.
DrawText:
    ldy #$00
@next:
    lda ($06),y
    beq @done
    sta $2007
    iny
    bne @next
@done:
    rts

; Set PPU address from A=high, X=low, then call DrawText.
TextAt:
    sta $2006
    stx $2006
    jmp DrawText

DrawScreen:
    jsr ClearScreen
    ; Persistent title bar.
    lda #$21
    ldx #$CD
    jsr SetTextAddress
    lda #<Title
    sta $06
    lda #>Title
    sta $07
    jsr DrawText

    lda $00
    beq DrawLauncher
    cmp #$01
    beq DrawFiles
    cmp #$02
    beq DrawConsole
    cmp #$03
    beq DrawSettings
    jmp DrawAbout

SetTextAddress:
    sta $2006
    stx $2006
    rts

DrawLauncher:
    lda #$21
    ldx #$CD
    jsr SetTextAddress
    lda #<Title
    sta $06
    lda #>Title
    sta $07
    jsr DrawText
    lda #$21
    ldx #$8A
    jsr SetTextAddress
    lda #<FilesLabel
    sta $06
    lda #>FilesLabel
    sta $07
    jsr DrawText
    lda #$21
    ldx #$AA
    jsr SetTextAddress
    lda #<ConsoleLabel
    sta $06
    lda #>ConsoleLabel
    sta $07
    jsr DrawText
    lda #$21
    ldx #$CA
    jsr SetTextAddress
    lda #<SettingsLabel
    sta $06
    lda #>SettingsLabel
    sta $07
    jsr DrawText
    lda #$21
    ldx #$EA
    jsr SetTextAddress
    lda #<AboutLabel
    sta $06
    lda #>AboutLabel
    sta $07
    jsr DrawText
    ldx $01
    lda CursorAddress,x
    sta $2006
    lda #$0F
    sta $2007
    jmp EnableScreen

DrawFiles:
    lda #$21
    ldx #$8A
    jsr SetTextAddress
    lda #<FilesLabel
    sta $06
    lda #>FilesLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$0A
    jsr SetTextAddress
    lda #<CatalogLabel
    sta $06
    lda #>CatalogLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$4A
    jsr SetTextAddress
    lda #<ReadmeLabel
    sta $06
    lda #>ReadmeLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$8A
    jsr SetTextAddress
    lda #<ConfigLabel
    sta $06
    lda #>ConfigLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$CA
    jsr SetTextAddress
    lda #<LicenseLabel
    sta $06
    lda #>LicenseLabel
    sta $07
    jsr DrawText
    jmp EnableScreen

DrawConsole:
    lda #$21
    ldx #$8A
    jsr SetTextAddress
    lda #<ConsoleLabel
    sta $06
    lda #>ConsoleLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$0A
    jsr SetTextAddress
    lda #<HelpLabel
    sta $06
    lda #>HelpLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$4A
    jsr SetTextAddress
    lda #<AboutCmdLabel
    sta $06
    lda #>AboutCmdLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$8A
    jsr SetTextAddress
    lda #<ClearLabel
    sta $06
    lda #>ClearLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$CA
    jsr SetTextAddress
    lda $08
    beq @help_result
    cmp #$01
    beq @about_result
    lda #<ClearedLabel
    sta $06
    lda #>ClearedLabel
    sta $07
    jmp @result
@about_result:
    lda #<NativeLabel
    sta $06
    lda #>NativeLabel
    sta $07
    jmp @result
@help_result:
    lda #<HelpResult
    sta $06
    lda #>HelpResult
    sta $07
@result:
    jsr DrawText
    ldx $01
    lda CursorAddress,x
    clc
    adc #$80
    sta $2006
    lda #$0F
    sta $2007
    jmp EnableScreen

DrawSettings:
    lda #$21
    ldx #$8A
    jsr SetTextAddress
    lda #<SettingsLabel
    sta $06
    lda #>SettingsLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$4A
    jsr SetTextAddress
    lda #<PaletteLabel
    sta $06
    lda #>PaletteLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$8A
    jsr SetTextAddress
    lda $05
    beq @palette0
    lda #<PaletteOne
    sta $06
    lda #>PaletteOne
    sta $07
    jmp @palette_draw
@palette0:
    lda #<PaletteZero
    sta $06
    lda #>PaletteZero
    sta $07
@palette_draw:
    jsr DrawText
    jmp EnableScreen

DrawAbout:
    lda #$21
    ldx #$8A
    jsr SetTextAddress
    lda #<AboutLabel
    sta $06
    lda #>AboutLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$4A
    jsr SetTextAddress
    lda #<NativeLabel
    sta $06
    lda #>NativeLabel
    sta $07
    jsr DrawText
    lda #$22
    ldx #$8A
    jsr SetTextAddress
    lda #<HardwareLabel
    sta $06
    lda #>HardwareLabel
    sta $07
    jsr DrawText
    jmp EnableScreen

EnableScreen:
    lda #$00
    sta $2005
    sta $2005
    lda #$08
    sta $2001
    rts

ControllerMasks:
.byte $01,$02,$04,$08,$10,$20,$40,$80
CursorAddress:
.byte $68,$88,$A8,$C8

Title:          .byte 1,18,19,16,17,6,0
FilesLabel:     .byte 14,12,8,17,1,0
ConsoleLabel:   .byte 9,13,18,1,13,8,17,0
SettingsLabel:  .byte 1,17,11,11,12,18,22,1,0
AboutLabel:     .byte 19,20,13,21,11,0
CatalogLabel:   .byte 9,19,11,19,8,13,22,0
ReadmeLabel:    .byte 18,17,19,24,25,17,0
ConfigLabel:    .byte 9,13,18,14,12,22,0
LicenseLabel:   .byte 8,12,9,17,18,1,17,0
HelpLabel:      .byte 23,17,8,16,0
AboutCmdLabel:  .byte 19,20,13,21,11,0
ClearLabel:     .byte 9,8,17,19,18,0
HelpResult:     .byte 23,17,8,16,0
NativeLabel:    .byte 18,19,11,12,6,17,0
ClearedLabel:   .byte 9,8,17,19,18,0
PaletteLabel:   .byte 16,19,8,17,11,11,17,0
PaletteZero:    .byte 16,19,8,17,11,11,17,0
PaletteOne:     .byte 16,19,8,17,11,11,17,0
HardwareLabel:  .byte 23,13,25,17,0

.segment "VECTORS"
.word Reset, Reset, Reset

.segment "CHARS"
; Tile 0 blank. 1..16 preserve the original SNAKEY/menu alphabet.
.res 16, $00
; S
.byte $3C,$42,$40,$3C,$02,$42,$3C,$00
.res 8, $00
; N
.byte $42,$62,$52,$4A,$46,$42,$42,$00
.res 8, $00
; A
.byte $18,$24,$42,$7E,$42,$42,$42,$00
.res 8, $00
; K
.byte $42,$44,$48,$70,$48,$44,$42,$00
.res 8, $00
; E
.byte $7E,$40,$40,$7C,$40,$40,$7E,$00
.res 8, $00
; Y
.byte $42,$42,$24,$18,$18,$18,$18,$00
.res 8, $00
; P
.byte $7C,$42,$42,$7C,$40,$40,$40,$00
.res 8, $00
; L
.byte $40,$40,$40,$40,$40,$40,$7E,$00
.res 8, $00
; C
.byte $3C,$42,$40,$40,$40,$42,$3C,$00
.res 8, $00
; R
.byte $7C,$42,$42,$7C,$48,$44,$42,$00
.res 8, $00
; T
.byte $7E,$18,$18,$18,$18,$18,$18,$00
.res 8, $00
; I
.byte $7E,$18,$18,$18,$18,$18,$7E,$00
.res 8, $00
; O
.byte $3C,$42,$42,$42,$42,$42,$3C,$00
.res 8, $00
; F
.byte $7E,$40,$40,$7C,$40,$40,$40,$00
.res 8, $00
; > cursor
.byte $40,$20,$10,$08,$10,$20,$40,$00
.res 8, $00
; ? fallback
.byte $3C,$42,$02,$0C,$10,$00,$10,$00
.res 8, $00
; E (17)
.byte $7E,$40,$40,$7C,$40,$40,$7E,$00
.res 8, $00
; N (18)
.byte $42,$62,$52,$4A,$46,$42,$42,$00
.res 8, $00
; A (19)
.byte $18,$24,$42,$7E,$42,$42,$42,$00
.res 8, $00
; B (20)
.byte $7C,$42,$42,$7C,$42,$42,$7C,$00
.res 8, $00
; U (21)
.byte $42,$42,$42,$42,$42,$42,$3C,$00
.res 8, $00
; G (22)
.byte $3C,$42,$40,$4E,$42,$42,$3C,$00
.res 8, $00
; H (23)
.byte $42,$42,$42,$7E,$42,$42,$42,$00
.res 8, $00
; D (24)
.byte $78,$44,$42,$42,$42,$44,$78,$00
.res 8, $00
; M (25)
.byte $42,$66,$5A,$5A,$42,$42,$42,$00
.res 8, $00
.res $2000 - (26 * 16), $00
