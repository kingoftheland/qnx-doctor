/* isr_good.c — CORRECT version (fixture for qnx-doctor).
 * The interrupt is handled the QNX way: InterruptAttachEvent() with
 * SIGEV_INTR, then InterruptWait() in a real-time thread. No blocking
 * call inside any ISR, all kernel calls checked, memory locked.
 */
#include <pthread.h>
#include <sched.h>
#include <sys/neutrino.h>
#include <sys/siginfo.h>
#include <sys/slog2.h>
#include <sys/mman.h>
#include <stdlib.h>

static int irq = 5;

static void *isr_thread(void *arg)
{
    (void)arg;

    struct sigevent event;
    SIGEV_INTR_INIT(&event);
    if (InterruptAttachEvent(irq, &event, 0) == -1) {
        perror("InterruptAttachEvent");
        return NULL;
    }

    mlockall(MCL_CURRENT | MCL_FUTURE);

    for (;;) {
        if (InterruptWait(NULL, NULL) == -1) {
            perror("InterruptWait");
            continue;
        }
        /* Logging via slog2, never printf(), on the RT path. */
        slog2f(_SLOG_SETCODE(_SLOG_SYSMSG, 0), _SLOG_INFO, "interrupt");
    }
    return NULL;
}

int main(void)
{
    pthread_attr_t attr;
    struct sched_param sp;

    pthread_attr_init(&attr);
    pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
    sp.sched_priority = 20;
    pthread_attr_setschedparam(&attr, &sp);

    pthread_t t;
    if (pthread_create(&t, &attr, isr_thread, NULL) != 0) {
        perror("pthread_create");
        return EXIT_FAILURE;
    }
    pthread_join(t, NULL);
    return 0;
}
