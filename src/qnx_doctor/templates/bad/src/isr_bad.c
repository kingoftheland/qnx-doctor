/* isr_bad.c — INTENTIONALLY BUGGY (fixture for qnx-doctor).
 * RT-04: blocking calls inside the InterruptAttach() handler.
 * RT-06: InterruptAttach() / MsgSend() return values never checked.
 * RT-07: MsgSend() with no TimerTimeout().
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/neutrino.h>
#include <sys/siginfo.h>

static int coid;
static int chid;

static const struct sigevent *isr_handler(void *area, int id)
{
    (void)area;
    (void)id;

    /* RT-04: blocking MsgSend() inside an ISR handler. */
    int msg = 1, rpl = 0;
    MsgSend(coid, &msg, sizeof(msg), &rpl, sizeof(rpl));

    /* RT-04: printf() blocks on console I/O inside an ISR. */
    printf("interrupt!\n");

    /* RT-04: heap allocation inside an ISR. */
    char *buf = malloc(64);
    (void)buf;
    return NULL;
}

int main(void)
{
    chid = ChannelCreate(0);

    /* RT-06: InterruptAttach() return value never checked. */
    InterruptAttach(5, isr_handler, NULL, 0, 0);

    for (;;) {
        MsgReceive(chid, NULL, 0, NULL);
    }
    return 0;
}
