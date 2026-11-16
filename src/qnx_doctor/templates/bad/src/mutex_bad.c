/* mutex_bad.c — INTENTIONALLY BUGGY (fixture for qnx-doctor).
 * RT-02: mutex created with NULL attributes (no priority protocol).
 * QX-01: ChannelCreate(0) in a server that also handles pulses.
 * QX-04: name_attach() with no matching name_detach().
 * RT-06/RT-07: MsgSend() unchecked and without a timeout.
 */
#include <stdio.h>
#include <pthread.h>
#include <sys/neutrino.h>
#include <sys/dispatch.h>

static pthread_mutex_t lock;
static int chid;

static void *server_thread(void *arg)
{
    (void)arg;
    for (;;) {
        struct _pulse pulse;
        MsgReceivePulse(chid, &pulse, sizeof(pulse), NULL);
        pthread_mutex_lock(&lock);
        /* ... handle pulse ... */
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void)
{
    /* RT-02: NULL attributes — no PTHREAD_PRIO_INHERIT / PROTECT. */
    pthread_mutex_init(&lock, NULL);

    /* QX-01: plain ChannelCreate(0) although pulses are received. */
    chid = ChannelCreate(0);

    /* QX-04: attached, never detached. */
    name_attach(NULL, "bad_server", 0);

    pthread_t t;
    pthread_create(&t, NULL, server_thread, NULL);

    /* RT-06 + RT-07: bare MsgSend, no check, no TimerTimeout. */
    int coid = ConnectAttach(0, 0, chid, 0, 0);
    int msg = 42, rpl = 0;
    MsgSend(coid, &msg, sizeof(msg), &rpl, sizeof(rpl));
    return 0;
}
