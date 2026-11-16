/* heap_good.c — CORRECT version (fixture for qnx-doctor).
 * All heap allocation happens once in init_pool(), before the RT
 * thread starts. The RT loop reuses a static pool — no malloc/free,
 * no printf, memory locked.
 */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>
#include <sys/slog2.h>
#include <sys/mman.h>

#define POOL_SIZE 256

static char pool[POOL_SIZE];

static void init_pool(void)
{
    /* One-time allocation during initialisation — allowed. */
    char *tmp = malloc(POOL_SIZE);
    if (tmp == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < POOL_SIZE; i++) {
        pool[i] = tmp[i];
    }
    free(tmp);
}

static void *heap_rt_thread(void *arg)
{
    (void)arg;
    mlockall(MCL_CURRENT | MCL_FUTURE);
    for (;;) {
        /* Reuse the pre-allocated pool — no allocation on the RT path. */
        pool[0] ^= 0x5A;
        slog2f(_SLOG_SETCODE(_SLOG_SYSMSG, 0), _SLOG_INFO, "pool tick");
    }
    return NULL;
}

int main(void)
{
    init_pool();

    pthread_attr_t attr;
    struct sched_param sp;
    pthread_attr_init(&attr);
    pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED);
    pthread_attr_setschedpolicy(&attr, SCHED_FIFO);
    sp.sched_priority = 15;
    pthread_attr_setschedparam(&attr, &sp);

    pthread_t t;
    if (pthread_create(&t, &attr, heap_rt_thread, NULL) != 0) {
        perror("pthread_create");
        return EXIT_FAILURE;
    }
    pthread_join(t, NULL);
    return 0;
}
