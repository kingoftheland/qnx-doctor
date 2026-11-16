/* thread_bad.c — INTENTIONALLY BUGGY (fixture for qnx-doctor).
 * RT-03: pthread_create() without PTHREAD_EXPLICIT_SCHED and without
 *        a priority (policy set, setschedparam forgotten).
 * RT-11: sched_priority = 0 (the IDLE priority in QNX Neutrino).
 * RT-09: printf() inside the real-time loop.
 * RT-12: no mlockall() for the real-time thread.
 * QX-05: ThreadCtl(_NTO_TCTL_IO_PRIV, ...) return value unchecked.
 * RT-06/RT-07: MsgSend() unchecked and without a timeout.
 */
#include <stdio.h>
#include <pthread.h>
#include <sched.h>
#include <sys/neutrino.h>
#include <sys/mman.h>

static int coid;

static void *sensor_thread(void *arg)
{
    (void)arg;

    /* QX-05: I/O privilege requested, failure never checked. */
    ThreadCtl(_NTO_TCTL_IO_PRIV, 0);

    for (;;) {
        /* RT-09: console I/O on the real-time path. */
        printf("tick\n");

        /* RT-06 + RT-07: bare MsgSend, no check, no timeout. */
        int msg = 1, rpl = 0;
        MsgSend(coid, &msg, sizeof(msg), &rpl, sizeof(rpl));
    }
    return NULL;
}

int main(void)
{
    pthread_attr_t attr;
    struct sched_param sp;

    pthread_attr_init(&attr);
    /* Policy set, but inheritsched stays PTHREAD_INHERIT_SCHED and no
     * priority is ever applied (RT-03). */
    pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
    /* RT-11: priority 0 = IDLE — this thread would (almost) never run. */
    sp.sched_priority = 0;

    pthread_t t;
    pthread_create(&t, &attr, sensor_thread, NULL);
    pthread_join(t, NULL);
    return 0;
}
