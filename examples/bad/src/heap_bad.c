/* heap_bad.c — INTENTIONALLY BUGGY (fixture for qnx-doctor).
 * RT-01: malloc()/free() inside a real-time thread.
 * RT-05: malloc() inside an unbounded while(1) loop.
 * RT-09: printf() inside the real-time loop.
 * RT-11: sched_priority = 0 (IDLE).
 * RT-12: no mlockall() for the real-time thread.
 * RT-03: pthread_create() with NULL attributes.
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>

static void *heap_rt_thread(void *arg)
{
    (void)arg;
    struct sched_param sp;
    /* RT-11: priority 0 = IDLE, applied directly. */
    sp.sched_priority = 0;
    pthread_setschedparam(pthread_self(), SCHED_FIFO, &sp);

    for (;;) {
        /* RT-05 + RT-01: unbounded heap allocation in the RT loop. */
        char *buf = malloc(256);
        /* RT-09: console I/O on the real-time path. */
        printf("processing %p\n", (void *)buf);
        /* RT-01: free() in the RT thread. */
        free(buf);
    }
    return NULL;
}

int main(void)
{
    pthread_t t;
    /* RT-03: NULL attributes — no explicit scheduling at all. */
    pthread_create(&t, NULL, heap_rt_thread, NULL);
    pthread_join(t, NULL);
    return 0;
}
