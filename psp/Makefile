TARGET = snakey
OBJS = src/main.o

INCDIR =
CFLAGS = -O2 -G0 -Wall -Wextra
CXXFLAGS = ${CFLAGS} -fno-exceptions
ASFLAGS = ${CFLAGS}

BUILD_PRX = 1
PSP_FW_VERSION = 660
PSP_EBOOT_TITLE = Snakey PSP

LIBS = -lpspdebug -lpspdisplay -lpspctrl -lpspkernel -lpspuser

EXTRA_TARGETS = EBOOT.PBP

include $(PSPSDK)/lib/build.mak
