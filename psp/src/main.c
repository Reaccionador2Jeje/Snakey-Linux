#include <pspkernel.h>
#include <pspdebug.h>
#include <pspctrl.h>
#include <pspdisplay.h>
#include <pspgu.h>
#include <psputility.h>
#include <stdio.h>
#include <string.h>

PSP_MODULE_INFO("Snakey PSP", PSP_MODULE_USER, 1, 0);
PSP_MAIN_THREAD_ATTR(THREAD_ATTR_USER | THREAD_ATTR_VFPU);

#define MENU_COUNT 4

static const char *menu_items[MENU_COUNT] = {
    "Start Snakey shell",
    "System information",
    "Build information",
    "Power off"
};

static int selected = 0;

static void draw_screen(const char *page)
{
    pspDebugScreenClear();
    pspDebugScreenSetXY(2, 1);
    pspDebugScreenSetTextColor(0xFF70D080);
    pspDebugScreenPrintf("SNAKEY PSP");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
    pspDebugScreenSetXY(2, 3);
    pspDebugScreenPrintf("Native PSP homebrew | Snakey Linux family");
    pspDebugScreenSetXY(2, 5);
    pspDebugScreenPrintf("----------------------------------------");

    if (page != NULL) {
        pspDebugScreenSetXY(2, 7);
        pspDebugScreenPrintf("%s", page);
        pspDebugScreenSetXY(2, 10);
        pspDebugScreenPrintf("Press CIRCLE to return.");
        return;
    }

    pspDebugScreenSetXY(2, 7);
    pspDebugScreenPrintf("Use UP/DOWN and CROSS to select:");
    for (int i = 0; i < MENU_COUNT; ++i) {
        pspDebugScreenSetXY(4, 10 + i * 2);
        pspDebugScreenSetTextColor(i == selected ? 0xFF70D080 : 0xFFFFFFFF);
        pspDebugScreenPrintf("%s %s", i == selected ? ">" : " ", menu_items[i]);
    }
    pspDebugScreenSetTextColor(0xFFB0B0B0);
    pspDebugScreenSetXY(2, 22);
    pspDebugScreenPrintf("START: exit   CROSS: select   CIRCLE: back");
    pspDebugScreenSetTextColor(0xFFFFFFFF);
}

static void wait_for_release(void)
{
    SceCtrlData pad;
    do {
        sceCtrlReadBufferPositive(&pad, 1);
        sceKernelDelayThread(16000);
    } while (pad.Buttons != 0);
}

static void show_page(const char *message)
{
    SceCtrlData pad;
    draw_screen(message);
    for (;;) {
        sceCtrlReadBufferPositive(&pad, 1);
        if (pad.Buttons & PSP_CTRL_CIRCLE)
            break;
        if (pad.Buttons & PSP_CTRL_START)
            sceKernelExitGame();
        sceKernelDelayThread(16000);
    }
    wait_for_release();
}

int main(void)
{
    SceCtrlData pad;
    unsigned int previous = 0;

    pspDebugScreenInit();
    sceCtrlSetSamplingCycle(0);
    sceCtrlSetSamplingMode(PSP_CTRL_MODE_ANALOG);

    draw_screen(NULL);
    for (;;) {
        sceCtrlReadBufferPositive(&pad, 1);
        unsigned int pressed = pad.Buttons & ~previous;
        previous = pad.Buttons;

        if (pressed & PSP_CTRL_UP) {
            selected = (selected + MENU_COUNT - 1) % MENU_COUNT;
            draw_screen(NULL);
        } else if (pressed & PSP_CTRL_DOWN) {
            selected = (selected + 1) % MENU_COUNT;
            draw_screen(NULL);
        } else if (pressed & PSP_CTRL_CROSS) {
            wait_for_release();
            switch (selected) {
            case 0:
                show_page("Snakey shell is running. Interactive command runtime is next.");
                break;
            case 1:
                show_page("Platform: Sony PSP\nCPU: MIPS Allegrex\nMemory class: 32 MiB\nRuntime: native PSP homebrew");
                break;
            case 2:
                show_page("Snakey PSP development build\nTarget: PPSSPP / Sony PSP\nFormat: EBOOT.PBP");
                break;
            case 3:
                sceKernelExitGame();
                break;
            }
            draw_screen(NULL);
        } else if (pressed & PSP_CTRL_START) {
            sceKernelExitGame();
        }
        sceKernelDelayThread(16000);
    }
    return 0;
}
