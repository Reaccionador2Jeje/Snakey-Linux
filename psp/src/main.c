#include <pspkernel.h>
#include <pspdebug.h>
#include <pspctrl.h>
#include <pspdisplay.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

PSP_MODULE_INFO("Snakey PSP", PSP_MODULE_USER, 1, 0);
PSP_MAIN_THREAD_ATTR(THREAD_ATTR_USER | THREAD_ATTR_VFPU);

#define COMMAND_MAX 48
#define KEY_ROWS 5
#define KEY_COLS 10

typedef enum {
    VIEW_DESKTOP,
    VIEW_TERMINAL,
    VIEW_SYSTEM,
    VIEW_ABOUT
} View;

static View current_view = VIEW_DESKTOP;
static int desktop_selected = 0;
static int key_row = 1;
static int key_col = 0;
static char command_line[COMMAND_MAX + 1];
static char terminal_output[7][58];
static int output_count = 0;
static int output_scroll = 0;
static const char *desktop_items[] = {
    "Terminal",
    "System monitor",
    "About Snakey",
    "Power off"
};
static const char *keyboard[KEY_ROWS] = {
    "1234567890",
    "qwertyuiop",
    "asdfghjkl;",
    "zxcvbnm.-_",
    " SPACE DEL "
};

static void output(const char *line)
{
    if (output_count < 7) {
        snprintf(terminal_output[output_count++], sizeof(terminal_output[0]), "%s", line);
    } else {
        for (int i = 0; i < 6; ++i)
            snprintf(terminal_output[i], sizeof(terminal_output[i]), "%s", terminal_output[i + 1]);
        snprintf(terminal_output[6], sizeof(terminal_output[6]), "%s", line);
    }
    output_scroll = 0;
}

static void clear_output(void)
{
    output_count = 0;
    output_scroll = 0;
}

static void draw_header(const char *subtitle)
{
    pspDebugScreenClear();
    pspDebugScreenSetTextColor(0xFF70D080);
    pspDebugScreenSetXY(2, 1);
    pspDebugScreenPrintf("SNAKEY PSP");
    pspDebugScreenSetTextColor(0xFFB0B0B0);
    pspDebugScreenSetXY(2, 2);
    pspDebugScreenPrintf("%s", subtitle);
    pspDebugScreenSetTextColor(0xFFFFFFFF);
    pspDebugScreenSetXY(2, 3);
    pspDebugScreenPrintf("----------------------------------------------------------");
}

static void draw_desktop(void)
{
    draw_header("Desktop environment | Native PSP edition");
    pspDebugScreenSetXY(3, 6);
    pspDebugScreenSetTextColor(0xFF70D080);
    pspDebugScreenPrintf("[ SNAKEY WORKSPACE ]");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
    pspDebugScreenSetXY(3, 8);
    pspDebugScreenPrintf("Select an application:");
    for (int i = 0; i < 4; ++i) {
        pspDebugScreenSetXY(5, 11 + i * 2);
        pspDebugScreenSetTextColor(i == desktop_selected ? 0xFF70D080 : 0xFFFFFFFF);
        pspDebugScreenPrintf("%s  %s", i == desktop_selected ? ">" : " ", desktop_items[i]);
    }
    pspDebugScreenSetTextColor(0xFFB0B0B0);
    pspDebugScreenSetXY(2, 25);
    pspDebugScreenPrintf("D-PAD: navigate   CROSS: open   START: power off");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
}

static void draw_terminal(void)
{
    draw_header("Terminal | Built-in Snakey command runtime");
    pspDebugScreenSetXY(2, 5);
    pspDebugScreenSetTextColor(0xFF70D080);
    pspDebugScreenPrintf("snakey@psp:~$");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
    pspDebugScreenSetXY(2, 6);
    pspDebugScreenPrintf("Welcome. Type help to list built-in commands.");
    for (int i = 0; i < output_count; ++i) {
        pspDebugScreenSetXY(2, 8 + i);
        pspDebugScreenPrintf("%s", terminal_output[i]);
    }
    pspDebugScreenSetXY(2, 16);
    pspDebugScreenSetTextColor(0xFF70D080);
    pspDebugScreenPrintf("> %s_", command_line);
    pspDebugScreenSetTextColor(0xFFFFFFFF);
    pspDebugScreenSetXY(2, 19);
    pspDebugScreenPrintf("On-screen keyboard (D-PAD + CROSS):");
    for (int r = 0; r < KEY_ROWS; ++r) {
        pspDebugScreenSetXY(5, 21 + r);
        for (int c = 0; c < KEY_COLS; ++c) {
            char ch = keyboard[r][c];
            if (r == 4 && c == 0) {
                pspDebugScreenPrintf(key_row == r && key_col == c ? "[SPACE]" : " SPACE ");
                c = 5;
            } else if (r == 4 && c == 6) {
                pspDebugScreenPrintf(key_row == r && key_col == c ? "[DEL]" : " DEL ");
                c = 9;
            } else {
                if (key_row == r && key_col == c)
                    pspDebugScreenSetTextColor(0xFF70D080);
                pspDebugScreenPrintf("%c ", ch);
                pspDebugScreenSetTextColor(0xFFFFFFFF);
            }
        }
    }
    pspDebugScreenSetTextColor(0xFFB0B0B0);
    pspDebugScreenSetXY(2, 28);
    pspDebugScreenPrintf("START: run command  CIRCLE: desktop  SQUARE: backspace");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
}

static void draw_info(const char *title, const char *line1, const char *line2, const char *line3)
{
    draw_header(title);
    pspDebugScreenSetXY(3, 7); pspDebugScreenPrintf("%s", line1);
    pspDebugScreenSetXY(3, 9); pspDebugScreenPrintf("%s", line2);
    pspDebugScreenSetXY(3, 11); pspDebugScreenPrintf("%s", line3);
    pspDebugScreenSetTextColor(0xFFB0B0B0);
    pspDebugScreenSetXY(2, 25); pspDebugScreenPrintf("CIRCLE: return to desktop");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
}

static void execute_command(void)
{
    char result[58];
    if (command_line[0] == '\0')
        return;

    if (strcmp(command_line, "help") == 0) {
        output("Built-in commands:");
        output("help clear uname version mem pwd ls echo exit");
    } else if (strcmp(command_line, "clear") == 0) {
        clear_output();
    } else if (strcmp(command_line, "uname") == 0) {
        output("Snakey PSP | MIPS Allegrex | PSP SDK");
    } else if (strcmp(command_line, "version") == 0) {
        output("Snakey PSP development build 0.2");
    } else if (strcmp(command_line, "mem") == 0) {
        output("Hardware target: PSP | RAM class: 32 MiB");
    } else if (strcmp(command_line, "pwd") == 0) {
        output("/snakey");
    } else if (strcmp(command_line, "ls") == 0) {
        output("workspace/  system/  apps/  cartridges/");
        output("(virtual entries; storage not mounted)");
    } else if (strncmp(command_line, "echo ", 5) == 0) {
        output(command_line + 5);
    } else if (strcmp(command_line, "exit") == 0) {
        command_line[0] = '\0';
        current_view = VIEW_DESKTOP;
        return;
    } else {
        snprintf(result, sizeof(result), "Unknown command: %.40s", command_line);
        output(result);
        output("Type help for available commands.");
    }
    command_line[0] = '\0';
}

static void insert_key(void)
{
    if (key_row == 4 && key_col == 0) {
        size_t len = strlen(command_line);
        if (len < COMMAND_MAX) {
            command_line[len] = ' ';
            command_line[len + 1] = '\0';
        }
    } else if (key_row == 4 && key_col == 6) {
        size_t len = strlen(command_line);
        if (len > 0)
            command_line[len - 1] = '\0';
    } else {
        size_t len = strlen(command_line);
        if (len < COMMAND_MAX) {
            command_line[len] = keyboard[key_row][key_col];
            command_line[len + 1] = '\0';
        }
    }
}

static void wait_for_release(void)
{
    SceCtrlData pad;
    do {
        sceCtrlReadBufferPositive(&pad, 1);
        sceKernelDelayThread(16000);
    } while (pad.Buttons != 0);
}

int main(void)
{
    SceCtrlData pad;
    unsigned int previous = 0;

    pspDebugScreenInit();
    sceCtrlSetSamplingCycle(0);
    sceCtrlSetSamplingMode(PSP_CTRL_MODE_ANALOG);
    draw_desktop();

    for (;;) {
        sceCtrlReadBufferPositive(&pad, 1);
        unsigned int pressed = pad.Buttons & ~previous;
        previous = pad.Buttons;

        if (current_view == VIEW_DESKTOP) {
            if (pressed & PSP_CTRL_UP) {
                desktop_selected = (desktop_selected + 3) % 4;
                draw_desktop();
            } else if (pressed & PSP_CTRL_DOWN) {
                desktop_selected = (desktop_selected + 1) % 4;
                draw_desktop();
            } else if (pressed & PSP_CTRL_CROSS) {
                wait_for_release();
                if (desktop_selected == 0) {
                    current_view = VIEW_TERMINAL;
                    draw_terminal();
                } else if (desktop_selected == 1) {
                    current_view = VIEW_SYSTEM;
                    draw_info("System monitor", "Platform: Sony PSP / PPSSPP", "CPU: MIPS Allegrex", "Runtime: Snakey native command shell");
                } else if (desktop_selected == 2) {
                    current_view = VIEW_ABOUT;
                    draw_info("About Snakey", "Snakey Linux console environment", "PSP edition: native homebrew interface", "Not a Linux kernel boot yet");
                } else {
                    sceKernelExitGame();
                }
            } else if (pressed & PSP_CTRL_START) {
                sceKernelExitGame();
            }
        } else if (current_view == VIEW_TERMINAL) {
            if (pressed & PSP_CTRL_UP) {
                key_row = (key_row + KEY_ROWS - 1) % KEY_ROWS;
                draw_terminal();
            } else if (pressed & PSP_CTRL_DOWN) {
                key_row = (key_row + 1) % KEY_ROWS;
                if (key_row == 4 && key_col > 6) key_col = 6;
                draw_terminal();
            } else if (pressed & PSP_CTRL_LEFT) {
                key_col = (key_col + KEY_COLS - 1) % KEY_COLS;
                if (key_row == 4 && key_col != 0 && key_col != 6) key_col = 0;
                draw_terminal();
            } else if (pressed & PSP_CTRL_RIGHT) {
                key_col = (key_col + 1) % KEY_COLS;
                if (key_row == 4 && key_col != 0 && key_col != 6) key_col = 6;
                draw_terminal();
            } else if (pressed & PSP_CTRL_CROSS) {
                insert_key();
                draw_terminal();
            } else if (pressed & PSP_CTRL_SQUARE) {
                size_t len = strlen(command_line);
                if (len > 0) command_line[len - 1] = '\0';
                draw_terminal();
            } else if (pressed & PSP_CTRL_START) {
                execute_command();
                draw_terminal();
            } else if (pressed & PSP_CTRL_CIRCLE) {
                current_view = VIEW_DESKTOP;
                draw_desktop();
            }
        } else if (pressed & PSP_CTRL_CIRCLE) {
            current_view = VIEW_DESKTOP;
            draw_desktop();
        }
        sceKernelDelayThread(16000);
    }
    return 0;
}
